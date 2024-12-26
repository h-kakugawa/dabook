from algorithm import Algorithm
from simulator import Simulator

class WV_P(Algorithm):

    @staticmethod
    def get_name():
        return 'WV-P by Tel for Wave'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.cnt = 0

    def when_initiator(self):
        for pid_j in self.get_neighbors():
            if pid_j != self.pid:
                self.send(['TOKEN'], pid_j)

    def message_handler(self, pid_from, msg):
        [msg_type, *_] = msg
        if msg_type == 'TOKEN': 
            self.send(['REPLY'], pid_from)
        elif msg_type == 'REPLY': 
            self.cnt += 1
            if self.cnt == self.get_n() - 1:
                self.emit_internal('DECIDE')
                self.halt()
