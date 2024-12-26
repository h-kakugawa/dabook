# LE_P 実行スクリプト
from alg_LE_P import LE_P                # 実行アルゴリズム
from simulator import Simulator          # シミュレーター
from nw_ring_unidir import NWRingUnidir  # ネットワーク

# プロセス数の指定
param_n = 4
# ネットワークの生成 (プロセス配置: ascend/descend/random/revbin/[list])
nw = NWRingUnidir(param_n, pidmap_spec = 'random')
# プロセスの生成
procs = [ LE_P(pid, nw) for pid in range(nw.get_n()) ]
# 始動プロセスの指定 (ほか 0 や [0,1,2] の形でも指定可)
param_i = 'all'  
# シミュレーターの生成
sim = Simulator(nw, procs, param_i)
# シミュレーション開始
sim.start()
