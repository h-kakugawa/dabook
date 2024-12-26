# クリーク
from network import Network

class NWComplete(Network):
    def __init__(self, n,
                 delay_spec = None,
                 pidmap_spec = None,
                 ordering_spec = None): 
        name = "Complete"
        m = n * (n-1)
        neighbor_spec = [ self.__neighbors(pid, n) for pid in range(n) ]
        super().__init__(name, n, m, neighbor_spec,
                         delay_spec = delay_spec,
                         pidmap_spec = pidmap_spec,
                         ordering_spec = ordering_spec)

    def __neighbors(self, pid, n):
        return [ (i + pid) % n for i in range(1, n) ]

    
