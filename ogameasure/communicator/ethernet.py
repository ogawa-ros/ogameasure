import socket
from . import communicator


class ethernet(communicator.communicator):
    method = 'ethernet'

    host = ''
    port = 0
    timeout = 3
    family = ''
    type = ''

    def __init__(self, host, port, timeout=3,
                 family=socket.AF_INET,
                 type=socket.SOCK_STREAM):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.family = family
        self.type = type
        pass

    def open(self):
        #print('open', self.host, self.port)
        if self.connection == False:
            self.sock = socket.socket(self.family, self.type)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.host, self.port))
            self.sockfp = self.sock.makefile()
            self.connection = True
            pass
        return

    def close(self):
        self.sock.close()
        del(self.sock)
        self.connection = False
        return

    def send(self, msg):
        #self.sock.send(msg)
        self.sock.send((msg+self.terminator).encode())
        return
        
    def recv(self, byte=1024):
        ret = self.sock.recv(byte)
        return ret

    def readline(self):
        ret = self.sockfp.readline()
        return ret
