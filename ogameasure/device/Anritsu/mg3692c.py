import time
from ..SCPI import scpi

# main class
# ==========

delay_time = 0.1


class InvalidRangeError(Exception):
    pass


class mg3692c(scpi.scpi_family):
    manufacturer = "Anritsu"
    product_name = "MG3692C"
    classification = "Signal Generator"

    _scpi_enable = "*IDN? *RCL *RST"

    freq_range_ghz = (2, 20)
    power_default_dbm = 0
    power_range_dbm = (-20, 30)

    def freq_set(self, freq, unit="GHz"):
        self.com.send("FREQ:CW %.10f %s" % (freq, unit))
        return

    def freq_query(self):
        self.com.send("FREQ:CW?")
        ret = self.com.readline()
        freq = float(ret)

        return freq

    def power_set(self, power=-20.0):
        if -20.0 <= power <= 30.0:
            self.com.send("POW %f dBm" % (power))
        else:
            msg = "Power range is -20.0[dBm] -- 30.0[dBm],"
            msg += " while {}[dBm] is given.".format(power)
            raise InvalidRangeError(msg)
        return

    def power_query(self):
        self.com.send("POW?")
        ret = self.com.readline()
        power = float(ret)
        return power

    def output_on(self):
        self.com.send("OUTP ON")
        return

    def output_off(self):
        self.com.send("OUTP OFF")
        return

    def output_query(self):
        self.com.send("OUTP?")
        ret = self.com.readline()
        ret = int(ret)

        return ret

    def close(self):
        self.com.close()
