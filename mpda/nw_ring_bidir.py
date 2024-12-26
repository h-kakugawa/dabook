# 双方向リング
from network import Network

class NWRingBidir(Network):
    def __init__(self, n, delay_spec = None, pidmap_spec = None):
        name = "Bidirectional-Ring"
        m = 2*n
        neighbor_spec = [ self.__neighbors(pid, n) for pid in range(n) ]
        super().__init__(name, n, m, neighbor_spec,
                         delay_spec = delay_spec, pidmap_spec = pidmap_spec)

    def __neighbors(self, pid, n):
        return [ (pid + 1) % n, 
                 (pid - 1) % n ]
