from ..SCPI import scpi

# helper classes
# ==============

# Channel List
# ------------
class channel_list(object):
    ch_available = []
    
    def __init__(self, ch_list):
        target_ch = []
        if type(ch_list) == str:
            ch_list = ch_list.strip('(@)')
            if ch_list.find(':') != -1:
                v1, v2 = ch_list.split(':')
                target_ch = range(int(v1), int(v2)+1)
            elif ch_list.find(',') != -1:
                v = ch_list.split(',')
                target_ch = [int(_v) for _v in v]
            else:
                target_ch = [int(ch_list)]
                pass
            pass
        elif type(ch_list) in [list, tuple]:
            target_ch = ch_list
        else:
            target_ch = [ch_list]
            pass
        self.ch = target_ch
        self._verify()
        self._make_query()
        pass
        
    def _verify(self):
        for c in self.ch:
            if not c in self.ch_available:
                raise ValueError('ch %d is not supported.'%(c))
            continue
        return
        
    def _make_query(self):
        self.query = '(@' + ','.join(['%03d'%c for c in self.ch]) + ')' 
        return

class channel_list_11713B(channel_list):
    ch_available = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]

class channel_list_11713C(channel_list):
    ch_available = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
                    201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
    
# Supply Voltage
# --------------
class switch_voltage(object):
    available = {'OFF': 0, 'P5v': 5, 'P15v': 15, 'P24v': 24, 'USER': None}
    
    def __init__(self, val):
        if type(val) == int:
            if not val in self.available.values():
                raise ValueError('voltage %d is not supported.'%(val))
            self.int = val
            self.str = [key for key, value in self.available.items() if value==val][0]
        elif type(val) == str:
            if val[0]=='P' & val[-1]!='v': val += 'v'
            if not val in self.available.keys():
                raise ValueError('voltage %s is not supported.'%(val))
            self.str = val
            self.int = self.available[val]
        else:
            raise TypeError('voltage should be specified as int or str')
        pass
            
# Bank Number
# -----------
class bank_number(object):
    available = [1, 2]
    
    def __init__(self, val):
        if type(val) == int:
            if not val in self.available:
                raise ValueError('voltage %d is not supported.'%(val))
            self.int = val
        else:
            raise TypeError('voltage should be specified as int or str')
        pass
            
# ON - OFF
# --------
class on_off(object):
    available = {'OFF': 0, 'ON': 1}
    
    def __init__(self, val):
        if type(val) in [int, bool]:
            val = int(val)
            if not val in self.available.values():
                raise ValueError('voltage %d is not supported.'%(val))
            self.int = val
            self.str = [key for key, value in self.available.items() if value==val][0]
        elif type(val) == str:
            if val[0]=='P' & val[-1]!='v': val += 'v'
            if not val in self.available.keys():
                raise ValueError('voltage %s is not supported.'%(val))
            self.str = val
            self.int = self.available[val]
        else:
            raise TypeError('voltage should be specified as int or str')
        pass
            



# main class
# ==========

class agilent_11713(scpi.scpi_family):
    manufacturer = 'Agilent'
    product_name = '11713'
    classification = 'Attenuator/Switch Driver'
    
    _scpi_enable = '*IDN?'
    
    _ch_list = channel_list
    
    def switch_open(self, ch):
        """
        :ROUTe:OPEn : Open ch(s)
        ------------------------
        Open switching path(s).
        
        Args
        ====
        < ch : ch_list  :  >
            Specify ch(s) to open.
            <ch> should be str, list of int, or int.
            
            str : Specify the ch(s) by characters.
                  Following formats are available.
                   - single ch : '101'
                   - multiple chs : '102, 104, 108'
                   - a range of chs : '101:105'
        
            list : Specify the multiple chs by a list of int.
                   e.g., [101, 102, 105]
          
            int : Specify the ch by a int value.
                  e.g., 106
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> a.switch_open('101')
        >>> a.switch_open('101, 102')
        >>> a.switch_open('101:104')
        >>> a.switch_open([101, 102])
        >>> a.switch_open(101)
        """
        ch = self._ch_list(ch)
        self.com.send(':ROUTe:OPEn %s'%(ch.query))
        return
        
    def switch_close(self, ch):
        """
        :ROUTe:CLOSe : Close ch(s)
        --------------------------
        Close switching path(s).
        
        Args
        ====
        < ch : ch_list  :  >
            Specify ch(s) to close.
            <ch> should be str, list of int, or int.
            
            str : Specify the ch(s) by characters.
                  Following formats are available.
                   - single ch : '101'
                   - multiple chs : '102, 104, 108'
                   - a range of chs : '101:105'
        
            list : Specify the multiple chs by a list of int.
                   e.g., [101, 102, 105]
          
            int : Specify the ch by a int value.
                  e.g., 106
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> a.switch_close('101')
        >>> a.switch_close('101, 102')
        >>> a.switch_close('101:104')
        >>> a.switch_close([101, 102])
        >>> a.switch_close(101)
        """
        ch = self._ch_list(ch)
        self.com.send(':ROUTe:CLOSe %s'%(ch.query))
        return

    def switch_open_all(self):
        """
        :ROUTe:OPEn:ALL : Open all chs
        ------------------------------
        Open all switching paths.
        
        Args
        ====
        Nothing
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> a.switch_open_all()
        """
        self.com.send(':ROUTe:OPEn:ALL')
        return
        
    def switch_close_all(self):
        """
        :ROUTe:CLOSe:ALL : Close all chs
        --------------------------------
        Close all switching paths.
        
        Args
        ====
        Nothing
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> a.switch_close_all()
        """
        self.com.send(':ROUTe:CLOSe:ALL')
        return
        
    def switch_open_query(self, ch):
        """
        :ROUTe:OPEn? : Query open ch(s)
        -------------------------------
        Query switching path is open.
        
        Args
        ====
        < ch : ch_list  :  >
            Specify ch(s) to check open.
            <ch> should be str, list of int, or int.
            
            str : Specify the ch(s) by characters.
                  Following formats are available.
                   - single ch : '101'
                   - multiple chs : '102, 104, 108'
                   - a range of chs : '101:105'
        
            list : Specify the multiple chs by a list of int.
                   e.g., [101, 102, 105]
          
            int : Specify the ch by a int value.
                  e.g., 106
        
        Returns
        =======
        < is_open : list(int): >
            Return a list of open_flag for each chs requested.
            0 = close, 1 = open
        
        Examples
        ========
        >>> a.switch_open_query('101')
        [1]
        
        >>> a.switch_open_query('101, 102')
        [1, 0]
        
        >>> a.switch_open_query('101:104')
        [1, 0, 1, 0]
        
        >>> a.switch_open_query([101, 102])
        [1, 0]
        
        >>> a.switch_open_query(101)
        [1]
        """
        ch = self._ch_list(ch)
        self.com.send(':ROUTe:OPEn? %s'%(ch.query))
        ret = self.com.readline()
        ret = [int(r) for r in ret.strip().split(',')]
        return ret

    def switch_close_query(self, ch):
        """
        :ROUTe:CLOSe? : Query close ch(s)
        ---------------------------------
        Query switching path is close.
        
        Args
        ====
        < ch : ch_list  :  >
            Specify ch(s) to check close.
            <ch> should be str, list of int, or int.
            
            str : Specify the ch(s) by characters.
                  Following formats are available.
                   - single ch : '101'
                   - multiple chs : '102, 104, 108'
                   - a range of chs : '101:105'
        
            list : Specify the multiple chs by a list of int.
                   e.g., [101, 102, 105]
          
            int : Specify the ch by a int value.
                  e.g., 106
        
        Returns
        =======
        < is_close : list(int): >
            Return a list of close_flag for each chs requested.
            0 = open, 1 = close
        
        Examples
        ========
        >>> a.switch_close_query('101')
        [0]
        
        >>> a.switch_close_query('101, 102')
        [0, 1]
        
        >>> a.switch_close_query('101:104')
        [0, 1, 0, 1]
        
        >>> a.switch_close_query([101, 102])
        [0, 1]
        
        >>> a.switch_close_query(101)
        [0]
        """
        ch = self._ch_list(ch)
        self.com.send(':ROUTe:CLOSe? %s'%(ch.query))
        ret = self.com.readline()
        ret = [int(r) for r in ret.strip().split(',')]
        return ret
        
    def supply_voltage_set(self, voltage, bank=1):
        """
        :CONFigure:BANKn : Set Supply Voltage
        -------------------------------------
        Set the supply voltage for specified bank.
        
        Args
        ====
        < voltage : switch_voltage  :  >
            Specify the voltage to apply.
            <voltage> should be str, or int.
            
            str : Specify the voltage by characters.
                  voltage = 'OFF', 'P5v', 'P15v', 'P24v', or 'USER'
            
            int : Specify the voltage by a int value.
                  0 = OFF,  5 = P5v,  15 = P15v,  24 = P24v
        
        < bank : int : 1,2 >
            Specify the bank to apply the voltage.
            bank = 1 or 2. default is bank = 1.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> a.switch_supply_voltage_set('P24v')
        >>> a.switch_supply_voltage_set(5)
        >>> a.switch_supply_voltage_set('P24v', bank=2)
        """
        voltage = switch_voltage(voltage)
        bank = bank_number(bank)
        self.com.send('CONFigure:BANK%d %s'%(bank.int, voltage.str))
        return
    
    def supply_voltage_query(self, bank=1):
        """
        :CONFigure:BANKn? : Query Supply Voltage
        -----------------------------------------
        Query the supply voltage for specified bank.
        
        Args
        ====
        < bank : int : 1,2 >
            Specify the bank to check the voltage.
            bank = 1 or 2. default is bank = 1.
        
        Returns
        =======
        < voltage : str : 'OFF', 'P5', 'P15', 'P24', 'USER' >
            Return voltage which is applyed to the switch.
            <voltage> is 'OFF', 'P5', 'P15', 'P24', or 'USER'.
        
        Examples
        ========
        >>> a.switch_supply_voltage_query()
        'P24'
        
        >>> a.switch_supply_voltage_query(bank=2)
        'P5'
        """
        bank = bank_number(bank)
        self.com.send('CONFigure:BANK%d?'%(bank.int))
        ret = self.com.readline().strip()
        return ret
        
    def switch_ttl_on_off(self, ttl, bank=1):
        """
        :CONFigure:BANKn:TTL : Set TTL ON/OFF
        -------------------------------------
        Set TTL ON/OFF for specified bank.
        
        Args
        ====
        < ttl : on_off  : 0,1,'ON,'OFF',True,False  >
            Specify the TTL ON/OFF.
            <ttl> should be str, int, or bool.
            
            str : ttl = 'ON', or 'OFF'            
            int : 1 = 'ON', or 0 = 'OFF'
            bool: True = 'ON', or False = 'OFF'

        < bank : int : 1,2 >
            Specify the bank to configure TTL.
            bank = 1 or 2. default is bank = 1.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> a.switch_ttl_on_off('ON')
        >>> a.switch_ttl_on_off(0, bank=2)
        """
        ttl = on_off(ttl)
        bank = bank_number(bank)
        self.com.send('CONFigure:BANK%d:TTL %s'%(bank.int, ttl.str))
        return
        
    def switch_ttl_on_off_query(self, bank=1):
        """
        :CONFigure:BANKn:TTL? : Query TTL ON/OFF
        ----------------------------------------
        Query TTL ON/OFF for specified bank.
        
        Args
        ====
        < bank : int : 1,2 >
            Specify the bank to configure TTL.
            bank = 1 or 2. default is bank = 1.
        
        Returns
        =======
        < ttl : int  : 0,1 >
            Return TTL ON/OFF.
            0 = OFF,  1 = ON
        
        Examples
        ========
        >>> a.switch_ttl_on_off_query()
        0
        
        >>> a.switch_ttl_on_off_query(bank=2)
        1
        """
        bank = bank_number(bank)
        self.com.send('CONFigure:BANK%d:TTL?'%(bank.int))
        ret = self.com.readline()
        ret = int(ret)
        return ret
        
    def relay_cycles_query(self, ch):
        """
        :DIAGnostic:RELay:CYCles? : Query Number of Relay Cycles
        --------------------------------------------------------
        Query the number of relay cycles for each channel.
        
        Args
        ====
        < ch : ch_list  :  >
            Specify ch(s) to check the number of relay cycles.
            <ch> should be str, list of int, or int.
            
            str : Specify the ch(s) by characters.
                  Following formats are available.
                   - single ch : '101'
                   - multiple chs : '102, 104, 108'
                   - a range of chs : '101:105'
        
            list : Specify the multiple chs by a list of int.
                   e.g., [101, 102, 105]
          
            int : Specify the ch by a int value.
                  e.g., 106
        
        Returns
        =======
        < number_of_cycles : list(int): >
            Return a list of number of cycles for each ch.
        
        Examples
        ========
        >>> a.relay_cycles_query('101')
        [123]
        
        >>> a.relay_cycles_query('101, 102')
        [123, 103]
        
        >>> a.relay_cycles_query('101:104')
        [123, 103, 43, 28]
        
        >>> a.relay_cycles_query([101, 102])
        [123, 103]
        
        >>> a.relay_cycles_query(101)
        [123]
        """
        ch = self._ch_list(ch)
        self.com.send(':DIAGnostic:RELay:CYCles? %s'%(ch.query))
        ret = self.com.readline()
        ret = [int(r) for r in ret.strip().split(',')]
        return ret
        
    def relay_cycles_clear(self, ch):
        """
        :DIAGnostic:RELay:CLEAr : Clear Relay Cycles
        --------------------------------------------
        Clear the number of relay cycles for each channel.
        
        Args
        ====
        < ch : ch_list  :  >
            Specify ch(s) to clear the number of relay cycles.
            <ch> should be str, list of int, or int.
            
            str : Specify the ch(s) by characters.
                  Following formats are available.
                   - single ch : '101'
                   - multiple chs : '102, 104, 108'
                   - a range of chs : '101:105'
        
            list : Specify the multiple chs by a list of int.
                   e.g., [101, 102, 105]
          
            int : Specify the ch by a int value.
                  e.g., 106
        
        Returns
        =======
        Nothing
        
        Examples
        ========
        >>> a.relay_cycles_clear('101')
        >>> a.relay_cycles_clear('101, 102')
        >>> a.relay_cycles_clear('101:104')
        >>> a.relay_cycles_clear([101, 102])
        >>> a.relay_cycles_clear(101)
        """
        ch = self._ch_list(ch)
        self.com.send(':DIAGnostic:RELay:CLEAr %s'%(ch.query))
        return 
        
    
        
    _shortcut_command = {'OPEn': 'switch_open',
                         'CLOSe': 'switch_close',
                         'OPEnALL': 'switch_open_all',
                         'CLOSeALL': 'switch_close_all',
                         'OPEnQ': 'switch_open_query',
                         'CLOSeQ': 'switch_close_query',  
                         'BANK': 'supply_voltage_set', 
                         'BANKQ': 'supply_voltage_query',    
                         'TTL': 'switch_ttl_on_off',
                         'TTLQ': 'switch_ttl_on_off_query',
                         'CYClesQ': 'relay_cycles_query',
                         'RELayCLEAr': 'relay_cycles_clear'}


class agilent_11713B(agilent_11713):
    product_name = '11713B'
    _ch_list = channel_list_11713B
    
class agilent_11713C(agilent_11713):
    product_name = '11713C'
    _ch_list = channel_list_11713C
    
