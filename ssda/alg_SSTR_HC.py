# SSTR_HC
# Self-stabilizing spanning tree
# by Huang and Chen (IPL 1992)
# 元論文と本原稿との違い
#   元論文: level, 本原稿: dist
#   元論文: levelの値が 1,2,...,n, 本原稿: 0,1,...,n-1

from alg_SS import SS_Algorithm
import sys
import random

class SSTR_HC(SS_Algorithm):
    @staticmethod
    def get_name():
        return 'SSTR_HC by Huang and Chen for self-stabilizing spanning tree'

    # 根プロセスか否か
    isroot = False
    # 局所変数
    par = None
    dist = None
    # 補助変数 (定数)
    n = None   # 総プロセス数
    
    # 局所変数の初期化
    def init_local_state(self, how_init):
        self.n = len(self.procs)
        pid_root = self.n - 1  # 根プロセス: 最大識別子
        if ((type(how_init) is str) and (how_init == 'zero')): # ゼロ
            self.par  = self.neighbors[0]
            self.dist = 0
        elif ((type(how_init) is str) and (how_init == 'random')) \
             or (how_init == None): # ランダム
            r = random.randint(0, len(self.neighbors)-1)
            self.par  = self.neighbors[r]
            self.dist = random.randint(1, self.n-1)
        elif (type(how_init) is list): # 指定値
            self.par  = how_init[self.pid][0]
            self.dist = how_init[self.pid][1]
        else:
            print("ERROR: UNKNOWN INITIALIZATION METHOD {}".format(how_init))
            sys.exit(1)
        # 根プロセスの場合は固定値
        if self.pid == pid_root:
            self.isroot = True
            self.par    = self.pid
            self.dist   = 0

    # 局所変数
    def state(self):
        return [self.par, self.dist]

    # 自己安定分散アルゴリズム  本体
    def guarded_command(self, action):
        # 規則1:
        if not self.isroot and \
           (self.dist != self.procs[self.par].dist + 1) and \
           (self.procs[self.par].dist < self.n-1):
            if (action == 'EXEC-COMMAND'):
                self.dist = self.procs[self.par].dist + 1
            return 1
        # 規則2:
        elif not self.isroot and \
             ((pid_k := self.argmin_dist()) is not None) and \
             (self.procs[self.par].dist > self.procs[pid_k].dist):
            if (action == 'EXEC-COMMAND'):
                self.dist = self.procs[pid_k].dist + 1
                self.par  = pid_k
            return 2
        # すべてのガードが偽
        else:
            return 0

    # 規則3のガード部分
    def argmin_dist(self):
        k = self.neighbors[0]
        for l in self.neighbors[1:]:
            if self.procs[k].dist > self.procs[l].dist:
                k = l
        return k
