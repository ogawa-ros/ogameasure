#! /usr/bin/env python3

import time
import numpy as np

class tpg261():

#    manufacturer = ''
#    product_name = ''
#    classification = ''
    com = None
    
    def __init__(self, com):
        self.com = com
        self.com.open()
        pass

    def pressure(self):
        self.com.send(b"PR1 \r\n")
        time.sleep(0.3)
        self.com.send(b"\x05")
        time.sleep(0.3)
        self.raw_p = self.com.recv()
        pressure = np.float64(self.raw_p[5:16])
        pressure = pressure.strip("b'")
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

'''
 def pressure_both(self):
         self.com.send(b"PRX \r\n")
         time.sleep(0.3)
         self.com.send(b"\x05")
         time.sleep(0.3)
         rawb = self.com.recv()
         status1 = rawb[3:4]
         status2 = rawb[6:16]
         pressure1 = str(raw2[17:18])
         pressure2 = str(raw2[18:30])


    def gauge_change_1(self):
        self.tpg261.write(b"SEN , 2 , 1 \r\n")
        time.sleep(0.3)
        self.tpg261.write(b"\x05")
        time.sleep(0.3)
        get = self.tpg261.readline()
        status1 = str(get[0:1])
        status2 = str(get[2:3])

    def gauge_change_2(self):
        self.tpg261.write(b"SEN , 1 , 2 \r\n")
        time.sleep(0.3)
        self.tpg261.write(b"\x05")
        time.sleep(0.3)
        get = self.tpg261.readline()
        status1 = str(get[0:1])
        status2 = str(get[2:3])

    def change_gague1(self):
        self.tpg261.write(b"SCT , 0\r\n")
        time.sleep(0.3)
        self.tpg261.write(b"\x05")
        time.sleep(0.3)
        get = self.tpg261.readline()
        status = str(get[0:1])

    def change_gague2(self):
        self.tpg261.write(b"SCT , 1\r\n")
        time.sleep(0.3)
        self.tpg261.write(b"\x05")
        time.sleep(0.3)
        get = self.tpg261.readline()
        status = str(get[0:1])

    def query_error(self):
        self.tpg261.write(b"ERR \r\n")
        time.sleep(0.3)
        self.tpg261.write(b"\x05")
        time.sleep(0.3)
        get = self.tpg261.readline()
        status = str(get[0:4])

    def turn_status2(self):
        self.com.send(b"SEN , 0, 0 \r\n")
        time.sleep(0.3)
        self.com.send(b"\x05")
        time.sleep(0.3)
        self.raw_p = self.com.recv()
        gauge1 = self.raw_p[5:6]
        if gauge1 == b'0' :
            print('Gauge cannot be turned on/off')
        elif gauge1 == b'1' :
            print('Gauge turned off')
        elif gauge1 == b'2' :
            print('Gauge turned on')
        else :
            pass

    def gauge_on_g2(self):
        self.com.send(b"SEN , 0 , 2 \r\n")
        time.sleep(0.3)
        self.com.send(b"\x05")
        time.sleep(0.3)
        self.get = self.com.recv()
        status1_g = self.get[5:6]
        if status1_g == b'0' :
            print('Gauge cannot be turned on/off')
        elif status1_g == b'1' :
            print('Gauge turned off')
        elif status1_g == b'2' :
            print('Gauge turned on')
        else :
            pass

    def gauge_off_g2(self):
        self.com.send(b"SEN , 0 , 1 \r\n")
        time.sleep(0.3)
        self.com.send(b"\x05")
        time.sleep(0.3)
        self.get = self.com.recv()
        status1_g = self.get[5:6]
        if status1_g == b'0' :
            print('Gauge cannot be turned on/off')
        elif status1_g == b'1' :
            print('Gauge turned off')
        elif status1_g == b'2' :
            print('Gauge turned on')
        else :

'''
