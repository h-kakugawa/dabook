from algorithm import Algorithm
from simulator import Simulator

class LE_CR(Algorithm):

    @staticmethod
    def get_name():
        return 'LE-CR by Chang-Roberts for Leader Election'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.state = 'IDLE'

    def when_initiator(self):
        self.state = 'CAND'
        self.send_to_next(['ID', self.pid])

    def message_handler(self, pid_from, msg):
        [mtype, pid_x] = msg
        if mtype == 'ID':
            if self.state == 'IDLE':
                self.state = 'LOST'
                self.emit_internal('LOST')
            if self.state == 'CAND':
                if pid_x > self.pid:
                    self.state = 'LOST'
                    self.emit_internal('LOST')
                    self.send_to_next(msg)
                elif pid_x == self.pid:
                    self.state = 'LEADER'
                    self.emit_internal('LEADER')
            elif self.state == 'LOST':
                self.send_to_next(msg)

    def send_to_next(self, msg):
        self.send(msg, self.get_neighbors()[0])
