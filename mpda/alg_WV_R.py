from algorithm import Algorithm
from simulator import Simulator

class WV_R(Algorithm):

    @staticmethod
    def get_name():
        return 'WV-R by Tel for Wave'
    
    def __init__(self, pid, nw):
        super().__init__(pid, nw)

    def when_initiator(self):
        self.send_to_next(['TOKEN'])

    def message_handler(self, pid_from, msg):
        [msg_type, *_] = msg
        if msg_type == 'TOKEN': 
            if self.is_initiator():
                self.emit_internal('DECIDE')
                self.halt()
            else:
                self.send_to_next(['TOKEN'])

    def send_to_next(self, msg):
        pid_next = (self.pid + 1) % self.get_n()
        self.send(msg, pid_next)
