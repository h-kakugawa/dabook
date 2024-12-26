# WV_Pに対して停止判定(TD)を行うためのラッパークラス
from alg_WV_P import WV_P
from simulator import Simulator

class WV_P_TD(WV_P):

    @staticmethod
    def get_name():
        return "WV_P_TD for wave on cliqeue (WV_P) " \
            + "with termination detection interface"

    def __init__(self, pid, nw, tdet):
        super().__init__(pid, nw)
        self.tdet = tdet

    def set_sim(self, sim):
        super().set_sim(sim)
        self.tdet.set_sim(sim)

    def when_initiator(self):
        self.tdet.__initiator = self.is_initiator()
        self.tdet.td_when_initiator(super())

    def message_handler(self, pid_from, msg):
        self.tdet.td_message_handler(super(), pid_from, msg)

    def send(self, msg, pid_to, delay = None):
        self.tdet.td_send(super(), msg, pid_to, delay = delay)
