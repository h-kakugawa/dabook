# SSMIS (Self-stabilizing maximal independet set)
# by Shulka et al. (WSS 95)

from alg_SS import SS_Algorithm
import sys
import random

class SSMIS(SS_Algorithm):
    @staticmethod
    def get_name():
        return 'SSMIS by Shulka et al. ' + \
            'for self-stabilizing maximal independent set'

    # 局所変数
    x = 0
    
    # 局所変数の初期化
    def init_local_state(self, how_init):
        if ((type(how_init) is str) and (how_init == 'zero')): # ゼロ
            self.x = 0
        elif ((type(how_init) is str) and (how_init == 'random')) \
             or (how_init == None): # ランダム
            self.x = random.randint(0, 1)
        elif (type(how_init) is list): # 指定値
            self.x = how_init[self.pid][0]
        else:
            print("ERROR: UNKNOWN INITIALIZATION METHOD {}".format(how_init))
            sys.exit(1)

    # 局所変数
    def state(self):
        return [self.x]

    # 自己安定分散アルゴリズム  本体
    def guarded_command(self, action):
        # 規則1: 独立性
        if (self.x == 1) and \
           any([self.procs[pj].x == 1 for pj in self.neighbors]):
            if (action == 'EXEC-COMMAND'):
                self.x = 0
            return 1
        # 規則2: 極大性
        elif (self.x == 0) and \
             all([self.procs[pj].x == 0 for pj in self.neighbors]):
            if (action == 'EXEC-COMMAND'):
                self.x = 1
            return 2
        # すべてのガードが偽
        else:
            return 0
