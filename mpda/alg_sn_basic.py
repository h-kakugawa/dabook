# スナップショット, 応用アルゴリズムクラス
from simulator import Simulator
from algorithm import Algorithm
from alg_if_sn import AlgorithmSnapshotIf

class SN_Basic(Algorithm, AlgorithmSnapshotIf):

    @staticmethod
    def get_name():
        return 'Basic algorithm'

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        # __lstate: 局所状態
        #   スナップショット値の確認用に事象発生ごとに増加させる
        self.__lstate = 0  

    # 内部事象
    def on_internal_event(self, ev_msg):
        self.__lstate += 1

    # 送信事象
    def send(self, msg, pid_to, delay = None):
        self.__lstate += 1
        super().send(msg, pid_to, delay)

    # 受信事象
    def message_handler(self, pid_from, msg):
        self.__lstate += 1
        super().message_handler(pid_from, msg)

    # 局所状態の取得
    def take_local_state(self):
        return self.__lstate
