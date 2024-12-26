# グリッド
from network import Network
import re

class NWGrid(Network):
    def __init__(self, size,
                 delay_spec = None,
                 pidmap_spec = None,
                 ordering_spec = None):
        # size: "AxB" 形式の文字列 (例: "5x4")
        name = "Grid-" + size
        self.__adjlist = None
        (nw, nh, n, m) = self.__grid(size)
        super().__init__(name, n, m, self.__adjlist,
                         delay_spec = delay_spec,
                         pidmap_spec = pidmap_spec,
                         ordering_spec = ordering_spec)
        
    def __grid(self, size):
        # "AxB" 形式の文字列 (例: "5x4") を解析
        reg = re.compile(r'(\d+)[xX](\d+)')
        rem = reg.search(size)
        nw = int(rem.group(1))
        nh = int(rem.group(2))
        n = nw * nh
        # 辺を列挙して隣接プロセス集合を構成
        m = 0;
        self.__adjlist = [ [] for pid_i in range(n) ] 
        for e_y in range(nh):
            for e_x in range(nw - 1):
                pid_i = e_y * nw + (e_x + 0)
                pid_j = e_y * nw + (e_x + 1)
                self.__adjlist[pid_i].append(pid_j)
                self.__adjlist[pid_j].append(pid_i)
                m += 2
        for e_x in range(nw):
            for e_y in range(nh - 1): 
                pid_i = (e_y + 0) * nw + e_x 
                pid_j = (e_y + 1) * nw + e_x 
                self.__adjlist[pid_i].append(pid_j)
                self.__adjlist[pid_j].append(pid_i)
                m += 2
        for pid in range(n):
            self.__adjlist[pid].sort()
        return (nw, nh, n, m)
