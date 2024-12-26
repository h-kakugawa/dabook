from algorithm import Algorithm
from simulator import Simulator

class LC_VC(Algorithm):

    @staticmethod
    def get_name():
        return 'LC-VC by Fidge, Mattern, and Schmuck for vector logical clock'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.vc = { pid: 0 for pid in range(self.get_n()) }  # 時計値

    # 時計値
    def get_value(self):
        return self.vc

    # 内部事象発生時
    def tick(self):
        self.vc[self.pid] += 1

    # メッセージ送信時
    def send(self, m, pid_to, delay=None):
        msg = ['VClock', self.vc, m]
        super().send(msg, pid_to, delay)

    # メッセージ到着時
    def message_received(self, msg):
        [mtype, vc, m] = msg
        if mtype == 'VClock':
            for pid_j in range(self.get_n()):
                self.vc[pid_j] = max(self.vc[pid_j], vc[pid_j])
            self.vc[self.pid] += 1
