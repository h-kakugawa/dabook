import abc
class AlgorithmTerminationDetectionIf(metaclass=abc.ABCMeta):
#    @abc.abstractmethod
#    def td_active(self): 
#        pass
#    @abc.abstractmethod
#    def td_passive(self):
#        pass
    @abc.abstractmethod
    def td_message_handler(self, app, pid_from, msg):
        pass
    @abc.abstractmethod
    def td_send(self, app, msg, pid_to):
        pass
