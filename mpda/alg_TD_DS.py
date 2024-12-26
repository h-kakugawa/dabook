from simulator import Simulator
from algorithm import Algorithm
from alg_if_td import AlgorithmTerminationDetectionIf

class TD_DS(Algorithm, AlgorithmTerminationDetectionIf):
    
    @staticmethod
    def get_name():
        return 'TD-DS by Dijkstra & Scholten for Termination Detection '

    def __init__(self, pid, nw):
        super().__init__(pid, nw)
        self.state = 'PASSIVE'
        self.par = None
        self.d = 0

    def td_when_initiator(self, app): 
        self.par = self.pid
        self.emit_internal('ACTIVE')
        self.state = 'ACTIVE'
        app.when_initiator()
        self.emit_internal('PASSIVE')
        self.state = 'PASSIVE'
        if (self.d == 0):
            self.emit_internal('DETECTED')

    def td_message_handler(self, app, pid_from, msg):
        [mtype, *_] = msg
        if mtype == 'BASIC':
            [_, bmsg] = msg
            self.emit_internal('ACTIVE')
            self.state = 'ACTIVE'
            app.message_handler(pid_from, bmsg)
            self.emit_internal('PASSIVE')
            self.state = 'PASSIVE'
            if self.par is None and (self.d > 0):
                self.par = pid_from
            else:
                self.send(['SIGNAL'], pid_from)
        elif mtype == 'SIGNAL':
            self.d -= 1
            if self.d == 0:
                if self.par == self.pid:
                    self.emit_internal('DETECTED')
                else:
                    self.send(['SIGNAL'], self.par)
                self.par = None
            
    def td_send(self, app, bmsg, pid_to, delay = None):
        msg = ['BASIC', bmsg]
        app.send(msg, pid_to, delay = delay)
        self.d += 1
