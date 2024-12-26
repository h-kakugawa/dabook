# プロセス実装クラスのインターフェース
import abc

class ProcessIf(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_sim(self, sim):
        pass
    @abc.abstractmethod
    def event_handler(self, ev_type, ev_msg):
        pass
