# TD_DS 実行スクリプト (応用アルゴリズム: SP)
from alg_TD_DS import TD_DS        # 実行アルゴリズム
from alg_SP_TD  import SP_TD       # 基本アルゴリズム
from simulator import Simulator    # シミュレーター
from nw_file import NWFile         # ネットワーク (DIMACS形式ファイル)
import sys

# 事象スクリプト
evs = [ ]
# プロセス数の指定
param_n = 'g_td_1.dat'
# ネットワークの生成
nw = NWFile(param_n)
# プロセスの生成
tdets = [ TD_DS(pid, nw)              for pid in range(nw.get_n()) ]
procs = [ SP_TD(pid, nw, tdets[pid])  for pid in range(nw.get_n()) ]
# 始動プロセスの指定
param_i = [0]
# シミュレーターの生成
sim = Simulator(nw, procs, param_i, evscript = evs)
# シミュレーション開始
sim.start()
