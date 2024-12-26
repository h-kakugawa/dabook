# DIMACSフォーマットファイル読み込み (無向グラフ限定)
import sys
import re
from network import Network
from dimacs import DIMACS

class NWFile(Network):
    def __init__(self, fname,
                 delay_spec = None,
                 pidmap_spec = None,
                 ordering_spec = None):
        name = "File-" + fname
        self.__adj = None
        d = DIMACS(fname)
        n = d.get_n()
        m = 2 * d.get_m()
        neighbor_spec = [ self.__neighbors(d.get_edges(), pid, n)
                          for pid in range(n) ]
        super().__init__(name, n, m, neighbor_spec, 
                         delay_spec = delay_spec,
                         pidmap_spec = pidmap_spec,
                         ordering_spec = ordering_spec)
        self.set_weight(d.get_wedges())

    def __neighbors(self, e, pid, n):
        s1 = [ pid_dst for (pid_src, pid_dst) in e if pid_src == pid ] 
        s2 = [ pid_src for (pid_src, pid_dst) in e if pid_dst == pid ] 
        return list(set(s1 + s2))
