# WV_P 実行スクリプト
from alg_WV_P import WV_P          # 実行アルゴリズム
from simulator import Simulator    # シミュレーター
from nw_complete import NWComplete # ネットワーク
import sys

# 事象スクリプト
evs = [ ]
# プロセス数の指定
param_n = 6
# ネットワークの生成
nw = NWComplete(param_n)
# プロセスの生成
procs = [ WV_P(pid, nw) for pid in range(nw.get_n()) ]
# 始動プロセスの指定
param_i = [0]
# シミュレーターの生成
sim = Simulator(nw, procs, param_i, evscript = evs)
# シミュレーション開始
sim.start()
