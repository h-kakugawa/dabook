# 自己安定分散アルゴリズムシミュレータ
# シミュレータコア部分

import sys
import os
import copy
import random
import argparse

class SimSSDA():
    def __init__(self, ssalg_class, nw,
                 duration = None,
                 how_init = None,
                 rseed = None):
        self.ssalg_class = ssalg_class # アルゴリズムのクラス
        self.nw        = nw        # ネットワーク
        self.how_init  = how_init  # プロセス状態の初期化方法, または 初期状況
        self.rseed     = rseed     # 疑似乱数系列の種
        self.duration  = duration  # 実行打ち切り時間
        self.curtime = None    # シミュレーション時間
        self.procs   = None    # プロセスオブジェクト表 (添字: 0..n-1)
        self.n_execs = None    # 規則の実行総数
        self.exec_order = []   # プロセスの実行スケジュール(実行順序リスト)

    # シミュレーション実行 (実行結果のファイル出力制御)
    def start(self, fname_out):
        # 実行
        if fname_out is not None:  # 出力ファイル指定あり
            with open(fname_out, 'w') as f_out:
                sys.stdout = f_out  
                self.__start()
                sys.stdout = sys.__stdout__
        else:    # 出力ファイル指定なし
            self.__start()

    # シミュレーション実行本体
    def __start(self):
        # 乱数生成器の初期化
        random.seed(a = self.rseed)
        # シミュレーション管理変数の初期化
        self.curtime = -1
        self.n_execs = 0
        self.procs = [ None for pi in range(self.nw.get_n()) ]
        self.exec_order = []
        # 初期状況(指定された場合)のチェック
        if (type(self.how_init) is list) \
           and (len(self.how_init) != self.nw.get_n()):
            # プロセス数ぶんだけの指定がされてない
            print('ERROR: Initial configuration does not match network size:')
            print('  {}'.format(self.how_init))
            sys.exit(1)
        # プロセス生成
        for pi in range(self.nw.get_n()):
            self.procs[pi] = self.ssalg_class(pi, self.nw.get_neighbors(pi),
                                              self.procs, self.how_init)
        # アルゴリズム名表示
        print("ALGORITHM: {}".format(self.ssalg_class.get_name()))
        # パラメータ表示出力
        print("NETWORK: {}".format(self.nw.get_name()))
        print("NPROCS: {}".format(self.nw.get_n()))
        links = []   # リンク
        for pi in range(self.nw.get_n()):
            gtnei = list(filter(lambda pj: pi < pj, self.nw.get_neighbors(pi)))
            es = list(map(lambda pj: (pi, pj), gtnei))
            for e in es:
                links.append(e)
        print("LINKS: {}".format(links))
        print("HOW_INIT:  {}".format(self.how_init))
        print("RAND_SEED: {}".format(self.rseed))
        # シミュレーションメインループ
        while True:
            print("#----------------")
            # 時刻管理
            self.curtime += 1
            if type(self.duration) is int and \
               (self.curtime > self.duration):  # 実行時間上限
                print("ABORTED: EXCEEDS SIMULATION DURATION LIMIT")
                sys.exit(1)  # 実行打切
            print("TIME: {}".format(self.curtime))
            # 状況の表示
            c = [ self.procs[pi].state()
                  for pi in range(self.nw.get_n()) ]
            print("CONFIG: {}".format(c))
            # 各プロセスのガードの評価
            gval = [ self.procs[pi].guarded_command(action='EVAL-GUARD') \
                     for pi in range(self.nw.get_n()) ]
            # ガードの評価結果の表示
            print("GUARD: {}".format(gval))
            # ガードが真のプロセス数の表示 (特権数)
            nprivs = len(list(filter(lambda g: g > 0, gval)))
            print("N_PRIVS: {}".format(nprivs))
            if nprivs == 0:
                # 収束: 全プロセスでガードが偽
                print("EXEC_PROC: ")
                break
            # Cデーモンによる実行対象プロセスの選択
            pi = self.c_daemon(gval)
            # 選択されたプロセスでのコマンド実行
            self.procs[pi].guarded_command(action='EXEC-COMMAND')
            self.n_execs += 1
            print("EXEC_PROC: {}".format(pi))
        # 統計出力
        print("#----------------")
        print("CONVERGED:")
        print("N_STEPS: {}".format(self.curtime))
        print("N_EXECS: {}".format(self.n_execs))
        print("DONE:")

    # Cデーモン (呼出の前提: 真のガードを持つプロセスが存在)
    def c_daemon(self, gval):
        n = 2*self.nw.get_n()
        while n > 0:
            if len(self.exec_order) == 0:
                self.exec_order = self.pid_order_random() 
            pi = self.exec_order[0]
            self.exec_order = self.exec_order[1:]
            if gval[pi] > 0:  # piには真のガードあり
                return pi     # piを選択
            n = n - 1
        print("INTERNAL ERROR: c_daemon()")
        sys.exit(1)

    # プロセス識別子のランダムな順序を生成
    def pid_order_random(self):
        # ダステンフェルドのアルゴリズムを使用
        pid_list = [ i for i in range(self.nw.get_n()) ]
        for i in range(self.nw.get_n()-1, -1, -1):
            j = random.randint(0, i)
            (pid_list[i],pid_list[j]) = (pid_list[j], pid_list[i])
        return pid_list
