# TD_CR: 終了判定アルゴリズム  (債権回収)
# 債権の分割/回収において演算誤差を避けるため，債権値は
# 2進数表現での何ビット目かで表現する．
# 具体的には，債権値 2**{-k} を cred = k で表す．
# P0 の債権の初期値 1 = 2^0 は cred = 0 で表現する．
from simulator import Simulator
from algorithm import Algorithm
from alg_if_td import AlgorithmTerminationDetectionIf

class TD_CR(Algorithm, AlgorithmTerminationDetectionIf):
    
    pid_0 = 0

    @staticmethod
    def get_name():
        return 'TD-M, known as Credit Recovery Algorithm, ' \
            + 'by Mattern for Termination Detection'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.state = 'PASSIVE'
        self.cred = 0 if self.pid == 0 else None
        self.ret = set()

    def td_when_initiator(self, app): 
        self.emit_internal('ACTIVE')
        self.state = 'ACTIVE'
        app.when_initiator()
        self.emit_internal('PASSIVE')
        self.state = 'PASSIVE'
        self.collect(self.cred)
        self.cred = 0
            
    def td_message_handler(self, app, pid_from, msg):
        [mtype, *_] = msg
        if mtype == 'BASIC':
            [_, c, m] = msg
            self.emit_remark("C={}".format(c))
            self.cred = c
            self.emit_internal('ACTIVE')
            self.state = 'ACTIVE'
            app.message_handler(pid_from, m)
            self.emit_internal('PASSIVE')
            self.state = 'PASSIVE'
            if app.is_initiator():
                self.collect(self.cred)
            else:
                self.send(['RETURN', self.cred], self.pid_0)
            self.cred = None
        elif mtype == 'RETURN':
            [_, c] = msg
            self.emit_remark("RETURN={}".format(c))
            self.collect(c)

    def td_send(self, app, msg, pid_to, delay = None): 
        c = self.cred + 1
        app.send(['BASIC', c, msg], pid_to, delay = delay)
        self.cred += 1

    def collect(self, c):
        while c in self.ret:
            self.ret.remove(c)
            c -= 1
        self.ret.add(c)
        self.emit_remark("RETURN={}".format(self.ret))
        if self.ret == {0}:  # 回収完了
            self.emit_internal('DETECTED')
