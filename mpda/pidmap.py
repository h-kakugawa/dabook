# PID写像: PIDの順序の変更
import random
import traceback
import sys

class PIDMap():
    def __init__(self, n, pidmap_spec):
        self.__n = n
        self.__map = [ i for i in range(n) ] # 昇順
        if pidmap_spec == None:
            self.__setup_ascend()
        elif pidmap_spec == 'ascend':
            self.__setup_ascend()
        elif pidmap_spec == 'descend':
            self.__setup_descend()
        elif pidmap_spec == 'random':
            self.__setup_random()
        elif pidmap_spec == 'interleave':
            self.__setup_interleave()
        elif pidmap_spec == 'revbin':
            self.__setup_revbinary()
        elif pidmap_spec[0] == '[':
            self.__setup_as_specified(pidmap_spec)
        else:
            print('ERROR: UNNOWN pidmap_spec:', pidmap_spec)
            print('pidmap_spec: ascend, descend, random, interleave, revbin')
            sys.exit(1)
        self.__self_test()
            
    # PIDの写像
    def map(self, i):
        return self.__map[i]

    # 写像設定: 昇順
    def __setup_ascend(self):
        self.__map = [ i for i in range(self.__n) ]

    # 写像設定: 降順
    def __setup_descend(self):
        self.__map = [ self.__n - 1 - i for i in range(0, self.__n) ]

    # 写像設定: ランダム
    def __setup_random(self):  
        self.__setup_ascend()
        # ダステンフェルドのアルゴリズムを使用
        for i in range(self.__n - 1, -1, -1):
            j = random.randint(0, i)
            t = self.__map[i]
            self.__map[i] = self.__map[j]
            self.__map[j] = t

    # 写像設定: インターリーブ
    def __setup_interleave(self):
        for i in range(0, self.__n - 1, 2):
            self.__map[i+0] = i+1
            self.__map[i+1] = i+0
        if self.__n % 2 == 1:
            self.__map[self.__n - 1] = self.__n - 1

    # 写像設定: 指定通りに
    def __setup_as_specified(self, spec):
        s = eval(spec)
        if self.__n != len(s):
            sys.exit('ERROR (pidmap.py): ILLEGAL PROC ARRANGEMENT DATA '  \
                     + str(spec) + '<->' + str(self.__n))
        if self.__n != len(set(s)):
            sys.exit('ERROR (pidmap.py): ILLEGAL PROC ARRANGEMENT DATA '  \
                     + str(spec) + '<->' + str(self.__n))
        for i in range(self.__n):
            self.__map[i] = s[i]

    # 写像設定: バイナリビット逆転 (nは2の冪乗に限定)
    def __setup_revbinary(self):
        # nは2の冪乗か否か
        nnn = self.__n
        while nnn > 0:
            if (nnn % 2 == 1) and ((nnn // 2) != 0):
                sys.exit('ERROR: NOT A POWER OF 2 for N: ' + str(self.__n))
            nnn = nnn // 2
        # バイナリビット逆転
        for i in range(self.__n):
            i_rev = 0
            ii = i
            nn = self.__n - 1
            while nn != 0:
                nn = nn // 2
                (ii, m) = divmod(ii, 2)
                if m % 2 == 0:
                    i_rev = 2 * i_rev
                else:
                    i_rev = 2 * i_rev + 1
            self.__map[i] = i_rev
            
    # 自己診断用
    def __self_test(self):
        if (len(self.__map) != self.__n) \
           or ({pid for pid in range(self.__n)} != set(range(self.__n))):
            sys.exit('INTERNAL ERROR (pidmap.py): BROKEN MAPPING')
