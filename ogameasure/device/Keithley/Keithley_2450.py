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
        return

    def limit(self, limit): #mA
        return
    
    def source_volt(self):
        return

    def limit_volt(self, limit): #mV
        return

    def set_voltage(self, volt): #mV
        return

    def current_query(self):
        return
    
    def volt_query(self):
        return

    def creat_buf(self, buf):
        return

    def clear_buf(self, buf):
        return

    def delete_buf(self, buf):
        return

    def read_back_on(self):
        return

    def read_back_off(self):
        return

    def digits_num(self, num):
        return

    def read_num(self, count):
        return

    def read_vi(self ,buf_name):
        return

    def get_vi(self, buf_name):
        return

    def close(self):
        self.com.close()
