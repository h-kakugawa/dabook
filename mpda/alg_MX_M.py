from algorithm import Algorithm
from simulator import Simulator
from cot_fpp import FppCoterie
import heapq

class MX_M(Algorithm):

    @staticmethod
    def get_name():
        return 'MX-M by Maekawa for Mutual Exclusion'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.quorum = FppCoterie(self.get_n()).get_quorum(self.pid)
        self.state = 'OUT'
        self.c = 0
        self.reply  = { pid: None  for pid in self.quorum }
        self.waitpq = [ ]
        self.locked = None
        self.inq = None
        self.relinq = { pid: False for pid in self.nw.get_allprocs() }
        
    def on_startup(self):
        self.emit_remark("QUORUM {}".format(self.quorum))

    def on_internal_event(self, ev_msg):
        if ev_msg == 'REQ-CS':
            self.c += 1
            self.state = 'TRYING'
            for pid_j in self.quorum:
                self.send(['REQUEST', self.c], pid_j)
        elif ev_msg == 'EXIT-CS': 
            self.state = 'OUT'
            for pid_j in self.quorum:
                self.send(['RELEASE', self.c], pid_j)
                self.reply[pid_j] = None

    def message_handler(self, pid_from, msg):
        [mtype, c] = msg
        self.c = max(self.c, c) + 1
        if mtype == 'LOCKED':
            self.reply[pid_from] = 'LOCKED'
            if all( [ (self.reply[pid_j] == 'LOCKED')
                      for pid_j in self.quorum ] ):
                self.state = 'IN'
                self.emit_internal("ENTER-CS")
        elif mtype == 'FAILED':
            self.reply[pid_from] = 'FAILED'
            for pid_j in self.get_allprocs():
                if self.relinq[pid_j]:
                    self.relinq[pid_j] = False
                    self.reply[pid_j] = None
                    self.send(['RELINQUISH', self.c], pid_j)
        elif mtype == 'INQUIRE':
            if self.reply[pid_from] == 'LOCKED':
                if any([self.reply[pid_j] == 'FAILED'
                        for pid_j in self.quorum]):
                    self.reply[pid_from] = None
                    self.send(['RELINQUISH', self.c], pid_from)
                else:
                    self.relinq[pid_from] = True
        elif mtype == 'REQUEST':
            req = [c, pid_from]
            if self.locked is None:
                self.locked = req
                self.send(['LOCKED', self.c], pid_from)
            else:
                heapq.heappush(self.waitpq, req)
                if (req > self.locked) \
                   or (self.waitpq and (req > self.waitpq[0])):
                    self.send(['FAILED', self.c], pid_from)
                elif self.inq is None:
                    self.inq = self.locked
                    [_, pid_j] = self.locked
                    self.send(['INQUIRE', self.c], pid_j)
        elif mtype == 'RELINQUISH':
            self.inq = None
            heapq.heappush(self.waitpq, self.locked)
            self.locked = heapq.heappop(self.waitpq)
            [_, pid_j] = self.locked
            self.send(['LOCKED', self.c], pid_j)
            self.send(['FAILED', self.c], pid_from)
        elif mtype == 'RELEASE':
            self.locked = None
            self.inq = None
            if self.waitpq:
                self.locked = heapq.heappop(self.waitpq)
                [_, pid_j] = self.locked
                self.send(['LOCKED', self.c], pid_j)
    
