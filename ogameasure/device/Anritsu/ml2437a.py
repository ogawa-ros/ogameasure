#! /usr/bin/env python3

import time
from ..SCPI import scpi

class ml2437a(scpi.scpi_family):

    def initilize(self, ch = 1):

        for i in range(ch):
            self.com.send('CHUNIT %d, DBM' %(i))
            self.com.send('CHRES %d, %d' %(i, resolution))

    def check(self, ch = 1):

        self.com.send('o %d' %(ch))
        ret = self.com.readline()
        mode = float(ret)
        return mode

    def measure(self, ch=1, resolution=3):
        '''
        DESCRIPTION
        ================
        This function queries the input power level.
        ARGUMENTS
        ================
        1. ch: the sensor channel number.
            Number: 1-2
            Type: int
            Default: 1
        2. resolution: the sensor order of the resolution.
            Number: 1-3
            Type: int
            Default: 3
        RETURNS
        ================
        1. power: the power value [dBm]
            Type: float
        '''
        self.com.send('O %d' %(ch))
        ret = self.com.readline()
        power = float(ret)
        return power

    def set_average_onoff(self, onoff, sensor='A'):
        '''
        DESCRIPTION
        ================
        This function switches the averaging mode.
        ARGUMENTS
        ================
        1. onoff: averaging mode
            Number: 0 or 1
            Type: int
            Default: Nothing.
        2. sensor: averaging sensor.
            Number: 'A' or 'B'
            Type: string
            Default: 'A'
        RETURNS
        ================
        Nothing.
        '''

        if onoff == 1:
            self.com.send('AVG %s, RPT, 60' %(sensor))
        else:
            self.com.send('AVG %s, OFF, 60' %(sensor))
        return

    def query_average_mode(self,ch=1):

        '''
        DESCRIPTION
        ================
        This function queries the averaging mode.
        ARGUMENTS
        ================
        1. ch: the sensor channel number.
            Number: 1-2
            Type: int
            Default: 1
        RETURNS
        ================
        1. onoff: averaging mode
            mode:  ‘0’ = OFF, ‘1’ = AUTO, ‘2’ = Moving, ‘3’ = Repeat.
            Type: string
        '''

        self.com.send('STATUS')
        ret = self.com.readline()
        if ch == 1:
            if ret[17] == '0':
                ret = "OFF"
            elif ret[17] == '1':
                ret = "AUTO"
            elif ret[17] == '2':
                ret = "Moving"
            elif ret[17] == '3':
                ret = "Repeat"
            else:
                ret = "==ERROR=="

        if ch == 2:
            if ret[18] == '0':
                ret = "OFF"
            elif ret[18] == '1':
                ret = "AUTO"
            elif ret[18] == '2':
                ret = "Moving"
            elif ret[18] == '3':
                ret = "Repeat"
            else:
                ret = "==ERROR=="
        return ret

    def set_average_count(self, count, sensor='A'):
        '''
        DESCRIPTION
        ================
        This function sets the averaging counts.
        ARGUMENTS
        ================
        1. count: averaging counts
            Type: int
            Default: Nothing.
        2. sensor: averaging sensor.
            Number: 'A' or 'B'
            Type: string
            Default: 'A'
        RETURNS
        ================
        Nothing.
        '''

        self.com.send('AVG %s, RPT, %d' %(sensor, count))

        return

    def query_average_count(self,ch=1):
        '''
        DESCRIPTION
        ================
        This function queries the averaging counts.
        ARGUMENTS
        ================
        1. ch: the sensor channel number.
            Number: 1-2
            Type: int
            Default: 1
        RETURNS
        ================
        1. count: averaging counts
            Type: int
        '''
        self.com.send('STATUS')
        if ch ==1:
            ret = self.com.readline()
            count = int(ret[19:23])
        if ch ==2:
            ret = self.com.readline()
            count = int(ret[24:28])

        return count
