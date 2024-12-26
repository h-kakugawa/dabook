# 多数決 (majority) コータリー
from coterie import Coterie

class MajorityCoterie(Coterie):
    def make_quorum(self, i):
        if (self.n % 2) == 1:
            h = (self.n + 1) // 2
            q = { (k + i) % self.n  for k in range(h) }
        else:
            h = (self.n // 2)
            q = { (i + k) % self.n  for k in range(h+1) }
        return q
