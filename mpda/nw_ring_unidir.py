# 単方向リング
from network import Network

class NWRingUnidir(Network):
    def __init__(self, n, delay_spec = None, pidmap_spec = None):
        name = "Unidirectional-Ring"
        m = n
        neighbor_spec = [ self.__neighbor_spec(pid, n) for pid in range(n) ]
        super().__init__(name, n, m, neighbor_spec,
                         delay_spec = delay_spec, pidmap_spec = pidmap_spec)
            
    def __neighbor_spec(self, pid, n):
        return [ (pid + 1) % n ]
