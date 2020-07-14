# coding:utf_8
import time
import datetime
import sys
import socket
from ..SCPI import scpi

class PMX18_2A(scpi.scpi_family):
    manufacturer = 'KIKUSUI'
    product_name = 'PMX18'
    classification = 'Power Supply'

    _scpi_enable = '*CLS *ESE *ESR? *IDN? *OPC *OPT? *RCL *RST *SAV *SRE *STB? *TRG? *TST? *WAI'





    """
        "*IDN?"
        製品の機種名とファームウェアのバージョンを問い合わせる。

        <レスポンス>
        PMX-A:形名　PMX18-5,シリアルAB123456,IFCバージョン1.00,
        IFCビルド番号0016,IOCバージョン1.00,IOCビルド番号0015の場合
        >>> KIKUSUI,PMX18-5,AB123456,IFC01.00.0016 IOC01.00.0015
    """

    def get_ID(self):
        self.com.send('*IDN?')
        ret = self.com.readline()
        return ret


    def show_ID(self):
        res = self.get_ID()
        print( "\n Device ID : %s\n" %res)
        return True


        """
        "OUTP"
        出力のON/OFF
        設定値：ON(1)   出力オン
　　　　 OFF(0)  出力オフ
        """
    def query_output_onoff(self):
        self.com.send('OUTP?')
        time.sleep(0.05)
        ret = int(self.com.readline())
        return ret


    def set_ON(self):
        self.com.send('OUTP 1')
        return



    def set_OFF(self):
        self.com.send('OUTP 0')
        return


        """
        "CURR" "VOLT" "CURR?" "VOLT?"
        電流・電圧値の設定・問合せ
        単位：A,V
        """

    def set_curr(self,curr):
        self.com.send('CURR %s'%(curr))
        time.sleep(0.1)
        return

    def set_volt(self,vol):
        self.com.send('VOLT %s'%(vol))
        time.sleep(0.1)
        return


    def query_curr(self):
        self.com.send('MEAS:CURR?')
        ret = self.com.readline()
        ret = float(ret.rstrip("\r\n"))
        return ret

    def query_volt(self):
        self.com.send('MEAS:VOLT?')
        ret = self.com.readline()
        ret = float(ret.rstrip("\r\n"))
        return ret
