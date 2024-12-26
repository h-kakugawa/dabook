# 離散事象シミュレーター  コア部分
# - 発生する事象をヒープに格納
# - ヒープから発生時刻の順で事象を取り出し，処理を行う
# - ヒープが空になればシミュレーションは終了
from process_if import ProcessIf
import sys
import os
import heapq

class Simulator():
    PID_SYS = 'SYS'   # Special pid for system
    EV_INITIATOR = 'EV-INITIATOR' # 事象型: 始動プロセス
    EV_INTERNAL  = 'EV-INTERNAL'  # 事象型: 内部
    EV_TIMER     = 'EV-TIMER'     # 事象型: タイマ
    EV_RECEIVE   = 'EV-RECV'      # 事象型: 受信
    EV_SEND      = 'EV-SEND'      # 事象型: 送信 (事象スクリプト内限定)
    EV_SYSTEM    = 'EV-SYSTEM'    # 事象型: システム

    def __init__(self, nw, procs, initips_spec = 'all', evscript = []):
        self.__nw = nw          # ネットワーク
        self.__proctbl = procs  # プロセス表 (添字: 0..n-1)
        self.__pid_set = list(range(self.__nw.get_n()))
                                # プロセス識別子の集合
        self.__initips = self.__initiators(initips_spec) # Initiators
        self.__evscript = evscript   # 事象スクリプト
        self.__curtime = 0.0    # 現在時刻
        self.__evq = [ ]        # イベントキュー
        self.__evseq = 0        # イベントのシーケンス番号
        self.__nmsgs = 0        # 送信メッセージの総数

    # 始動プロセスのリストを作成 
    def __initiators(self, initips_spec):
        x = []
        if (initips_spec is None) or \
           (type(initips_spec) is str and initips_spec == 'none'):
            x = [ ]
        elif (type(initips_spec) is str) and (initips_spec == 'all'):
            x = self.__pid_set
        elif type(initips_spec) is int:  # 例: 2
            x = [initips_spec]
        elif type(initips_spec) is list:  # 例: [1,3,4]
            x = [int(pid) for pid in initips_spec]
        else:
            sys.exit('ERROR: UNKNOWN INITIATORS SPEC: ' + str(initips_spec))
        if any([(type(pid) is not int) or (pid not in self.__pid_set)
                for pid in x]):
            sys.exit('ERROR: ILLEGAL INITIATORS SPEC: ' + str(initips_spec))
        return x

    # 現在時刻
    def get_time(self):
        return self.__curtime

    # シミュレーション実行開始 (出力ファイル指定)
    def start(self, fname_output=None, overwrite=None):
        if fname_output is not None and \
           (overwrite is None or overwrite is False) and \
           os.path.exists(fname_output):
            sys.exit('ERROR: FILE EXISTS: ' + str(fname_output))
        if fname_output is not None:
            with open(fname_output, 'w') as f_out:
                sys.stdout = f_out
                self.__start()
                sys.stdout = sys.__stdout__
        else:
            self.__start()

    # シミュレーション実行
    def __start(self):
        # シミュレーション設定を表示
        self.__emit_settings()
        # シミュレーターオブジェクトを各プロセスに設定
        for pid in range(self.__nw.get_n()):
            self.__proctbl[pid].set_sim(self)
        # 各プロセスの on_startup() メソッドの呼出 (PIDmap順で)
        for pid in self.__nw.get_pidmap():  # range(self.__nw.get_n())
            self.__proctbl[pid].on_startup()
        # 始動プロセスを起動 (PIDmap順で)
        for ev_pid in self.__nw.get_pidmap():  # range(self.__nw.get_n())
            if ev_pid in self.__initips:
                self.sched_ev_initiator(ev_pid)
        # 事象スクリプト(event script)で指示された事象の生起をスケジュール
        ev_t_prev = -1
        i = 0
        for ev_item in self.__evscript:
            ev_t    = ev_item[0]      # 生起時刻
            ev_pid  = ev_item[1]      # 事象が生起するプロセス識別子
            ev_type = ev_item[2]      # 事象型
            if ev_pid == 'SYS':            # 事象型: システム事象
                ev_msg  = ev_item[3]       # 事象
                self.sched_ev_system(ev_t, ev_msg)
            elif ev_type == 'SEND':        # 事象型: 送信事象
                ev_pid_to = ev_item[3]     # 受信プロセス識別子
                ev_msg    = ev_item[4]     # 事象
                if (len(ev_item) >= 6):
                    ev_delay = ev_item[5]  # メッセージ遅延
                    self.sched_ev_send(ev_t, ev_pid, ev_pid_to, ev_msg, 0,
                                       delay = ev_delay)
                else:
                    self.sched_ev_send(ev_t, ev_pid, ev_pid_to, ev_msg, 0)
            elif ev_type == 'INTERNAL':    # 事象型: 内部事象
                if ev_t_prev == ev_t: # 同時動作をわずかにずらす
                    i += 1
                else:
                    i = 0
                    ev_t_prev = ev_t 
                t_epsilon = i * 10e-5 # ずらし時間(algorithm.pyとの兼ね合い注意)
                ev_t += t_epsilon     # 同時動作をずらす
                ev_msg  = ev_item[3]       # 事象
                self.sched_ev_internal(ev_t, ev_pid, ev_msg)
            else:
                sys.exit('ERROR: Unsupported event tag for event script: ' \
                         + str(ev_type))
        # シミュレーション開始
        # メインループ
        while self.__evq:                 # 事象がなくなれば終了
            ev = heapq.heappop(self.__evq)        # 次に生起する事象の取出
            if not self.__handle_next_event(ev):  # 事象の処理を実行
                break                             # (強制終了の場合あり)
        # シミュレーション終了
        # 各プロセスの on_finish() メソッドの呼出
        for pid in range(self.__nw.get_n()):
            self.__proctbl[pid].on_finish()
        # シミュレーション結果を表示 (統計情報など)
        self.__emit_performacne()

    # シミュレーション設定を表示
    def __emit_settings(self):
        print("ALGORITHM:     {}".format(self.__proctbl[0].get_name()))
        print("NETWORK:       {}".format(self.__nw.get_name()))
        print("NPROCESSES:    {}".format(self.__nw.get_n()))
        print("PIDMAP:        {}".format(self.__nw.get_pidmap()))
        
    # シミュレーション結果を表示
    def __emit_performacne(self):
        print("NMESSAGES:     {}".format(self.__nmsgs))
        print("SIMDURATION:  {:6.2f}".format(self.__curtime))

    # シミュレーション中の 事象(event), 注釈(remark), 診断(diag) など表示
    def emit(self, label, pid, s):
        print("{} {:6.2f} {:2d} {}".format(label, self.__curtime, pid, s))

    # 事象処理
    def __handle_next_event(self, ev):
        ev_t    = ev[0]  # 事象の生起時刻
        ev_seq  = ev[1]  # 事象のシーケンス番号
        ev_pid  = ev[2]  # 事象が生起するプロセス識別子
        ev_type = ev[3]  # 事象型
        ev_msg  = ev[4]  # 事象固有の情報 (メッセージ内容など)
        self.__curtime = ev_t      # 現在時刻を進める
        if (type(ev_pid) is int) \
           and (0 <= ev_pid) and (ev_pid < self.__nw.get_n()):
            # プロセスで生起の事象: event_handler() メソッド呼出
            proc = self.__proctbl[ev_pid]
            proc.event_handler(ev_type, ev_msg)
        elif ev_pid == self.PID_SYS:
            # システム事象: event_handler() メソッド呼出
            if not self.system_event_handler(ev_type, ev_msg):
                return False  # シミュレーションを強制終了
        else:
            sys.exit('ERROR: ILLEGAL PID: ' + str(ev_pid))
        return True

    # __evq に挿入するイベント情報の構造: [T, SEQ, PID, EV_TYPE, EV_ARG]
    #   T       : 事象の生起時刻
    #   SEQ     : 事象のシーケンス番号
    #   PID     : 事象が生起するプロセス識別子
    #   EV_TYPE : 事象型
    #   EV_ARG  : 事象固有の情報

    # 始動プロセスの起動をスケジュール
    def sched_ev_initiator(self, ev_pid):
        self.__evseq += 1
        heapq.heappush(self.__evq,
                       [0.0, self.__evseq, ev_pid, self.EV_INITIATOR, None])

    # 内部事象の生起をスケジュール
    def sched_ev_internal(self, t, ev_pid, evmsg):
        self.__evseq += 1
        heapq.heappush(self.__evq,
                       [t, self.__evseq, ev_pid, self.EV_INTERNAL, evmsg])

    # 内部事象(タイマ)の生起をスケジュール
    def sched_ev_timer(self, t, ev_pid, evmsg):
        self.__evseq += 1
        heapq.heappush(self.__evq,
                       [t, self.__evseq, ev_pid, self.EV_TIMER, evmsg])

    # 受信事象の生起をスケジュール
    def sched_ev_receive(self, t, pid_from, pid_to, msg, msgid):
        self.__evseq += 1
        evmsg = [pid_from, pid_to, msg, msgid]
        heapq.heappush(self.__evq,
                       [t, self.__evseq, pid_to, self.EV_RECEIVE, evmsg])
        self.__nmsgs += 1

    # 送信事象の生起をスケジュール (事象スクリプトでの使用を想定)
    def sched_ev_send(self, t, pid_from, pid_to, msg, msgid, delay=None):
        self.__evseq += 1
        evmsg = [pid_from, pid_to, msg, msgid, delay]
        heapq.heappush(self.__evq,
                       [t, self.__evseq, pid_from, self.EV_SEND, evmsg])

    # システム事象の生起をスケジュール
    def sched_ev_system(self, t, evmsg):
        self.__evseq += 1
        heapq.heappush(self.__evq,
                       [t, self.__evseq, self.PID_SYS, self.EV_SYSTEM, evmsg])

    # システム事象の処理
    def system_event_handler(self, ev_type, ev_msg):
        if ev_msg == 'END':  # シミュレーション強制終了を行う事象
            print("{} {:6.2f}".format("END:    ", self.__curtime))
            return False  
        return True # (それ以外はシミュレーションを継続)
