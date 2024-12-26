import abc

class AlgorithmSnapshotIf(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def take_local_state(self):
        pass
