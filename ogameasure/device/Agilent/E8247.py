import time
from ..SCPI import scpi

# main class
# ==========

class E8247(scpi.scpi_family):
    manufacturer = 'Agilent'
    product_name = 'E8247'
    classification = 'Signal Generator'
    
    _scpi_enable = '*CLS *ESE *ESE? *ESR? *IDN? *OPC *OPC? *PSC? *RCL ' +\
                   '*RST *SAV *SRE *SRE? *STB? *TST? *WAI'
    
    def _error_check(self):
        #err_num, err_msg = self.error_query()
        #error_handler.check(err_num, err_msg)
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
        
        < unit : str : 'GHz','MHz','kHz','Hz' >
            Specify the units of the <freq>.
            'GHz', 'MHz', 'kHz' or 'Hz'. default = 'GHz'
        
        Returnes
        ========
        Nothing.
        
        Examples
        ========
        >>> s.freq_set(1, 'GHz')
        >>> s.freq_set(1.234, 'MHz')
        >>> s.freq_set(98765.4321, 'kHz')
        """
        self.com.send('FREQ %.10f %s'%(freq, unit))
        return
    
    def freq_query(self):
        """
        FREQ? : Query CW frequency
        --------------------------
        This command query the signal generator output frequency for the CW
        frequency mode.
        
        Args
        ====
        Nothing.
        
        Returnes
        ========
        < freq : float :  >
            A frequency value in Hz.
        
        Examples
        ========
        >>> s.freq_get()
        +2.0000000e+10
        """
        self.com.send('FREQ?')
        ret = self.com.readline()
        ret = float(ret)
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
        
        Returnes
        ========
        Nothing.
        
        Examples
        ========
        >>> s.power_set(-130)
        >>> s.power_set(-10.2, 'dBm')
        """
        self.com.send('POW %f %s'%(pow, unit))
        return
    
    def power_query(self):
        """
        POW? : Query RF output power
        ----------------------------
        This command query the RF output power.
        
        Args
        ====
        Nothing.
        
        Returnes
        ========
        < power : float :  >
            A power value in dBm.
        
        Examples
        ========
        >>> s.freq_get()
        10.1
        """
        self.com.send('POW?')
        ret = self.com.readline()
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
        
        Returnes
        ========
        Nothing.
        
        Examples
        ========
        >>> s.output_set('ON')
        >>> s.output_set(1)
        >>> s.output_set('OFF')
        >>> s.output_set(0)
        """
        self.com.send('OUTP %s'%(str(output)))
        return
    
    def output_on(self):
        """
        (Helper method) OUTP : Enable the RF output
        -------------------------------------------
        This command enables the RF output.
        
        Args
        ====
        Nothing.
        
        Returnes
        ========
        Nothing.
        
        Examples
        ========
        >>> s.output_on()
        """
        self.com.send('OUTP ON')
        return
    
    def output_off(self):
        """
        (Helper method) OUTP : Disable the RF output
        --------------------------------------------
        This command disables the RF output.
        
        Args
        ====
        Nothing.
        
        Returnes
        ========
        Nothing.
        
        Examples
        ========
        >>> s.output_off()
        """
        self.com.send('OUTP OFF')
        return
    
    def output_query(self):
        """
        OUTP? : Query RF output status
        ------------------------------
        This command queriesthe RF output status.
        
        Args
        ====
        Nothing.
        
        Returnes
        ========
        < output : int : 1,0 >
            Enable/disable the RF output.
            1 = ON, 0 = OFF
        
        
        Examples
        ========
        >>> s.output_query()
        1
        """
        self.com.send('OUTP?')
        ret = self.com.readline()
        ret = int(ret)
        return ret
    


class E8247C(E8247):
    product_name = 'E8247'
    




# ==============
# Helper Classes
# ==============

# Error Class
# ===========
class error_item(object):
    num = 0
    msg = ''
    txt = ''
    
    def __init__(self, num, msg, txt):
        self.num = num
        self.msg = msg
        self.txt = txt
        pass

class error_handler(object):
    error_list = []
    
    @classmethod
    def check(cls, num, msg):
        if num==0: return
        for e in cls.error_list:
            if msg == e.msg:
                emsg = '%s (%d)'%(e.msg, e.num)
                msg = 'Signal Generator returned Error message.\n'
                msg += '*'*len(emsg) + '\n'
                msg += emsg + '\n'
                msg += '*'*len(emsg) + '\n'
                msg += e.txt + '\n'
                raise StandardError(msg)
            continue
        _msg = 'Signal Generator returned Error message.\n'
        emsg = '%s (%d)\n'%(msg, num)
        _msg += '*'*len(emsg) + '\n'
        _msg += emsg
        _msg += '*'*len(emsg) + '\n'
        raise StandardError(_msg)
        return
    
    
