from algorithm import Algorithm
from simulator import Simulator

class MX_RA(Algorithm):

    @staticmethod
    def get_name():
        return 'MX-RA by Ricart & Agrawala for Mutual Exclusion'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.state = 'OUT'
        self.c = 0
        self.seqn = 0
        self.reps = 0
        self.deff = { p: False for p in self.get_allprocs() }

    def on_internal_event(self, ev_msg):
        if ev_msg == 'REQ-CS':
            self.state = 'TRYING'
            self.c += 1; self.seqn = self.c
            for pid_j in self.get_other_procs():
                self.send(['REQUEST', self.c], pid_j)
            self.reps = 0
        elif ev_msg == 'EXIT-CS':
            self.state = 'OUT'
            for pid_j in self.get_other_procs():
                if self.deff[pid_j]:
                    self.deff[pid_j] = False;
                    self.send(['REPLY', self.c], pid_j)
                                        
    def message_handler(self, pid_from, msg):
        [mtype, c] = msg
        self.c = max(self.c, c) + 1
        if mtype == 'REQUEST':
            if (self.state == 'TRYING' or self.state == 'IN') \
               and ([c, pid_from] > [self.seqn, self.pid]):
                self.deff[pid_from] = True
            else:
                self.send(['REPLY', self.c], pid_from)
        elif mtype == 'REPLY':
            self.reps += 1
        if (self.state == 'TRYING') and (self.reps == self.get_n()-1):
            self.state = 'IN'
            self.emit_internal("ENTER-CS")
            self.reps = 0
