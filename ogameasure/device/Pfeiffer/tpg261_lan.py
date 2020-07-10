#! /usr/bin/env python3

import time, numpy

class tpg261_lan(object):

    def __init__(self, com):
        self.com = com
        self.com.open()
        pass

    def pressure(self):
        self.com.send("PR1 \r\n")
        time.sleep(0.1)
        self.com.send("\x05")
        time.sleep(0.1)
        self.raw_p = self.com.recv().decode('utf-8').strip().split(',')
        time.sleep(0.1)
        pressure = float(self.raw_p[-1])
        return pressure

    def tpg_status(self):
        self.com.send(b"PR1 \r\n")
        time.sleep(0.3)
        self.com.send(b"\x05")
        time.sleep(0.3)
        self.get = self.com.recv()
        status_p = self.get[3:4]
        if status_p == b'0' :
            print('Measurement data okay')
        elif status_p == b'1' :
            print('Underrange')
        elif status_p == b'2' :
            print('Overrange')
        elif status_p == b'3' :
            print('Sensor error')
        elif status_p == b'4' :
            print('Sensor off (IKR, PKR, IMR, PBR)')
        elif status_p == b'5' :
            print('No sensor')
        else :
             print('Identification error')

    def turn_status_g1(self):
        self.com.send(b"SEN , 0, 0 \r\n")
        time.sleep(0.3)
        self.com.send(b"\x05")
        time.sleep(0.3)
        self.get = self.com.recv()
        status1_g = self.get[3:4]
        if status1_g == b'0' :
            print('Gauge cannot be turned on/off')
        elif status1_g == b'1' :
            print('Gauge turned off')
        elif status1_g == b'2' :
            print('Gauge turned on')
        else :
            pass

    def gauge_on_g1(self):
        self.com.send(b"SEN , 2 , 0 \r\n")
        time.sleep(0.3)
        self.com.send(b"\x05")
        time.sleep(0.3)
        self.get = self.com.recv()
        status1_g = self.get[3:4]
        if status1_g == b'0' :
            print('Gauge cannot be turned on/off')
        elif status1_g == b'1' :
            print('Gauge turned off')
        elif status1_g == b'2' :
            print('Gauge turned on')
        else :
            pass

    def gauge_off_g1(self):
        self.com.send(b"SEN , 1 , 0 \r\n")
        time.sleep(0.3)
        self.com.send(b"\x05")
        time.sleep(0.3)
        self.get = self.com.recv()
        status1_g = self.get[3:4]
        if status1_g == b'0' :
            print('Gauge cannot be turned on/off')
        elif status1_g == b'1' :
            print('Gauge turned off')
        elif status1_g == b'2' :
            print('Gauge turned on')
        else :
            pass

    def pres_unit_bar(self):
        self.com.send(b"UNI,0 \r\n")
        time.sleep(0.3)
        self.com.send(b"\x05")
        time.sleep(0.3)
        self.raw_bar = self.com.recv()
        unit = self.raw_bar[3:4]
        return unit

    def pres_unit_torr(self):
        self.com.send(b"UNI,1 \r\n")
        time.sleep(0.3)
        self.com.send(b"\x05")
        time.sleep(0.3)
        self.raw_torr = self.com.recv()
        unit = self.raw_torr[3:4]
        return unit

    def pres_unit_pa(self):
        self.com.send(b"UNI,2 \r\n")
        time.sleep(0.3)
        self.com.send(b"\x05")
        time.sleep(0.3)
        self.raw_pa = self.com.recv()
        unit = self.raw_pa[3:4]
        return unit
