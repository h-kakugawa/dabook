# 分散アルゴリズム実装のためのテンプレート
from algorithm import Algorithm
from simulator import Simulator

class XXX(Algorithm):   # クラス名

    # The name of algorithm
    @staticmethod
    def get_name():
        return '<CLASS-NAME> by <INVENTOR> for <PROBLEM-NAME>'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        # 局所変数の宣言 & 初期値設定
        self.lvar1 = 'IDLE'
        self.lvar2 = 0
        self.lvar3 = False
        self.lvar4 = { pid: 0 for pid in self.get_allprocs() }
        
    # 使用可能な変数/メソッド
    #     self.pid
    #         - プロセス識別子
    #     self.get_n()
    #         - プロセス数
    #     self.get_neighbors()
    #         - 隣接プロセスの識別子のリスト
    #     self.get_other_procs()
    #         - 自身以外の全プロセスの識別子のリスト
    #     self.get_allprocs()
    #         - 全プロセスの識別子のリスト
    #     self.is_initiator()
    #         - 始動プロセスか否か
    #     self.halt(msg)
    #         - 実行を停止
    #     self.send(msg, pid_to)
    #         - メッセージ msg を識別子 pid_to のプロセスへ送信
    #     self.emit(evstr)
    #         - 事象ログ出力 ('EVENT:' + evstr を出力)
    #     self.emit_remark(evstr)
    #         - 注釈ログ出力 ('REMARK:' + evstr を出力)
    #     self.emit_diag(evstr)
    #         - 診断ログ出力 ('DIAG:' + evstr を出力)

    # 1. 実行開始時に呼び出されるメソッド
    def on_startup(self):
        pass

    # 2. イニシエーターの場合に実行開始時に呼び出されるメソッド
    def when_initiator(self):
        pass

    # 3. 内部事象の発生時に呼び出されるメソッド
    #    ev_msg : 事象内容を表すメッセージ
    def on_internal_event(self, ev_msg):
        if ev_msg == 'XXX':
            pass
        elif ev_msg == 'YYY': 
            pass
        elif ev_msg == 'ZZZ': 
            pass

    # 3. メッセージ到着時に呼び出されるメソッド
    #    pid_from : メッセージの送信元のプロセスの識別子
    #    msg : 受信したメッセージ (単一オブジェクトでも良いが，
    #      リスト [tag, v1, ...] の形のタグと0個以上のパラメータの
    #      形にすることを推奨)
    def message_handler(self, pid_from, msg):
        [mtype, *_] = msg
        if mtype == 'AAA':
            pass
        elif mtype == 'BBB':
            pass
        elif mtype == 'CCC':
            pass

    # 3. タイマー事象発生時に呼び出されるメソッド
    #    ev_msg : 事象内容を表すメッセージ
    def on_timer_event(self, ev_msg):
        pass

    # 4. シミュレーション終了時に呼び出されるメソッド
    def on_finish(self):
        pass
