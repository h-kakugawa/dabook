from algorithm import Algorithm
from simulator import Simulator

class LC_SC(Algorithm):

    @staticmethod
    def get_name():
        return 'LC-SC by Lamport for scalar logical clock'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.c = 0        # 時計値

    # 時計値
    def get_value(self):
        return self.c

    # 内部事象発生時
    def tick(self):
        self.c += 1

    # メッセージ送信時
    def send(self, m, pid_to, delay = None):
        msg = ['SClock', self.c, m]
        super().send(msg, pid_to, delay)

    # メッセージ到着時
    def message_received(self, msg):
        [mtype, c, m] = msg
        if mtype == 'SClock':
            self.c = max(self.c, c) + 1
