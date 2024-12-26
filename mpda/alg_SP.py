from algorithm import Algorithm
from simulator import Simulator

class SP(Algorithm):

    @staticmethod
    def get_name():
        return "SP for shortest path tree"

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.cost = None
        self.par = None

    def when_initiator(self):
        self.par = self.pid
        self.cost = 0
        self.emit_internal('COST')
        self.emit_remark('COST: {}'.format(self.cost))
        for pid_j in self.get_neighbors():
            self.send(['COST', self.cost], pid_j)

    def message_handler(self, pid_from, msg):
        [mtype, *_] = msg
        if mtype == 'COST':
            [_, c] = msg
            lc = self.nw.get_weight(pid_from, self.pid)
            xc = c + lc
            if self.par is None or xc < self.cost:
                self.par = pid_from
                self.cost = xc
                self.emit_internal('COST')
                self.emit_remark('COST: {}'.format(self.cost))
                for pid_j in self.get_neighbors():
                    if pid_j != pid_from:
                        self.send(['COST', self.cost], pid_j)
