#! /usr/bin/env python3

import time
import serial

class tr_73u(object):

    def __init__(self, port):
        self.ser = self.serial_open(port)
        self.start()
        return

    def serial_open(self, port):
        ser = serial.Serial(port=port, baundrate=19200, timeout=None, stopbit=1)
        return ser

    def write(self, cmd):
        self.ser.write(cmd)
        return

    def read(self, byte=100):
        self.ser.read(byte_size)
        return

    def query(self, cmd, byte, wt=0.01):
        self.write(cmd)
        time.sleep(wt)
        ret = self.read(byte)
        return ret

    def　start(self):
        self.write(b'0x00')
        return

    def output_current_data(self):
        data = self.query(cmd=b'\x01\x33\x00\x04\x00\x00\x00\x00\x00\x38\x00', byte=26)
        return data
