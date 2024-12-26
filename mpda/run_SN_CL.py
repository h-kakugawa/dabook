# FL 実行スクリプト
from alg_SN_CL import SN_CL        # 実行アルゴリズム
from alg_sn_basic import SN_Basic  # 応用アルゴリズム
from simulator import Simulator    # シミュレーター
from nw_file import NWFile         # ネットワーク (DIMACS形式ファイル)
import sys

# 事象スクリプト
evs = [ [  1.9,  0,  'INTERNAL', 'SNAPSHOT' ],
        [  0.5,  0,  'SEND', 2,  ['m1'] ],
        [  0.7,  0,  'SEND', 1,  ['m2'] ],
        [  1.7,  2,  'SEND', 0,  ['m3'] ],
        [  1.9,  2,  'SEND', 0,  ['m4'] ],
        [  2.1,  2,  'SEND', 3,  ['m5'] ],
        [  3.3,  3,  'SEND', 2,  ['m6'] ],
        [  4.5,  2,  'SEND', 3,  ['m7'] ] ]
# プロセス数の指定
param_n = 'g_sn_cl_1.dat'
# ネットワークの生成
nw = NWFile(param_n)
# プロセスの生成
basic = [ SN_Basic(pid, nw)          for pid in range(nw.get_n()) ]
procs = [ SN_CL(pid, nw, basic[pid]) for pid in range(nw.get_n()) ]
# 始動プロセスの指定
param_i = []
# シミュレーターの生成
sim = Simulator(nw, procs, param_i, evscript = evs)
for pid in range(nw.get_n()):
    basic[pid].set_sim(sim)
# シミュレーション開始
sim.start()
