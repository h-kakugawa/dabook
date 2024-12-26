# SSTR_AG 
# Self-stabilizing spanning tree
# by Arora and Gouda (IEEE-TC 1994)

from alg_SS import SS_Algorithm
import sys
import random

class SSTR_AG(SS_Algorithm):
    @staticmethod
    def get_name():
        return 'SSTR_AG by Arora and Gouda for self-stabilizing spanning tree'

    # 局所変数
    root = None
    par  = None
    dist = None

    # 補助変数 (定数)
    K = None   # dist の上限
    ni = None  # 隣接プロセス集合 と Pi よりなる集合
    
    # 局所変数の初期化
    def init_local_state(self, how_init):
        n = len(self.procs)
        self.K = n
        self.ni = list(self.neighbors.copy())
        self.ni.append(self.pid)
        if ((type(how_init) is str) and (how_init == 'zero')): # ゼロ
            self.root = 0
            self.par  = self.pid
            self.dist = 0
        elif ((type(how_init) is str) and (how_init == 'random')) \
             or (how_init == None): # ランダム
            self.root = random.randint(0, n-1)
            self.par  = self.ni[random.randint(0, len(self.neighbors))]
            self.dist = random.randint(0, self.K-1)
        elif (type(how_init) is list): # 指定値
            self.root = how_init[self.pid][0]
            self.par  = how_init[self.pid][1]
            self.dist = how_init[self.pid][2]
        else:
            print("ERROR: UNKNOWN INITIALIZATION METHOD {}".format(how_init))
            sys.exit(1)

    # 局所変数
    def state(self):
        return [self.root, self.par, self.dist]

    # 自己安定分散アルゴリズム  本体
    def guarded_command(self, action):
        # 規則1: 根プロセスに立候補
        if (self.root < self.pid) or \
           ((self.par == self.pid) and \
            ((self.root != self.pid) or (self.dist != 0))) or \
           ((self.par not in self.ni) or (self.dist >= self.K)):
            if (action == 'EXEC-COMMAND'):
                self.root = self.pid
                self.par  = self.pid
                self.dist = 0
            return 1
        # 規則3: 親プロセスの選択
        elif ((pid_j := self.r3g()) is not None): 
            if (action == 'EXEC-COMMAND'):
                self.root = self.procs[pid_j].root
                self.par  = pid_j
                self.dist = self.procs[pid_j].dist + 1
            return 3
        # 規則2: 根プロセスと最短距離の設定
        elif (self.par in self.neighbors) and \
             (self.dist < self.K) and \
             ((self.root != self.procs[self.par].root) or \
              (self.dist != self.procs[self.par].dist + 1)):
            if (action == 'EXEC-COMMAND'):
                self.root = self.procs[self.par].root
                self.dist = self.procs[self.par].dist + 1
            return 2
        # すべてのガードが偽
        else:
            return 0

    # 規則3のガード部分
    def r3g(self):
        pid_j = None
        for j in self.neighbors:
            if ((self.root < self.procs[j].root) and \
                (self.procs[j].dist < self.K))   or  \
               ((self.root == self.procs[j].root) and \
                (self.procs[j].dist + 1 < self.dist)):
                #pid_j = j
                #return pid_j
                # Optimization    
                if (pid_j is None) or \
                   (self.procs[pid_j].root > self.procs[j].root):
                    pid_j = j
                elif (self.procs[pid_j].root == self.procs[j].root) and \
                     (self.procs[pid_j].dist > self.procs[j].dist):
                    pid_j = j
        return pid_j

