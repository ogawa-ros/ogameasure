import sys
import time
import socket
import numpy
import ogameasure
from ..SCPI import scpi


# ==============
# Helper Classes
# ==============

# Bias Hex Changer
# ================
class bias_changer(object):
    min = 0
    max = 1

    def __init__(self, bias=None, hex=None):
        self.bins = numpy.linspace(self.min, self.max, 0x1000)
        self.th = (self.bins + (abs(self.bins[1]-self.bins[0])/2.))[:-1]
        if bias is not None:
            self.bias = bias
            self.digit = numpy.digitize([bias], self.th)[0]
        elif hex is not None:
            if type(hex) == str: self.digit = int(hex, 16)
            elif type(hex) == int: self.digit = hex
            self.bias = self.bins[self.digit]
        else:
            raise ValueError
        self.hexstr = '%04X'%(self.digit)
        pass

class bias_changer_100(bias_changer):
    min = 0
    max = 100

class bias_changer_200(bias_changer):
    min = 0
    max = 200


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
    error_list = [
        error_item(-100, 'Command error', ''),
        error_item(-200, 'Execution error', ''),
        error_item(-400, 'Query error', ''),
        error_item(-350, 'Queue overflow', ''),
    ]

    @classmethod
    def check(cls, num, msg):
        if num==0: return
        for e in cls.error_list:
            if msg == e.msg:
                emsg = '%s (%d)'%(e.msg, e.num)
                msg = 'Power meter returned Error message.\n'
                msg += '*'*len(emsg) + '\n'
                msg += emsg + '\n'
                msg += '*'*len(emsg) + '\n'
                msg += e.txt + '\n'
                raise StandardError(msg)
            continue
        _msg = 'Power meter returned Error message.\n'
        emsg = '%s (%d)\n'%(msg, num)
        _msg += '*'*len(emsg) + '\n'
        _msg += emsg
        _msg += '*'*len(emsg) + '\n'
        raise StandardError(_msg)
        return


# ==========
# main class
# ==========

class GPDVC15(scpi.scpi_family):
    manufacturer = 'ELVA-1'
    product_name = 'GPDVC-15'
    classification = 'Attenuator Driver'

    _scpi_enable = '*IDN? *SAV'

    _bias_changer = bias_changer

    def gpib_address_search(self):
        print('GPIB Address Searching...')
        for i in range(31):
            sys.stdout.write('\r try address %d ...   '%(i))
            sys.stdout.flush()
            com = ogameasure.gpib_prologix(self.com.com.host, i)
            try:
                com.com.timeout = 1.2
                com.open()
                com.send('*IDN?')
                com.readline()
            except socket.timeout:
                com.close()
                sys.stdout.write('\x08\x08NG')
                sys.stdout.flush()
                time.sleep(0.1)
                continue
            sys.stdout.write('\x08\x08OK\n')
            sys.stdout.flush()
            com.close()
            return i
        return

    def _error_check(self):
        err_num, err_msg = self.error_query()
        error_handler.check(err_num, err_msg)
        return

    def error_query(self):
        """
        SYST:ERR? : Query Error Numbers
        -------------------------------
        Querry error number.

        Args
        ====
        Nothing.

        Returns
        =======
        < err_num : int :  >
            Error number. 0 = 'No Error'

        < err_msg : str :  >
            Error message.

        Examples
        ========
        >>> a.error_query()
        (0, 'No error.')
        """
        self.com.send('SYST:ERR?')
        ret = self.com.readline()
        ret = ret.strip().split(',')
        err_num = int(ret[0])
        err_msg = ret[1].strip('"')
        return err_num, err_msg

    def version_query(self):
        """
        SYST:VERS : Query Version
        -------------------------
        Querry Version

        Args
        ====
        Nothing.

        Returns
        =======
        < version : float :  >
            Version of the system.

        Examples
        ========
        >>> a.version_query()
        1994.0
        """
        self.com.send('SYST:VERS?')
        ret = self.com.readline()
        self._error_check()
        ret = float(ret)
        return ret

    def gpib_address_set(self, gpib_address):
        """
        SYST:COMM:GPIB:ADDR : Set GPIB Address
        --------------------------------------
        Set GPIB Address.

        NOTE : After executed this command, reconnect the GPIB connection
               to continue communications.

        NOTE : To save the changed configurations, please execute '*SAV 0'
               command.

        Args
        ====
        < gpib_address : int :  >
            Specify the GPIB address to set.

        Returns
        =======
        Nothing.

        Examples
        ========
        >>> a.gpib_address_set(4)
        """
        self.com.send('SYST:COMM:GPIB:ADDR %d'%(gpib_address))
        return

    def gpib_address_query(self):
        """
        SYST:COMM:GPIB:ADDR? : Query GPIB Address
        -----------------------------------------
        Query GPIB Address.

        Args
        ====
        Nothing.

        Returns
        =======
        < gpib_address : int :  >
            GPIB address.

        Examples
        ========
        >>> a.gpib_address_set(4)
        """
        self.com.send('SYST:COMM:GPIB:ADDR?')
        ret = self.com.readline()
        self._error_check()
        ret = int(ret)
        return ret

    def output_set(self, output):
        """
        PO : Set Output Current
        -----------------------
        Set the output current by mA.

        Args
        ====
        < output : float : (mA) >
            Specify the bias current to output.
            unit is mA

        Returns
        =======
        Nothing.

        Examples
        ========
        >>> a.output_set(0)
        >>> a.output_set(10.1)
        """
        output = self._bias_changer(bias=output)
        self.com.send('PO %s'%(output.hexstr))
        self.output = output
        return

    def output_get(self):
        """
        Get the output current.

        Args
        ====
        Nothing.

        Returns
        =======
        < output : float : (mA) >
            Bias current. Unit is mA.

        Examples
        ========
        >>> a.output_get()
        10.234
        """
        return self.output.bias


class GPDVC15_100(GPDVC15):
    _bias_changer = bias_changer_100

class GPDVC15_200(GPDVC15):
    _bias_changer = bias_changer_200
