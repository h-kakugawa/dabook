# SP 実行スクリプト
from alg_SP import SP              # 実行アルゴリズム
from simulator import Simulator    # シミュレーター
from nw_file import NWFile         # ネットワーク
import sys

# 事象スクリプト
evs = [ ]
# プロセス数の指定
param_n = 'g_sp_a_1.dat'
# ネットワークの生成
nw = NWFile(param_n)
# プロセスの生成
procs = [ SP(pid, nw) for pid in range(nw.get_n()) ]
# 始動プロセスの指定
param_i = [0]
# シミュレーターの生成
sim = Simulator(nw, procs, param_i, evscript = evs)
# シミュレーション開始
sim.start()
