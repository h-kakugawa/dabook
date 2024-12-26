# SPに対して停止判定(TD)を行うためのラッパークラス
from alg_SP import SP
from simulator import Simulator

class SP_TD(SP):

    @staticmethod
    def get_name():
        return "SP_TD for shortest path tree (SP) " \
            + "with termination detection interface"

    def __init__(self, pid, nw, tdet):
        super().__init__(pid, nw)
        self.tdet = tdet

    def set_sim(self, sim):
        super().set_sim(sim)
        self.tdet.set_sim(sim)

    def when_initiator(self):
        self.tdet.td_when_initiator(super())
        self.tdet.__initiator = super().is_initiator()

    def message_handler(self, pid_from, msg):
        self.tdet.td_message_handler(super(), pid_from, msg)

    def send(self, msg, pid_to, delay = None):
        self.tdet.td_send(super(), msg, pid_to, delay = delay)
