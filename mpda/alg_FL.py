# フラディング (一般ネットワーク)
from algorithm import Algorithm
from simulator import Simulator

class FL(Algorithm):

    @staticmethod
    def get_name():
        return "FL for Flooding"

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.done = False

    def when_initiator(self):
        self.done = True
        for pid_j in self.get_neighbors():
            self.send(['FLOOD'], pid_j)

    def message_handler(self, pid_from, msg):
        [mtype, *_] = msg
        if mtype == 'FLOOD':
            if not self.done:
                self.done = True
                for pid_j in self.get_neighbors():
                    if pid_j != pid_from:
                        self.send(['FLOOD'], pid_j)
