#! /usr/bin/env python3

import time
import serial

class tr_73u(object):

    def __init__(self, port):
        self.ser = self.serial_open(port)
        self.start()
        return

    def serial_open(self, port):
        ser = serial.Serial(port=port, baudrate=19200, timeout=5, stopbits=1)
        return ser

    def write(self, cmd):
        self.ser.write(cmd)
        return

    def read(self, byte=100):
        ret = self.ser.read(byte)
        return ret

    def query(self, cmd, byte, wt=0.01):
        self.write(cmd)
        time.sleep(wt)
        ret = self.read(byte)
        return ret

    def start(self):
        self.write(b'0x00')
        return

    def output_current_data(self):
        data = self.query(cmd=b'\x01\x33\x00\x04\x00\x00\x00\x00\x00\x38\x00', byte=26)
        return data

    #data = 26byte, format=B
    #temp = (data[6]*16**2+data[5]-1000)/10
    #humid = (data[8]*16**2+data[7]-1000)/10
    #press = (data[10]*16**2+data[9])/10
