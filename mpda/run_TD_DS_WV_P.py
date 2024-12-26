# TD_DS 実行スクリプト (応用アルゴリズム: WV_P)
from alg_TD_DS import TD_DS        # 実行アルゴリズム
from alg_WV_P_TD import WV_P_TD    # 基本アルゴリズム
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
tdets = [ TD_DS(pid, nw)                for pid in range(nw.get_n()) ]
procs = [ WV_P_TD(pid, nw, tdets[pid])  for pid in range(nw.get_n()) ]
# 始動プロセスの指定
param_i = [0]
# シミュレーターの生成
sim = Simulator(nw, procs, param_i, evscript = evs)
# シミュレーション開始
sim.start()
