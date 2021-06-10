import serial as pyserial
from . import communicator

class serial(communicator.communicator):
    method = 'serial'

    terminator = b''
    
    port = None
    baudrate = 9600
    bytesize = pyserial.EIGHTBITS
    parity = pyserial.PARITY_NONE
    stopbits = pyserial.STOPBITS_ONE
    timeout = None
    xonxoff = False
    rtscts = False
    write_timeout = None
    dsrdtr = False
    inter_byte_timeout = None
    
    def __init__(self, port,
                 baudrate = 9600,
                 bytesize = pyserial.EIGHTBITS,
                 parity = pyserial.PARITY_NONE,
                 stopbits = pyserial.STOPBITS_ONE,
                 timeout = None,
                 xonxoff = False,
                 rtscts = False,
                 write_timeout = None,
                 dsrdtr = False,
                 inter_byte_timeout = None):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.write_timeout = write_timeout
        self.dsrdtr = dsrdtr
        self.inter_byte_timeout = inter_byte_timeout
        pass

    def open(self):
        if self.connection == False:
            self.ser = pyserial.Serial(
                port = self.port,
                baudrate = self.baudrate,
                bytesize = self.bytesize,
                parity = self.parity,
                stopbits = self.stopbits,
                timeout = self.timeout,
                xonxoff = self.xonxoff,
                rtscts = self.rtscts,
                write_timeout = self.write_timeout,
                dsrdtr = self.dsrdtr,
                inter_byte_timeout = self.inter_byte_timeout,
            )

            self.connection = True
            pass
        return

    def close(self):
        self.ser.close()
        del(self.ser)
        self.connection = False
        return

    def send(self, msg):
        if type(msg)==str: msg = msg.encode()
        self.ser.write(msg+self.terminator)
        return

    def recv(self, byte=1024):
        d = self.ser.read(byte)
        if d.isascii():
            return d.decode()
        return d

    def readline(self):
        d = self.ser.readline()
        if d.isascii():
            return d.decode()
        return d
