from algorithm import Algorithm
from simulator import Simulator
import sys

INFINITY = sys.maxsize

class MX_L(Algorithm):

    @staticmethod
    def get_name():
        return 'MX-L by Lamport for Mutual Exclusion'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.state = 'OUT'
        self.c = 0
        self.reqt = [ INFINITY for _ in range(self.get_n()) ] 
        self.reps = 0

    def on_internal_event(self, ev_msg):
        if ev_msg == 'REQ-CS':
            self.state = 'TRYING'
            self.c += 1; self.reqt[self.pid] = self.c
            for pid_j in self.get_other_procs():
                self.send(['REQUEST', self.c], pid_j)
            self.reps = 0
        elif ev_msg == 'EXIT-CS':
            self.state = 'OUT'
            self.reqt[self.pid] = INFINITY
            for pid_j in self.get_other_procs():
                self.send(['RELEASE', self.c], pid_j)
                                        
    def message_handler(self, pid_from, msg):
        [mtype, c] = msg
        self.c = max(self.c, c) + 1
        if mtype == 'REQUEST':
            self.reqt[pid_from] = c; self.send(['REPLY', self.c], pid_from)
        elif mtype == 'REPLY':
            self.reps += 1
        elif mtype == 'RELEASE':
            self.reqt[pid_from] = INFINITY
        if (self.state == 'TRYING') \
           and (self.reps == self.get_n() - 1) \
           and all([(  (self.reqt[self.pid], self.pid)
                     < (self.reqt[pid_j],    pid_j))
                    for pid_j in self.get_other_procs()]):
            self.state = 'IN'
            self.emit_internal("ENTER-CS")
            self.reps = 0;
