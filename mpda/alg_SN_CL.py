from simulator import Simulator
from algorithm import Algorithm
from alg_sn_basic import SN_Basic

class SN_CL(Algorithm):

    @staticmethod
    def get_name():
        return "SN-CL by Chandy & Lamport for Snapshot"

    def __init__(self, pid, nw, bas_alg):
        super().__init__(pid, nw)
        self.taken = False
        self.lstate = None
        self.mkr  = { pid: False for pid in self.get_neighbors() } 
        self.msgs = { pid: [ ]   for pid in self.get_neighbors() } 
        self.bas_alg = bas_alg  # 基本アルゴリズム

    def on_startup(self):
        self.bas_alg.on_startup()

    def on_internal_event(self, ev_msg):
        if ev_msg == 'SNAPSHOT': # スナップショット開始の内部事象
            self.taken = True; 
            self.lstate = self.bas_alg.take_local_state()
            self.emit_internal('RECORD')
            for pid_j in self.get_neighbors():
                self.send(['MARKER'], pid_j)
        else: # 基本アルゴリズムの内部事象
            self.bas_alg.on_internal_event(ev_msg)

    def message_handler(self, pid_from, msg):
        [msg_type, *_] = msg
        if msg_type == 'MARKER': # スナップショットのメッセージ
            self.mkr[pid_from] = True
            if not self.taken:
                self.taken = True;
                self.lstate = self.bas_alg.take_local_state()
                self.emit_internal('RECORD')
                for pid_j in self.get_neighbors():
                    self.send(['MARKER'], pid_j)
            if all([self.mkr[pid] for pid in self.get_neighbors()]):
                self.emit_remark("LOCAL-STATE: " + str(self.lstate))
                self.emit_remark("EXTRA-MESSAGES: " + str(self.msgs))
                ml = str(self.lstate).replace(' ', '_') 
                mm = str(self.msgs).replace(': ', ':')
                self.emit_internal('DONE: ' + ml + ' / ' + mm)
        else: # 基本アルゴリズムのメッセージ
            if self.taken and not self.mkr[pid_from]:
                self.msgs[pid_from].append(msg)
            self.bas_alg.message_handler(pid_from, msg)

    def send(self, msg, pid_to, delay = None):
        [mtype, *_] = msg
        if mtype == 'MARKER':
            super().send(msg, pid_to, delay = delay)
        else:
            self.bas_alg.send(msg, pid_to, delay = delay)
