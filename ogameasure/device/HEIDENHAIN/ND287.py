#! /usr/bin/env python3
import serial
import time,sys,os
import math
import datetime

class ND287(object):

    def __init__(self, port):
        self._enc = self.serial_open(port)
        return

    def serial_open(self, port):
        _enc = serial.Serial(port,parity="E",stopbits=2, bytesize=7)
        return _enc

    def write(self, cmd):
        self._enc.write(cmd)
        return

    def read(self, byte=100):
        res = self._enc.readline()
        return res

    def query(self,cmd,wt=0.001):
        self.write(cmd)
        time.sleep(wt)
        ret = self.read()
        return ret

    def press_key(self,key):
        if key == "0":
            self.write(b"\x1BT0000\r")
        elif key == "1":
            self.write(b"\x1BT0001\r")
        elif key == "2":
            self.write(b"\x1BT0002\r")
        elif key == "3":
            self.write(b"\x1BT0003\r")
        elif key == "4":
            self.write(b"\x1BT0004\r")
        elif key == "5":
            self.write(b"\x1BT0005\r")
        elif key == "6":
            self.write(b"\x1BT0006\r")
        elif key == "7":
            self.write(b"\x1BT0007\r")
        elif key == "8":
            self.write(b"\x1BT0008\r")
        elif key == "9":
            self.write(b"\x1BT0009\r")
        elif key == "CLR":
            self.write(b"\x1BT0100\r")
        elif key == "-":
            self.write(b"\x1BT0101\r")
        elif key == ".":
            self.write(b"\x1BT0102\r")
        elif key == "NAVI":
            self.write(b"\x1BT0103\r")
        elif key == "ENT":
            self.write(b"\x1BT0004\r")
        elif key == "up":
            self.write(b"\x1BT0005\r")
        elif key == "down":
            self.write(b"\x1BT0006\r")
        elif key == "soft1":
            self.write(b"\x1BT0007\r")
        elif key == "soft2":
            self.write(b"\x1BT0008\r")
        elif key == "soft3":
            self.write(b"\x1BT0009\r")
        elif key == "soft4":
            self.write(b"\x1BT0010\r")
        else:
            pass

    def output_device_identification(self):
        """
        Return
        1 Device nameID
        2 number of the currently installed software
        3 Version number of the currently installed software
        """
        info = self.query(b"\x1BA0000\r")
        return info

    def output_position_display_value(self):
        position = self.query(b"\x1BA0100\r")
        return position

    def output_current_position(self):
        position = self.query(b"\x1BA0200\r")
        return position

    def output_error_message(self):
        error = self.query(b"\x1BA0301\r")
        return error

    def output_software_ID_number(self):
        software_id = self.query(b"\x1BA0400\r")
        return software_id

    def output_status_bar(self):
        """
        Return: a b c d e f g h
        a: Operating mode
            0 = Actual Value
            1 = Distance- To-Go
        b: Display mode for axis and coupled axes
            0 = X1
            1 = X2
            2 = X1 + X2
            3 = X1 - X2
            4 = f(X1, X2)
        c: Scale factor
            0 = Not active
            1 = Active
        d: Compensation
            0 = No compensation
            1 = Error compensation or axis-error compensation is active
        e: Stopwatch
            0 = Stopped
            1 = Stopwatch is running
        f: Unit of measure
            0 = mm
            1 = inches
            2 = DEG
            3 = DMS
            4 = rad
        g: Datum
            1 = Datum1
            2 = Datum 2
        h: Soft-key page
            1 = Page 1
            2 = Page 2
            3 = Page 3
            4 = Keyboard is locked
        """
        bar = self.query(b"\x1BA0800\r")
        return bar

    def output_status_indicators(self):
        indicator = self.query(b"\x1BA0900\r")
        return indicator

    def toggle_REF_function(self):
        indicator = self.query(b"\x1BF0000\r")
        return indicator

    def start_measurement_series_SPC(self):
        indicator = self.query(b"\x1BF0100\r")
        return indicator

    def Print(self):
        indicator = self.query(b"\x1BF0200\r")
        return indicator

    def reset_position_display(self):
        indicator = self.query(b"\x1BS0000\r")
        return indicator

    def lock_keypad(self):
        indicator = self.query(b"\x1BS0001\r")
        return indicator

    def release_keypad(self):
        indicator = self.query(b"\x1BS0002\r")
        return indicator
