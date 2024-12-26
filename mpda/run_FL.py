# FL 実行スクリプト
from alg_FL import FL              # 実行アルゴリズム
from simulator import Simulator    # シミュレーター
from nw_grid import NWGrid         # ネットワーク
import sys

# 事象スクリプト
evs = [ ]
# プロセス数の指定
param_n = '3x3'
# ネットワークの生成
nw = NWGrid(param_n)
# プロセスの生成
procs = [ FL(pid, nw) for pid in range(nw.get_n()) ]
# 始動プロセスの指定
param_i = [0]
# シミュレーターの生成
sim = Simulator(nw, procs, param_i, evscript = evs)
# シミュレーション開始
sim.start()
