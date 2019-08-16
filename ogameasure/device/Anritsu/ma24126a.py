import serial
import time,sys,os
import math
import datetime

class ma24126a(object):

    rtimeout = 0.1
    wtimeout = 0.1

    def __init__(self, port):
        self._pm = self.serial_open(port)
        return

    def serial_open(self, port):
        _pm = serial.Serial(port, timeout = self.rtimeout, write_timeout = self.wtimeout)
        return _pm

    def send(self, cmd):
        self._pm.write(cmd)
        return

    def read(self, byte=100):
        res = self._pm.read(byte)
        return res

    def quary(self,cmd,wt=0.001):
        self.send(cmd)
        time.sleep(wt)
        ret = self.read()
        return ret

    def quary2(self,cmd,wt):
        self.send(cmd)
        time.sleep(wt)
        ret = self.read()
        return ret

    def wait_ok(self,cmd,mergin,lt):
        self.send(cmd)
        t=0
        while True :
            if self.read() == b"OK\n": break
            else:
                time.sleep(mergin)
                t = t+mergin
                if t > lt:
                    print("ERROR. Maybe too long time passed")
                    sys.exit()

    def start(self):
        ret = self.quary(b"START\n")
        if ret == b"OK\n": pass
        else: sys.exit()
        return True

    def zero_set(self):
        self.start()
        self.wait_ok(b"ZERO\n",0.5,25)
        return True

    def close(self):
        self.read()
        self._pm.close()
        return

    def power(self):
        ret = self.quary(b"PWR?\n")
        return ret

    def power_cnt(self,count,mergin):
        a = 0
        while a < count:
            st = time.time()
            self.send(b"PWR?\n")
            ft = time.time()
            tt = mergin - (st-ft)
            time.sleep(tt)
            a = a+1
        ret = self.read(10*count)
        return ret

    def change_avetyp(self,avty):
        """
    	平均化タイプを変更するメソッド
		0 - Moving
		1 - Repeat mode ON
        """
        if avty == 0 or avty == 1 :
            self.wait_ok(b"AVGTYP %d\n"%avty,0.01,3)
        else :
            print(" Invalid value. Use only 0 or 1 ")
            sys.exit()

        ret2 = self.check_avetyp()
        if int(ret2) == avty :
            print("Success to change average type")
        else :
            print("Fail to change average type")
            sys.exit()
        return True


    def check_avetyp(self):
        ret = self.quary(b"AVGTYP?\n")
        return ret

    def change_avemode(self,avmd) :
        """
        自動平均モードのオンオフを設定できるメソッド
        表示されるパワー測定値の安定と合理的な安定時間とのバランスを取った平均化回数がセンサによって選択され　
		0 - OFF
		1 - ON
        """
        if avmd == 0 or avmd == 1 :
            self.wait_ok(b"AUTOAVG %d\n"%avmd,0.01,3)
        else :
            print("Invalid value. Use only 0 or 1 ")
            sys.exit()

        ret = self.check_avemode()
        if int(ret) == avmd : pass
        else :
            print("Fail to change average mode")
            sys.exit()
        return True

    def check_avemode(self):
        ret = self.quary(b"AUTOAVG?\n")
        return ret

    def change_avecnt(self,num):
        """
        平均化回数を設定できるメソッド（デフォは１）
        ※自動平均モードをオフにしなければ変更できない。
        """
        self.change_avemode(0)
        if 1 <= num <= 40000 and type(num) == int:
            self.wait_ok(b"AVGCNT %d\n"%num,0.01,3)
        else :
            print("Invalid value. Use only integer 1~40000 ")
            sys.exit()

        ret = self.check_avecnt()
        if int(ret) == num : pass
        else :
            print("Fail to set average count.")
            sys.exit()
        return True

    def check_avecnt(self):
        ret = self.quary(b"AVGCNT?\n")
        return ret

    def change_capt(self,capt):
        """
        開口時間を変更するメソッド
        0.01以下の値は拒否
        """
        a = capt - round(capt,2)
        if 0.01 <= capt <= 300.00 and a == 0 :
            self.wait_ok(b"CHAPERT %.2f\n"%capt,0.01,3)
        else :
            print("Invalid value. Use only 0.01~300.00ms.")
            sys.exit()

        ret = self.check_capt()
        if float(ret) == capt : pass
        else :
            print("Fail to change capture time.")
            sys.exit()
        return True

    def change_capt2(self,capt):
        """
        開口時間を変更するメソッド
        0.01以下の値はパワーメータが自動的に四捨五入
        """
        a = capt - round(capt,2)
        if 0.01 <= capt <= 300.00 and a == 0 :
            self.wait_ok(b"CHAPERT %.2f\n"%capt,0.01,3)
        elif 0.01 <= capt <= 300.00 :
            print("capture time was rounded off ")
            capt = round(capt,2)
            pass
        else :
            print("Invalid value. Use only 0.01~300.00ms.")
            sys.exit()

        ret = self.check_capt()
        if float(ret) == capt : pass
        else :
            print("Fail to change capture time.")
            sys.exit()
        return True

    def check_capt(self):
        ret = self.quary(b"CHAPERT?\n")
        return ret


    def change_mode(self,mode):
        """
        パワーセンサのモードを変更するメソッド
		0 - Continuous Average Mode
        1 - Time Slot Mode
    	2 - Scope Mode
		3 - Idle Mode
        """
        if 0 <= mode <= 3 and type(mode) == int :
            self.wait_ok(b"CHMOD %d\n"%mode,0.01,3)
        else :
            print("Invalid value. Use only 0,1,2,3 ")
            sys.exit()

        ret = self.check_mode()
        if int(ret) == mode: pass
        else :
            print("Fail to change mode.")
            sys.exit()
        return True

    def check_mode(self):
        ret = self.quary(b"CHMOD?\n")
        return ret

    def change_freq(self,freq):
        """
        校正係数周波数を変換するメソッド
        0.01以下の数値は拒否
		"""
        a = freq - round(freq,2)
        if 0.01 <= freq <= 26.00 and  a == 0 :
            self.wait_ok(b"FREQ %.2f\n"%freq,0.01,3)
        else :
            print("Invalid value. Use only 0.01 <= freq <= 26.00 GHz")
            sys.exit()

        ret = self.check_freq()
        if float(ret) == freq : pass
        else :
            print(" Fail to change frequancy.")
            sys.exit()

        return True

    def change_freq2(self,freq):
        """
        開口時間を変更するメソッド
        0.01以下の値はパワーメータが自動的に四捨五入
        """
        a = freq - round(freq,2)
        if 0.01 <= freq <= 26.00 and  a == 0 :
            self.wait_ok(b"FREQ %.2f\n"%freq,0.01,3)
        elif 0.01 <= freq <= 26.00 :
            print("freq was rounded off.")
            freq = round(freq,2)
            pass
        else :
            print("Invalid value. Use only 0.01 <= freq <= 26.00 GHz")
            sys.exit()

        ret = self.check_freq()
        if float(ret) == freq : pass
        else :
            print(" Fail to change frequancy.")
            sys.exit()

        return True


    def check_freq(self):
        ret = self.quary(b"FREQ?\n")
        return ret
