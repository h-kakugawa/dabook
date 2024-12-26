from algorithm import Algorithm
from simulator import Simulator

class LE_P(Algorithm):

    @staticmethod
    def get_name():
        return 'LE-P by Peterson for Leader Election'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.state = 'IDLE'
        self.cid  = None
        self.nid  = None
        self.nnid = None

    def when_initiator(self):
        self.state = 'CAND'
        self.cid = self.pid
        self.send_to_next(['NID', self.cid])

    def message_handler(self, pid_from, msg):
        [mtype, pid_x] = msg
        if self.state == 'IDLE':
            self.state = 'LOST'
            self.emit_internal('LOST')
        if self.state == 'CAND':
            if mtype == 'NID':
                if pid_x == self.pid:
                    self.elected()
                else:
                    self.nid = pid_x
                    self.send_to_next(['NNID', self.nid])
            elif mtype == 'NNID':
                self.nnid = pid_x
                if (self.nnid < self.nid) and (self.nid > self.cid):
                    self.cid = self.nid
                    self.send_to_next(['NID', self.cid])
                else:
                    self.state = 'RELAY'
                    self.emit_internal('RELAY')
        elif self.state == 'RELAY':
            if mtype == 'NID' and pid_x == self.pid:
                self.elected()
            else:
                self.send_to_next(msg)
        elif self.state == 'LOST':
            self.send_to_next(msg)

    def elected(self):
        self.state = 'LEADER'
        self.emit_internal('LEADER')

    def send_to_next(self, msg):
        self.send(msg, self.get_neighbors()[0])
