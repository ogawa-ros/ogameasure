import time
from . import communicator
from . import ethernet

class gpib_prologix(communicator.communicator):
    method ='gpib_prologix'

    open_flag = False

    host = ''
    gpibport = 10
    lag = 0.02

    def __init__(self, host, gpibport=10, lag=0.02, timeout=10):
        self.gpibport = gpibport
        self.lag = lag
        if type(host) == str:
            self.com = ethernet(host, 1234, timeout)
        else:
            self.com = host
        pass

    def _sleep(self):
        time.sleep(self.lag)
        return

    def open(self):
        if self.open_flag == False:
            self.com.open()
            self.mode_controller()
            self.open_flag = True
            pass
        return

    def close(self):
        self.com.close()
        self.open_flag = False
        return

    def send(self, msg):
        self.use_gpibport()
        self.com.send((msg+self.terminator))
        self._sleep()
        return

    def _send(self, msg):
        self.com.send(msg + self.terminator)
        self._sleep()
        return

    def recv(self, byte):
        self._send('++read %d'%byte)
        ret = self.com.recv(byte)
        return ret

    def readline(self):
        self._send('++read eoi')
        ret = self.com.readline()
        return ret

    def get_info(self):
        self._send('++ver')
        ret = self.readline().strip()
        return ret

    def set_gpibport(self, gpib):
        self.gpibport = int(gpib)
        self.use_gpibport()
        return

    def use_gpibport(self):
        self._send('++addr %d'%(self.gpibport))
        return

    def get_gpibport(self):
        self._send('++addr')
        ret = int(self.readline().strip())
        return ret

    def mode_device(self):
        self._send('++mode 0')
        self.get_mode()
        return

    def mode_controller(self):
        self._send('++mode 1')
        self.get_mode()
        return

    def get_mode(self):
        self._send('++mode')
        ret = int(self.readline().strip())
        return ret
