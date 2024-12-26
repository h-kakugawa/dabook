from algorithm import Algorithm
from simulator import Simulator

class MX_SK(Algorithm):

    @staticmethod
    def get_name():
        return 'MX-SK by Suzuki & Kasami for Mutual Exclusion'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.state = 'OUT'
        self.priv = False if (self.pid != 0) else True
        self.waitq = [ ]
        self.rn = { pid: -1 for pid in self.get_allprocs() } 
        self.ln = { pid: -1 for pid in self.get_allprocs() }

    def on_internal_event(self, ev_msg):
        if ev_msg == 'REQ-CS':
            if self.priv:
                self.state = 'IN'
                self.emit_internal("ENTER-CS")
            else:
                self.state = 'TRYING'
                self.rn[self.pid] += 1
                for pid_j in self.get_other_procs():
                    self.send(['REQUEST', self.rn[self.pid]], pid_j)
        elif ev_msg == 'EXIT-CS': 
            self.state = 'OUT'
            self.ln[self.pid] = self.rn[self.pid]
            for pid_j in self.get_allprocs():
                if pid_j != self.pid:
                    if (pid_j not in self.waitq) \
                       and (self.rn[pid_j] == self.ln[pid_j] + 1):
                        self.waitq.append(pid_j)
            if self.waitq:
                pid_to = self.waitq.pop(0)
                self.priv = False
                self.send(['PRIVILEGE', self.waitq, self.ln], pid_to)
                self.waitq = [ ]

    def message_handler(self, pid_from, msg):
        [mtype, *_] = msg
        if mtype == 'REQUEST':
            [_, r] = msg
            self.rn[pid_from] = max(self.rn[pid_from], r)
            if self.priv and (self.state == 'OUT'):
                if self.rn[pid_from] == self.ln[pid_from] + 1:
                    self.priv = False
                    self.send(['PRIVILEGE', self.waitq, self.ln], pid_from)
                    self.waitq = [ ]

        elif mtype == 'PRIVILEGE':
            [_, q, l] = msg
            self.state = 'IN'
            self.emit_internal("ENTER-CS")
            self.priv = True
            self.waitq = q
            self.ln = l
