# グリッド (grid) コータリー
from coterie import Coterie
import math

class GridCoterie(Coterie):
    def make_quorum(self, i):
        m = math.ceil(math.sqrt(self.n))
        x = i %  m
        y = i // m
        q_hor = { (k + y * m) % self.n  for k in range(m) }
        q_ver = { (x + k * m) % self.n  for k in range(m) }
        return q_hor | q_ver
