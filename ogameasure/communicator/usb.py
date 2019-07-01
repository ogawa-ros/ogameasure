import serial
from serial.tools import list_ports
from . import communicator

class usb(communicator.communicator):
    method = 'usb'

    serial_number = ''
    port = ''
    rtimeout = 0.1
    wtimeout = 0.1

    def __init__(self, serial_number):
        self.serial_number = serial_number.upper()
        #self.rtimeout = timeout
        #self.wtimeout = timeout
        serial_li = list_ports.comports()
        for i in range(len(serial_li)):
            try:
                if serial_li[i].serial_number == self.serial_number:
                    self.port = serial_li[i].device
                else: pass
            except: pass
        return

    def open(self):
        if self.connection == False:
            self.ser = serial.Serial(
                self.port, timeout=self.rtimeout, write_timeout=self.wtimeout
            )
            self.connection = True
        return

    def close(self):
        if self.connection == True:
            self.ser.close()
            self.connection = False
        return

    def send(self, msg):
        self.ser.write(msg)
        return

    def recv(self, byte=1024):
        ret = self.ser.read(byte)
        return ret
