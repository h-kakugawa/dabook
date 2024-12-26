from algorithm import Algorithm
from simulator import Simulator

class LE_L(Algorithm):

    @staticmethod
    def get_name():
        return 'LE-L by LeLann for Leader Election'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.state = 'IDLE'
        self.pset = [ ]

    def when_initiator(self):
        self.state = 'CAND'
        self.pset = [ self.pid ]
        self.send_to_next(['ID', self.pid])

    def message_handler(self, pid_from, msg):
        [mtype, pid_x] = msg
        if mtype == 'ID':
            if self.state == 'IDLE':
                self.state = 'LOST'
                self.emit_internal('LOST')
            if self.state == 'CAND':
                if pid_x != self.pid:
                    self.pset.append(pid_x)
                    self.send_to_next(['ID', pid_x])
                elif pid_x == self.pid:
                    if self.pid == max(self.pset):
                        self.state = 'LEADER'
                        self.emit_internal('LEADER')
                    else:
                        self.state = 'LOST'
                        self.emit_internal('LOST')
            elif self.state == 'LOST':
                self.send_to_next(['ID', pid_x])

    def send_to_next(self, msg):
        self.send(msg, self.get_neighbors()[0])
