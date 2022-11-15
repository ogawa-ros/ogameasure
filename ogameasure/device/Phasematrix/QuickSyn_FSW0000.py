import time
from socket import timeout
from ..SCPI import scpi

# main class
# ==========

delay_time = 0.1

class FSW0000(scpi.scpi_family):
    manufacturer = 'Phase Matrix'
    product_name = 'QuickSyn FSW Series'
    classification = 'Signal Generator'

    _scpi_enable = '*IDN? *RCL *RST'

    def _error_check(self):
        return

    def freq_set(self, freq, unit='GHz'):
        """
        FREQ : Set CW frequency
        -----------------------
        This command sets the signal generator output frequency for the CW
        frequency mode.

        Args
        ====
        < freq : float :  >
            A frequency value.

        < unit : str : 'GHz','MHz','kHz','mlHz' >
            Specify the units of the <freq>.
            'GHz', 'MHz', 'kHz' or 'mlHz'. default = 'GHz'

        Returns
        =======
        Nothing.

        Examples
        ========
        >>> s.freq_set(1, 'GHz')
        >>> s.freq_set(1.234, 'MHz')
        >>> s.freq_set(98765.4321, 'kHz')
        """
        self.com.send('FREQ {0}{1}\n'.format(freq, unit))
        time.sleep(delay_time)
        try:
            ret = self.com.recv()
            if b"Data out of range" in ret:
                raise ValueError(ret)
        except timeout:
            pass

    def freq_query(self):
        """
        FREQ? : Query CW frequency
        --------------------------
        This command query the signal generator output frequency for the CW
        frequency mode.

        Args
        ====
        Nothing.

        Returns
        ========
        < freq : float :  >
            A frequency value in Hz.

        Examples
        ========
        >>> s.freq_query()
        +2.0000000e+10
        """
        self.com.send('FREQ?\n')
        time.sleep(delay_time)
        ret = self.com.recv()
        ret = float(ret)
        ret = ret / 1000.
        return ret

    def power_set(self, pow, unit='dBm'):
        """
        POW : Set RF output power
        -------------------------
        This command sets the RF output power.

        Args
        ====
        < pow : float :  >
            A output power value.

        < unit : str : 'dBm'>
            Specify the units of the <pow>.
            'dBm'. default = 'dBm'

        Returns
        =======
        Nothing.

        Examples
        ========
        >>> s.power_set(-130)
        >>> s.power_set(-10.2, 'dBm')
        """
        self.com.send('POW {0:f} {1}\n'.format(pow, unit))
        return

    def power_query(self):
        """
        POW? : Query RF output power
        ----------------------------
        This command query the RF output power.

        Args
        ====
        Nothing.

        Returns
        =======
        < power : float :  >
            A power value in dBm.

        Examples
        ========
        >>> s.power_query()
        10.1
        """
        self.com.send('POW?\n')
        time.sleep(delay_time)
        ret = self.com.recv()
        ret = float(ret)
        return ret

    def output_set(self, output):
        """
        OUTP : Enable/disable RF output
        -------------------------------
        This command enables or disables the RF output. Although you can
        configure and engage various modulations, no signal is available at
        the RF OUTPUT connector until this command is executed.

        Args
        ====
        < output : str,int : 'ON','OFF',1,0 >
            Enable/disable the RF output.

        Returns
        =======
        Nothing.

        Examples
        ========
        >>> s.output_set('ON')
        >>> s.output_set(1)
        >>> s.output_set('OFF')
        >>> s.output_set(0)
        """
        self.com.send('OUTP:STAT {0}\n'.format(str(output)))
        return

    def output_on(self):
        """
        (Helper method) OUTP : Enable the RF output
        -------------------------------------------
        This command enables the RF output.

        Args
        ====
        Nothing.

        Returns
        =======
        Nothing.

        Examples
        ========
        >>> s.output_on()
        """
        self.com.send('OUTP:STAT ON\n')
        return

    def output_off(self):
        """
        (Helper method) OUTP : Disable the RF output
        --------------------------------------------
        This command disables the RF output.

        Args
        ====
        Nothing.

        Returns
        =======
        Nothing.

        Examples
        ========
        >>> s.output_off()
        """
        self.com.send('OUTP:STAT OFF\n')
        return

    def output_query(self):
        """
        OUTP? : Query RF output status
        ------------------------------
        This command queriesthe RF output status.

        Args
        ====
        Nothing.

        Returns
        =======
        < output : int : 1,0 >
            Enable/disable the RF output.
            1 = ON, 0 = OFF


        Examples
        ========
        >>> s.output_query()
        1
        """
        self.com.send('OUTP:STAT?\n')
        time.sleep(delay_time)
        ret = self.com.readline()
        if ret.upper().find('ON') != -1: ret = 1
        elif ret.upper().find('OFF') != -1: ret = 0
        else: ret = -1
        return ret

    def use_internal_reference_source(self):
        self.com.send('ROSC:SOUR INT')
        return

    def use_external_reference_source(self):
        self.com.send('ROSC:SOUR EXT')
        return

    def reference_source_query(self):
        self.com.send('ROSC:SOUR?\n')
        time.sleep(delay_time)
        ret = self.com.readline().strip()
        return ret

    def close(self):
        self.com.close()


class FSW0010(FSW0000):
    product_name = 'FSW-0010'

class FSW0020(FSW0000):
    product_name = 'FSW-0020'
