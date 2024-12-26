# SSCOL
# Self-stabilizing coloring
# by Hedetniemi, Jacobs and Srimani (IPL 2003)

from alg_SS import SS_Algorithm
import sys
import random

class SSCOL(SS_Algorithm):
    @staticmethod
    def get_name():
        return 'SSCOL by Hedetniemi et al. ' + \
            'for self-stabilizing coloring'

    # 局所変数
    c = 0

    # 局所変数の初期化
    def init_local_state(self, how_init):
        if ((type(how_init) is str) and (how_init == 'zero')): # ゼロ
            self.c = 1
        elif ((type(how_init) is str) and (how_init == 'random')) \
             or (how_init == None): # ランダム
            self.c = random.randint(1, len(self.neighbors)+1)
        elif (type(how_init) is list): # 指定値
            self.c = how_init[self.pid][0]
        else:
            print("ERROR: UNKNOWN INITIALIZATION METHOD {}".format(how_init))
            sys.exit(1)

    # 局所変数
    def state(self):
        return [self.c]

    # 自己安定分散アルゴリズム本体
    def guarded_command(self, action):

        nc = self.neighc()  # 隣接プロセスに割り当て済みの色集合
        delta = len(self.neighbors)  # 次数
        allc = set(c for c in range(1, len(self.neighbors)+1))

        # 規則1: 彩色規則
        if self.c in nc:
            if (action == 'EXEC-COMMAND'):
                if nc == allc:
                    self.c = delta + 1
                else:
                    self.c = min(allc - nc)
            return 1
        # すべてのガードが偽
        return 0

    # 隣接プロセスに割り当て済みの色集合
    def neighc(self):
        return set(self.procs[pid_j].c for pid_j in self.neighbors)
