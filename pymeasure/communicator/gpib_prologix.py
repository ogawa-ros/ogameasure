#! /usr/bin/env python

import time
import communicator
import ethernet

class gpib_prologix(communicator.communicator):
    method ='gpib_prologix'
    
    host = ''
    gpibport = 10
    lag = 0.02

    def __init__(self, host, gpibport=10, lag=0.02, timeout=10):
        self.gpibport = gpibport
        self.lag = lag
        self.com = ethernet.ethernet(host, 1234, timeout)
        pass
    
    def _sleep(self):
        time.sleep(self.lag)
        return
        
    def open(self):
        self.com.open()
        self.mode_controller()
        self.set_gpibport(self.gpibport)
        return
        
    def close(self):
        self.com.close()
        return
    
    def send(self, msg):
        self.com.send(msg)
        self._sleep()
        return
    
    def recv(self, byte):
        self.send('++read %d\n'%byte)
        ret = self.com.recv(byte)
        return ret

    def readline(self):
        self.send('++read eoi\n')
        ret = self.com.readline()
        return ret
    
    def get_info(self):
        self.send('++ver\n')
        ret = self.readline().strip()
        return ret
        
    def set_gpibport(self, gpib):
        self.gpibport = int(gpib)
        self.send('++addr %d\n'%(self.gpibport))
        return

    def get_gpibport(self):
        self.send('++addr\n')
        ret = int(self.readline().strip())
        return ret
        
    def mode_device(self):
        self.send('++mode 0\n')
        self.get_mode()
        return

    def mode_controller(self):
        self.send('++mode 1\n')
        self.get_mode()
        return
        
    def get_mode(self):
        self.send('++mode\n')
        ret = int(self.readline().strip())
        return ret
