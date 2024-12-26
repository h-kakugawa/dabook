from algorithm import Algorithm
from simulator import Simulator

class WV_E(Algorithm):

    @staticmethod
    def get_name():
        return "WV-E (Echo Algorithm) by Chang for Wave"

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.cnt = 0
        self.par = None

    def when_initiator(self):
        for pid_j in self.get_neighbors():
            self.send(['TOKEN'], pid_j)

    def message_handler(self, pid_from, msg):
        [msg_type, *_] = msg
        if msg_type == 'TOKEN': 
            self.cnt += 1
            if self.is_initiator():
                if self.cnt == len(self.get_neighbors()):
                    self.emit_internal('DECIDE')
                    self.halt()
            else:
                if self.par == None:
                    self.par = pid_from
                    for pid_j in self.get_neighbors():
                        if pid_j != self.par:
                            self.send(['TOKEN'], pid_j)
                else:
                    if self.cnt == len(self.get_neighbors()):
                        self.send(['TOKEN'], self.par)
