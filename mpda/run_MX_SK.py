# MX_SK 実行スクリプト
from alg_MX_SK import MX_SK        # 実行アルゴリズム
from simulator import Simulator    # シミュレーター
from nw_complete import NWComplete # ネットワーク
import sys

# 事象スクリプト
evs = [ [  0.5,  0,  'INTERNAL', 'REQ-CS'  ],
        [  2.5,  2,  'INTERNAL', 'REQ-CS'  ],
        [  4.5,  0,  'INTERNAL', 'EXIT-CS' ],
        [  6.0,  2,  'INTERNAL', 'EXIT-CS' ] ]

# プロセス数の指定
param_n = 3
# ネットワークの生成
nw = NWComplete(param_n, delay_spec = 0.7)
# プロセスの生成
procs = [ MX_SK(pid, nw) for pid in range(nw.get_n()) ]
# 始動プロセスの指定
param_i = None
# シミュレーターの生成
sim = Simulator(nw, procs, param_i, evscript = evs)
# シミュレーション開始
sim.start()
