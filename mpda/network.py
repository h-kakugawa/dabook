# ネットワーク
from pidmap import PIDMap
import sys
import re
import pprint

class Network():

    default_link_weight = 1  # デフォルトのリンク重み

    def __init__(self, name, n, m, neighbor_spec,
                 delay_spec = None,
                 pidmap_spec = None,
                 ordering_spec = None):
        self.__name = name         # ネットワーク名称
        self.__n = n               # プロセス数
        self.__m = m               # リンク数
        self.__neighbor = [[] for pid in range(n)]
                                   # (プロセスごと) 隣接プロセス集合
        self.__weight = None       # (プロセスごと) リンク重み
        self.__delay_spec = delay_spec  # リンクの伝送遅延
        self.__pidmap = None            # PIDマップ
        self.__ns(n, pidmap_spec, neighbor_spec)
        for pid in range(n):
            self.__neighbor[pid] \
                = Network.reorder(self.__neighbor[pid], pid, \
                                  ordering_spec = ordering_spec)

    # ネットワーク名称
    def get_name(self):
        return self.__name

    # プロセス数 (頂点数)
    def get_n(self):
        return self.__n

    # リンク数 (辺数)
    def get_m(self):
        return self.__m

    # (プロセスの)隣接プロセス集合
    def get_neighbors(self, pid):
        return self.__neighbor[pid]

    # 他プロセスすべての集合
    def get_other_procs(self, pid):
        return [pid_j for pid_j in self.__neighbor[pid] if pid_j != pid]

    # 全プロセス集合
    def get_allprocs(self):
        return [pid_j for pid_j in range(self.__n)]

    # PIDマップ
    # PIDマップって何?  プロセス識別子のつけかえを行う仕組み．
    #     リングネットワーク等でプロセス識別子の配置の変更を実現可能とする．
    #     (非完全グラフで有用. 完全グラフでは無用)
    def get_pidmap(self):
        return [self.__pidmap.map(pid) for pid in range(self.__n)]

    # (PIDマップによる) 隣接プロセス集合の再設定
    def __ns(self, n, pidmap_spec, neighbor_spec):
        self.__pidmap = PIDMap(n, pidmap_spec)
        for pid in range(self.__n):
            xpid       =   self.__pidmap.map(pid)
            xneighbors = [self.__pidmap.map(pid)
                          for pid in neighbor_spec[pid]] 
            self.__neighbor[xpid] = xneighbors

    # リンク遅延
    def get_delay(self, pid_from, pid_to):
        delay = self.default_link_weight  # デフォルト遅延値
        if self.__delay_spec is None:
            pass
        elif self.__delay_spec == 'default':
            pass
        elif self.__delay_spec == 'link-weight':
            delay = self.get_weight(pid_from, pid_to)
        elif self.__delay_spec == 'id':
            delay = 1.0 + pid_to
        elif type(self.__delay_spec) is int \
             or type(self.__delay_spec) is float:
            delay = self.__delay_spec
        return delay

    # リンク重み設定
    def set_weight(self, wlinks):
        self.__weight = [[] for pid in range(self.__n)]
        for e in wlinks:
            (u, v, w) = e
            self.__weight[u].append([v, w])
            self.__weight[v].append([u, w])

    # リンク重み
    def get_weight(self, pid_from, pid_to,
                   default_weight = default_link_weight):
        if self.__weight is None:  # 未設定
            return default_weight 
        for vw in self.__weight[pid_from]:
            (v, w) = vw
            if v == pid_to:
                return w
        return default_weight

    # 隣接プロセスのリスト内の順序を変更
    @classmethod
    def reorder(self, neighbors, pid, ordering_spec = None):
        if ordering_spec is None:
            # そのまま
            return neighbors
        elif ordering_spec == 'sorted-ascend' or ordering_spec == 'sorted':
            # 昇順
            return sorted(neighbors)
        elif ordering_spec == 'sorted-descend':
            # 降順
            return sorted(neighbors, reverse=True)
        elif ordering_spec == 'tsd-friendly':
            # 時空ダイアグラムでメッセージ線の重なり少ない順序
            # (時空ダイアグラム上で P0,P1,P2,... の順を仮定)
            p_above = []; p_below = []
            for i in neighbors:
                if i <= pid:
                    p_above.append(i)
                else:
                    p_below.append(i)
            return sorted(p_above) + sorted(p_below, reverse=True)

    # (デバッグ用) 内容表示
    def dump(self):
        pp = pprint.PrettyPrinter()
        print(self.__name)
        print('n =', self.__n)
        print('m =', self.__m)
        pp.pprint(self.get_pidmap())
        adj = [self.get_neighbors(pid) for pid in range(self.__n)]
        pp.pprint(adj)
        pp.pprint(self.__weight)
