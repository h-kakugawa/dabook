# 各プロセスのアルゴリズム記述のためのクラス
from process_if import ProcessIf
from simulator import Simulator
from network import Network
import copy
import sys

class Algorithm(ProcessIf):

    # メッセージ識別子
    msgid_next = 0  

    # アルゴリズム名称の文字列 (表示用)
    def get_name(self):
        return "(no name)" 

    def __init__(self, pid, nw): 
        self.__procstat = 'IDLE'  # プロセス状態 (IDLE/ACTIVE/PASSIVE/HALT)
        self.pid = pid            # プロセスID
        self.nw = nw              # ネットワーク
        self.__initiator = False  # 始動プロセスか否か
        self.__neighbors = nw.get_neighbors(pid)   # 隣接プロセス集合
        self.__allprocs  = nw.get_allprocs()       # 全プロセス
        self.sim = None           # シミュレーターオブジェクト
        
    # プロセスID
    def get_pid(self):
        return self.pid
    
    # プロセス数
    def get_n(self):
        return self.nw.get_n()

    # 隣接プロセスの集合
    def get_neighbors(self):
        return self.__neighbors

    # 他プロセスすべての集合
    def get_other_procs(self):
        return self.nw.get_other_procs(self.pid)
    
    # 全プロセスの集合
    def get_allprocs(self):
        return self.nw.get_allprocs()

    # シミュレーターオブジェクト設定
    def set_sim(self, sim):
        self.__sim = sim

    # 事象ハンドラ
    def event_handler(self, ev_type, ev_msg):
        if self.__procstat == 'PASSIVE' or self.__procstat == 'IDLE':
            self.__procstat = 'ACTIVE'
            # Event on a running process
            if ev_type == Simulator.EV_INITIATOR: 
                self.emit_remark("INITIATOR")
                self.__initiator = True
                self.when_initiator()
            elif ev_type == Simulator.EV_TIMER: 
                self.emit_remark("TIMER")
                self.on_timer_event(ev_msg)
            elif ev_type == Simulator.EV_INTERNAL: 
                self.emit_internal("{}".format(ev_msg))
                self.on_internal_event(ev_msg)
            elif ev_type == Simulator.EV_RECEIVE: 
                pid_from = ev_msg[0]
                pid_to   = ev_msg[1]
                msg      = ev_msg[2]
                msgid    = ev_msg[3]
                self.emit("RECV {:>2d} {:>2d}  {} {:3d}"
                          .format(pid_from, self.pid, msg, msgid))
                self.message_handler(pid_from, msg)
            elif ev_type == Simulator.EV_SEND: 
                pid_from = ev_msg[0]
                pid_to   = ev_msg[1]
                msg      = ev_msg[2]
                msgid    = ev_msg[3]
                delay    = ev_msg[4]
                self.send(msg, pid_to, delay = delay)
            else:
                sys.exit("INTERNAL ERROR: UNKNOWN ev_type {}".format(ev_type))
            self.__procstat = 'PASSIVE'
        else:
            # 停止プロセスで事象の発生には要注意
            if ev_type == Simulator.EV_RECEIVE: 
                self.emit_diag("MESSAGE-TO-HALTED-PROCESS: " 
                               + "RECV {:>2d} {:>2d} {}"
                               .format(ev_msg[0], ev_msg[1], ev_msg[2]))
            else:
                self.emit_diag("EVENT-ON-HALTED-PROCESS: {}".format(ev_type))

    # プロセスを停止
    def halt(self, msg=''):
        self.emit_remark("HALT {}".format(msg))
        self.__procstat = 'HALT'

    # 始動プロセスか否か
    def is_initiator(self):
        return self.__initiator

    # プロセス起動時に呼び出し
    def on_startup(self):
        pass

    # 始動プロセスの場合に呼び出し
    def when_initiator(self):
        pass

    # 内部事象ハンドラ
    def on_internal_event(self, ev_msg):
        pass

    # 周期事象ハンドラ
    def on_timer_event(self, ev_msg):
        pass

    # メッセージハンドラ
    def message_handler(self, pid_from, msg):
        pass

    # シミュレーション終了時に呼び出し
    def on_finish(self):
        pass

    # 送信本体
    def __send(self, msg, pid_to, delay = None):
        if list(msg):
            msg = copy.deepcopy(msg)
        Algorithm.msgid_next += 1
        msgid = Algorithm.msgid_next
        if delay is None: 
            delay = self.nw.get_delay(self.pid, pid_to)
        elif (type(delay) is not int and
              type(delay) is not float) or \
             (delay < 1e-4):
            sys.exit('ERROR: ILLEGAL VALUE FOR MESSAGE DELAY: ' + str(delay))
        #t_epsilon = 0
        t_epsilon = abs(pid_to - self.pid) * 1e-7 # スッキリ時空ダイアグラムに
        t_arrive = self.__sim.get_time() + delay + t_epsilon
        pid_from = self.pid
        self.emit("SEND {:>2d} {:>2d}  {} {:>3d} {:6.2f} {:6.2f}"
                  .format(pid_from, pid_to, msg, msgid, delay, t_arrive))
        self.__sim.sched_ev_receive(t_arrive, pid_from, pid_to, msg, msgid)

    # メッセージの送信
    def send(self, msg, pid_to, delay = None):
        self.__send(msg, pid_to, delay)

    # (実行ログ出力) 事象 
    def emit(self, evstr):
        self.__sim.emit('EVENT:  ', self.pid, evstr)

    # (実行ログ出力) 内部事象
    def emit_internal(self, evstr):
        self.__sim.emit('EVENT:  ', self.pid, 'INTERNAL ' + evstr)

    # (実行ログ出力) 注釈
    def emit_remark(self, evstr):
        self.__sim.emit('REMARK: ', self.pid, evstr)

    # (実行ログ出力) 診断メッセージ
    def emit_diag(self, evstr):
        self.__sim.emit('DIAG:   ', self.pid, evstr)
