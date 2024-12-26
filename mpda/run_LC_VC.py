# LC_VC 実行スクリプト
from alg_LC_VC import LC_VC        # 実行アルゴリズム
from simulator import Simulator    # シミュレーター
from nw_complete import NWComplete # ネットワーク
import sys

# 仮想プロセス動作 (論理時計の動作確認用)
class LC_Test(LC_VC):

    @staticmethod
    def get_name():
        return 'Test run of logical scalar clock'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
    
    def on_internal_event(self, ev_msg):
        ev_tag =  ev_msg
        self.tick()
        self.emit_remark("LC {}".format(self.get_value()))

    def send(self, msg, pid_to, delay = None):
        self.tick()
        super().send(msg, pid_to, delay)

    def message_handler(self, pid_from, msg):
        super().message_received(msg)
        self.emit_remark("LC {}".format(self.get_value()))

# 事象スクリプト
evs = [         [  1.0,  0,  'INTERNAL', 'I' ],
        [  1.5,  0,  'SEND', 1,  ['M'], 0.3 ],
        [  2.0,  0,  'SEND', 2,  ['M'], 4.0 ],
        [  4.5,  0,  'SEND', 2,  ['M'], 0.8 ],
        [  5.0,  0,  'INTERNAL', 'I' ],
        [  2.3,  1,  'SEND', 2,  ['M'], 0.3 ],
        [  2.0,  2,  'SEND', 3,  ['M'], 0.2 ],
        [  3.5,  2,  'INTERNAL', 'I' ],
        [  4.0,  2,  'SEND', 3,  ['M'], 1.0 ],
        [  6.5,  2,  'INTERNAL', 'I' ],
        [  1.0,  3,  'INTERNAL', 'I' ],
        [  1.5,  3,  'SEND', 2,  ['M'], 0.2 ],
        [  3.0,  3,  'INTERNAL', 'I' ],
        [  3.5,  3,  'SEND', 0,  ['M'], 0.5 ] ]

# プロセス数の指定
param_n = 4
# ネットワークの生成
nw = NWComplete(param_n)
# プロセスの生成
procs = [ LC_Test(pid, nw) for pid in range(nw.get_n()) ]
# 始動プロセスの指定
param_i = None
# シミュレーターの生成
sim = Simulator(nw, procs, param_i, evscript = evs)
# シミュレーション開始
sim.start()
