import time
from ..SCPI import scpi

delay_time = 0.1

class Keithley_2450(scpi.scpi_family):
    manufacturer = "Keithley"
    product_name = "2450"
    classification = "Source Meter"

    def f_wire(self):
        self.com.send(":SENSe:CURRent:RSENse ON\n")
        return

    def output_on(self):
        self.com.send(":OUTP ON\n")
        return

    def output_off(self):
        self.com.send(":OUTP OFF\n")
        return

    def source_delay(self, delay) :
        self.com.send("SOUR:VOLT:DEL %f\n"%delay)
        return

    def limit(self, limit): #mA
        limit = limit / 1000
        self.com.send(":SOURce:VOLTage:ILIMit %f\n"%limit)
        return
    
    def source_volt(self):
        self.com.send("SOUR:FUNC VOLT\n")
        return

    def limit_volt(self, limit): # mV
        limit = limit / 1000
        self.com.send("SOUR:VOLT:PROT PROT%f\n"%limit)
        return

    def set_voltage(self, volt): # mV
        volt = volt / 1000
        self.com.send(":SOURce:VOLT %f\n"%volt)
        return

    def current_query(self): # uA
        self.com.send(":MEASure:CURRent?\n")
        time.sleep(delay_time)
        ret = self.com.readline()
        ret = float(ret) * 1000000
        return ret
    
    def voltage_query(self): # mV
        self.com.send(":MEASure:VOLTage?\n")
        time.sleep(delay_time)
        ret = self.com.readline()
        ret = float(ret) * 1000
        return ret

    def creates_buf(self, buf):
        self.com.send("""TRAC:MAKE "%s", 1000000\n"""%buf)
        return

    def clear_buf(self, buf):
        self.com.send(""":TRACe:CLEar "%s"\n"""%buf)
        return

    def delete_buf(self, buf):
        self.com.send(""":TRACe:DELete "%s"\n"""%buf)
        return

    def read_back_on(self):
        self.com.send("SOUR:VOLT:READ:BACK ON\n")
        return

    def read_back_off(self):
        self.com.send("SOUR:VOLT:READ:BACK OFF\n")
        return

    def digits_num(self, num):
        self.com.send(":FORMat:ASCii:PRECision %f\n"%num)
        return

    def read_num(self, count):
        self.com.send("COUNT %f\n"%count)
        return

    def read_vi(self ,buf_name):
        self.com.send("""READ? "%s", SOUR, READ\n"""%buf_name)
        return

    def get_vi(self, buf_name):
        self.com.send("""TRAC:DATA? 1, 10, "%s", SOUR, READ\n"""%buf_name)
        time.sleep(delay_time)
        ret = self.com.readline()
        return ret

    def close(self):
        self.com.close()
