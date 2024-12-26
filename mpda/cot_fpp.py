# 有限射影平面 (finite projective plane) コータリー
import sys
import math
from coterie import Coterie

class FppCoterie(Coterie):
    c3k2 = [ {0,1}, {1,2}, {0,2} ]
    c7k3 = [ {0,1,2}, {1,3,5}, {2,4,5},
             {0,3,4}, {1,4,6}, {0,5,6},
             {2,3,6} ]
    c13k4 = [ {0,1,2,3}, {1,4,7,10}, {2,5,7,12},
              {3,5,9,10}, {0,4,5,6}, {1,5,8,11},
              {1,6,9,12}, {0,7,8,9}, {2,6,8,10},
              {2,4,9,11}, {0,10,11,12}, {3,6,7,11},
              {3,4,8,12} ]
    c21k5 = [ {0,1,2,3,4}, {1,5,9,13,17}, {2,6,9,15,20},
              {3,6,12,13,19}, {4,6,11,16,17}, {0,5,6,7,8},
              {1,6,10,14,18}, {1,7,11,15,19}, {1,8,12,16,20},
              {0,9,10,11,12}, {2,5,10,16,19}, {2,8,11,13,18},
              {2,7,12,14,17}, {0,13,14,15,16}, {3,5,11,14,20},
              {3,8,10,15,17}, {3,7,9,16,18}, {0,17,18,19,20},
              {4,5,12,15,18}, {4,8,9,14,19}, {4,7,10,13,20} ]

    def make_quorum(self, i):
        c = { }
        if self.n < 3:
            c = { (k % self.n) for k in self.c3k2[i] }
        elif self.n == 3:
            c = self.c3k2[i]
        elif self.n < 7:
            c = { (k % self.n) for k in self.c7k3[i] }
        elif self.n == 7:
            c = self.c7k3[i]
        elif self.n < 13:
            c = { (k % self.n) for k in self.c13k4[i] }
        elif self.n == 13:
            c = self.c13k4[i]
        elif self.n < 21:
            c = { (k % self.n) for k in self.c21k5[i] }
        elif self.n == 21:
            c = self.c21k5[i]
        else:
            sys.exit('ERROR: FPP COTERIE, TOO LARGE N: ' + str(self.n))
        return c
