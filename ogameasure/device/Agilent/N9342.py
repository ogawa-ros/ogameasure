import time
import datetime
import numpy
from ..SCPI import scpi

# main class
# ==========

class N9342(scpi.scpi_family):
    manufacturer = 'Agilent'
    product_name = 'N9342'
    classification = 'Spectrum Analyzer'
    
    _scpi_enable = '*CLS *ESE *ESR? *IDN? *OPC *OPT? *RST ' +\
                   '*SRE *STB? *TST? *WAI'
    
    def _error_check(self):
        err_num, err_msg = self.error_query()
        error_handler.check(err_num, err_msg)
        return
    
    def error_query(self):
        """
        SYST:ERR? : Query System Error
        ------------------------------
        Use this command to read the system error information.
        
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
        >>> p.error_query()
        (0, 'No error.')
        """
        self.com.send('SYST:ERR?')
        ret = self.com.readline()
        ret = ret.strip().split(',')
        err_num = int(ret[0])
        err_msg = ret[1].strip('"')
        return err_num, err_msg
        
    def installed_option_query(self):
        """
        SYST:OPT? : Installed Option Query
        ----------------------------------
        This command returns a list of the options that are installed.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < options : list(str) :  >
            A list of the options that are installed.
                
        Examples
        ========
        >>> s.installed_option_query()
        ['']
        """
        self.com.send('SYST:OPT?')
        ret = self.com.readline()
        self._error_check()
        ret = ret.strip().split(',')
        return ret
        
    def system_time_set(self, h, m, s):
        """
        SYST:TIME : Set System Time
        ---------------------------
        Sets the system time of the instrument with <"hhmmss">.
        Hour must be an integer 0 to 23.
        Minute must be an integer 0 to 59.
        Second must be an integer 0 to 59.
        
        Args
        ====
        < h : int : 0-23 >
            Hour to set.
        
        < m : int : 0-23 >
            Minute to set.
        
        < s : int : 0-23 >
            Second to set.
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.system_time_set(12, 10, 15)
        """
        settime = '%02d%02d%02d'%(h, m, s)
        self.com.send('SYST:TIME "%s"'%(settime))
        self._error_check()
        return

    def system_time_query(self):
        """
        SYST:TIME? : Query System Time
        ------------------------------
        Query the system time of the instrument.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < h : int : 0-23 >
            Hours.
        
        < m : int : 0-23 >
            Minutes.
        
        < s : int : 0-23 >
            Seconds.
                
        Examples
        ========
        >>> s.system_time_query()
        (12, 10, 15)
        """
        self.com.send('SYST:TIME?')
        ret = self.com.readline()
        self._error_check()
        h = int(ret[:2])
        m = int(ret[2:4])
        s = int(ret[4:6])
        return h, m, s
        
    def system_date_set(self, y, m, d):
        """
        SYST:DATE : Set System Date
        ---------------------------
        Sets the system date of the real-time clock of the instrument.
        Year is a 4-digit integer. Month is an integer 1 to 12. 
        Day is an integer 1 to 31 (depending on the month)        
        
        Args
        ====
        < y : int : 0-9999 >
            Year to set.
        
        < m : int : 1-12 >
            Month to set.
        
        < d : int : 1-31 >
            Day to set.
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.system_date_set(2014, 12, 23)
        """
        settime = '%04d%02d%02d'%(y, m, d)
        self.com.send('SYST:DATE "%s"'%(settime))
        self._error_check()
        return

    def system_date_query(self):
        """
        SYST:DATE? : Query System Date
        ------------------------------
        Query the system date of the instrument.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < y : int : 0-9999 >
            Year to set.
        
        < m : int : 1-12 >
            Month to set.
        
        < d : int : 1-31 >
            Day to set.
                
        Examples
        ========
        >>> s.system_date_query()
        (2014, 12, 23)
        """
        self.com.send('SYST:DATE?')
        ret = self.com.readline()
        self._error_check()
        y = int(ret[:4])
        m = int(ret[4:6])
        d = int(ret[6:8])
        return y, m, d
        
    def system_datetime_now(self):
        """
        SYST:TIME/DATE : (Helper Method) Set System DateTime Now
        --------------------------------------------------------
        Set the date and time now.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.system_datetime_now()
        """
        Y = int(time.strftime('%Y'))
        m = int(time.strftime('%m'))
        d = int(time.strftime('%d'))
        self.system_date_set(Y, m, d)
        H = int(time.strftime('%H'))
        M = int(time.strftime('%M'))
        S = int(time.strftime('%S'))
        self.system_time_set(H, M, S)
        return

    def system_datetime_get(self):
        """
        SYST:TIME/DATE : (Helper Method) Get System DateTime Now
        --------------------------------------------------------
        Get the date and time.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < datetime : datetime-object :  >
            System datetime.
                
        Examples
        ========
        >>> s.system_datetime_now()
        """
        Y, m, d = self.system_date_query()
        H, M, S = self.system_time_query()
        fmt = '%Y/%m/%d %H:%M:%S'
        ret = '%d/%d/%d %d:%d:%d'%(Y, m, d, H, M, S)
        timestamp = datetime.datetime.strptime(ret, fmt)
        return timestamp

    def trace_data_query(self, ch=1):
        """
        TRAC? : Query Trace Data
        ------------------------
        This query command returns the current displayed data.
        
        Args
        ====
        < ch : int : 1-4 >
        
        Returns
        =======
        < data : list(float) :  >
            A list of the data that are displayed.
                
        Examples
        ========
        >>> s.trace_data_query()
        array([  4.156894, -52.79362, ... , -43.07858, -41.12521 ])
        """
        self.com.send('TRACE:DATA? TRACE%d'%(ch))
        ret = self.com.readline()
        self._error_check()
        ret = numpy.array(ret.strip().split(','), float)
        return ret
        
    def frequency_center_set(self, freq, unit='GHz'):
        """
        FREQ:CENT : Set Center Frequency
        --------------------------------
        Set the center frequency of the spectrum analyzer.
        
        Args
        ====
        < freq : str or float :  >
            The center frequency to set.
            In str : '3.5 GHz', '200MHz'
            In float : 3.5, 200
                       NOTE: <unit> is referenced as the unit.
        
        < unit : str :  >
            The unit of the specified <freq>.
            <unit> is ignored when <freq> is specified with str.
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.frequency_center_set(10)
        >>> s.frequency_center_set(10, 'MHz')
        >>> s.frequency_center_set('3.2GHz')
        """
        freq = freq_value(freq, unit)
        self.com.send('FREQ:CENT %s'%(freq.query))
        self._error_check()
        return
        
    def frequency_center_query(self):
        """
        FREQ:CENT? : Query Center Frequency
        -----------------------------------
        Query the center frequency of the spectrum analyzer.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < freq : float : (Hz) >
            The center frequency. unit is in Hz.
        
        Examples
        ========
        >>> s.frequency_center_query()
        3500000000.0
        """
        self.com.send('FREQ:CENT?')
        ret = self.com.readline()
        self._error_check()
        ret = float(ret)
        return ret
    
    def frequency_center_ch_set(self, ch):
        """
        FREQ:CENT:CHAN : Set Center Frequency Channel
        ---------------------------------------------
        Set the center frequency channel of the spectrum analyzer.
        
        Args
        ====
        < ch : int :  >
            The center frequency channel to set.
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.frequency_center_ch_set(200)
        """
        self.com.send('FREQ:CENT:CHAN %d'%(ch))
        self._error_check()
        return
        
    def frequency_center_ch_query(self):
        """
        FREQ:CENT:CHAN : Query Center Frequency Channel
        -----------------------------------------------
        Query the center frequency channel of the spectrum analyzer.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < ch : int :  >
            The center frequency channel.
                
        Examples
        ========
        >>> s.frequency_center_ch_query()
        10
        """
        self.com.send('FREQ:CENT:CHAN?')
        ret = self.com.readline()
        self._error_check()
        ret = int(ret)
        return ret
        
    def frequency_start_set(self, freq, unit='GHz'):
        """
        FREQ:STAR : Set Start Frequency
        -------------------------------
        Set the start frequency of the spectrum analyzer.
        
        Args
        ====
        < freq : str or float :  >
            The start frequency to set.
            In str : '3.5 GHz', '200MHz'
            In float : 3.5, 200
                       NOTE: <unit> is referenced as the unit.
        
        < unit : str :  >
            The unit of the specified <freq>.
            <unit> is ignored when <freq> is specified with str.
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.frequency_start_set(10)
        >>> s.frequency_start_set(10, 'MHz')
        >>> s.frequency_start_set('3.2GHz')
        """
        freq = freq_value(freq, unit)
        self.com.send('FREQ:STAR %s'%(freq.query))
        self._error_check()
        return
        
    def frequency_start_query(self):
        """
        FREQ:STAR? : Query Start Frequency
        ----------------------------------
        Query the start frequency of the spectrum analyzer.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < freq : float : (Hz) >
            The start frequency. unit is in Hz.
        
        Examples
        ========
        >>> s.frequency_start_query()
        0.0
        """
        self.com.send('FREQ:STAR?')
        ret = self.com.readline()
        self._error_check()
        ret = float(ret)
        return ret
    
    def frequency_stop_set(self, freq, unit='GHz'):
        """
        FREQ:STOP : Set Stop Frequency
        ------------------------------
        Set the stop frequency of the spectrum analyzer.
        
        Args
        ====
        < freq : str or float :  >
            The stop frequency to set.
            In str : '3.5 GHz', '200MHz'
            In float : 3.5, 200
                       NOTE: <unit> is referenced as the unit.
        
        < unit : str :  >
            The unit of the specified <freq>.
            <unit> is ignored when <freq> is specified with str.
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.frequency_stop_set(10)
        >>> s.frequency_stop_set(10, 'MHz')
        >>> s.frequency_stop_set('3.2GHz')
        """
        freq = freq_value(freq, unit)
        self.com.send('FREQ:STOP %s'%(freq.query))
        self._error_check()
        return
        
    def frequency_stop_query(self):
        """
        FREQ:STOP? : Query Start Frequency
        ----------------------------------
        Query the stop frequency of the spectrum analyzer.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < freq : float : (Hz) >
            The stop frequency. unit is in Hz.
        
        Examples
        ========
        >>> s.frequency_stop_query()
        0.0
        """
        self.com.send('FREQ:STOP?')
        ret = self.com.readline()
        self._error_check()
        ret = float(ret)
        return ret
    
    def frequency_span_set(self, freq, unit='GHz'):
        """
        FREQ:SPAN : Set Frequency Span
        ------------------------------
        Set the frequency span. Setting the span to 0 Hz puts the analyzer
        into zero span.
        
        Args
        ====
        < freq : str or float :  >
            The span frequency to set.
            In str : '3.5 GHz', '200MHz'
            In float : 3.5, 200
                       NOTE: <unit> is referenced as the unit.
        
        < unit : str :  >
            The unit of the specified <freq>.
            <unit> is ignored when <freq> is specified with str.
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.frequency_span_set(10)
        >>> s.frequency_span_set(10, 'MHz')
        >>> s.frequency_span_set('3.2GHz')
        """
        freq = freq_value(freq, unit)
        self.com.send('FREQ:SPAN %s'%(freq.query))
        self._error_check()
        return
        
    def frequency_span_query(self):
        """
        FREQ:SPAN? : Query Span Frequency
        ---------------------------------
        Query the span frequency of the spectrum analyzer.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < freq : float : (Hz) >
            The span frequency. unit is in Hz.
        
        Examples
        ========
        >>> s.frequency_span_query()
        0.0
        """
        self.com.send('FREQ:SPAN?')
        ret = self.com.readline()
        self._error_check()
        ret = float(ret)
        return ret
    
    def reference_level_set(self, level):
        """
        DISP:WIND:TRAC:Y:RLEV : Set Refelence Level
        -------------------------------------------
        This command sets the reference level for the Y-axis.
        
        Args
        ====
        < level : float :  >
            The reference level to set. unit is in dBm.
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.reference_level_set(0)
        >>> s.reference_level_set(-20)
        """
        self.com.send('DISP:WIND:TRAC:Y:RLEV %f dBm'%(level))
        self._error_check()
        return
        
    def reference_level_query(self):
        """
        DISP:WIND:TRAC:Y:RLEV? : Query Refelence Level
        ----------------------------------------------
        Query the reference level for the Y-axis.
        
        Args
        ====
        Nothing.
                
        Returns
        =======
        < level : float :  >
            The reference level. unit is in dBm.
        
        Examples
        ========
        >>> s.reference_level_query()
        0.0
        """
        self.com.send('DISP:WIND:TRAC:Y:RLEV?')
        ret = self.com.readline()
        self._error_check()
        ret = float(ret)
        return ret
        
    def attenuation_set(self, att):
        """
        POW:ATT : Set Input Attenuation
        -------------------------------
        Set the input attenuator of the spectrum analyzer.
        
        Args
        ====
        < att : int : 0, 50, 5step >
            The input attenuation to set. unit is in dB.
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.attenuation_set(10)
        """
        self.com.send('POW:ATT %f dB'%(att))
        self._error_check()
        return
        
    def attenuation_query(self):
        """
        POW:ATT? : Query Input Attenuation
        -----------------------------------
        Query the input attenuatior level.
        
        Args
        ====
        Nothing.
                        
        Returns
        =======
        < att : float :  >
            The input attenuator level. unit is in dB.
        
        Examples
        ========
        >>> s.attenuation_query()
        0.0
        """
        self.com.send('POW:ATT?')
        ret = self.com.readline()
        self._error_check()
        ret = int(ret)
        return ret
        
    def attenuation_auto_set(self, auto):
        """
        POW:ATT:AUTO : Set Input Attenuation AUTO/MANUAL
        ------------------------------------------------
        Set the input attenuator state to AUTO/MANUAL.
        
        Args
        ====
        < auto : int or str : 0,1,'OFF','ON' >
            The input attenuation state to set. 
            0 = 'OFF', 1 = 'ON'
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.attenuation_auto_set(0)
        >>> s.attenuation_auto_set('ON')
        """
        self.com.send('POW:ATT:AUTO %s'%(str(auto)))
        self._error_check()
        return
        
    def attenuation_auto_query(self):
        """
        POW:ATT:AUTO? : Query Input Attenuation AUTO/MANUAL
        ---------------------------------------------------
        Query the input attenuator state.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < auto : int : 0,1  >
            The input attenuation state.
            0 = 'OFF', 1 = 'ON'
                
        Examples
        ========
        >>> s.attenuation_auto_query()
        0
        """
        self.com.send('POW:ATT:AUTO?')
        ret = self.com.readline()
        self._error_check()
        ret = int(ret)
        return ret
        
    def scalediv_set(self, div):
        """
        DISP:WIND:TRAC:Y:PDIV : Set Scale/DIV
        -------------------------------------
        This command sets the per-division display scaling for the y-axis
        when scale type of Y axis is set to Log.
        
        Args
        ====
        < div : int : 1,2,5,10 >
            The per-division display scaling to set. unit is in dB.
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.scalediv_set(10)
        """
        self.com.send('DISP:WIND:TRAC:Y:PDIV DIV%d'%(div))
        self._error_check()
        return
        
    def scalediv_query(self):
        """
        DISP:WIND:TRAC:Y:PDIV? : Query Scale/DIV
        ----------------------------------------
        Query display scaling.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < div : int : 1,2,5,10 >
            The per-division display scaling. unit is in dB.
                
        Examples
        ========
        >>> s.scalediv_query()
        10
        """
        self.com.send('DISP:WIND:TRAC:Y:PDIV?')
        ret = self.com.readline()
        self._error_check()
        ret = int(ret.strip('DIV\n'))
        return ret
        
    def scaletype_set(self, stype):
        """
        DISP:WIND:TRAC:Y:SPAC : Set Scale Type
        --------------------------------------
        Toggles the vertical graticule divisions between logarithmic unit and
        linear unit. The default logarithmic unit is dBm, and the linear unit
        is mV.
        
        Args
        ====
        < stype : str : 'LOG','LIN' >
            The unit to set.
        
g        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.scaletype_set('LOG')
        """
        self.com.send('DISP:WIND:TRAC:Y:SPAC %s'%(stype))
        self._error_check()
        return
        
    def scaletype_query(self):
        """
        DISP:WIND:TRAC:Y:SPAC? : Query Scale Type
        -----------------------------------------
        Query the scale type.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < stype : str : 'LOG','LIN' >
            The scale type.
                
        Examples
        ========
        >>> s.scaletype_query()
        """
        self.com.send('DISP:WIND:TRAC:Y:SPAC?')
        ret = self.com.readline().strip()
        self._error_check()
        return ret
        
    def resolution_bw_set(self, bw, unit='MHz'):
        """
        BAND : Set Resolution Bandwidth
        -------------------------------
        Specifies the resolution bandwidth. For numeric entries, all RBW types
        choose the nearest (arithmetically, on a linear scale, rounding up)
        available RBW to the value entered.
        
        Args
        ====
        < bw : str or float : 10Hz-3MHz >
            The bandwidth to set.
            In str : '3 MHz', '10kHz'
            In float : 10, 3
                       NOTE: <unit> is referenced as the unit.
        
        < unit : str :  >
            The unit of the specified <freq>.
            <unit> is ignored when <freq> is specified with str.
        
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.resolution_bw_set(3, 'MHz')
        >>> s.resolution_bw_set('100Hz')
        """
        freq = freq_value(bw, unit)
        self.com.send('BAND %s'%(freq.query))
        self._error_check()
        return
        
    def resolution_bw_query(self):
        """
        BAND? : Query Resolution Bandwidth
        ----------------------------------
        Query resolution bandwidth.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < bw : float :  >
            The bandwidth. unit is Hz.
        
        Examples
        ========
        >>> s.resolution_bw_query()
        3000000.0
        """
        self.com.send('BAND?')
        ret = self.com.readline()
        self._error_check()
        ret = float(ret)
        return ret
        
    def resolution_bw_auto_set(self, auto):
        """
        BAND:AUTO : Set Resolution Bandwidth AUTO/MANUAL
        ------------------------------------------------
        This command turns on/off auto resolution bandwidth state.
        
        Args
        ====
        < auto : int or str : 0,1,'OFF','ON' >
            The resolution BW state to set. 
            0 = 'OFF', 1 = 'ON'
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.resolution_bw_auto_set(0)
        >>> s.resolution_bw_auto_set('ON')
        """
        self.com.send('BAND:AUTO %s'%(str(auto)))
        self._error_check()
        return
        
    def resolution_bw_auto_query(self):
        """
        BAND:AUTO? : Query Resolution Bandwidth AUTO/MANUAL
        ---------------------------------------------------
        Query the AUTO status of the resolution BW.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < auto : int or str : 0,1,'OFF','ON' >
            The resolution BW state. 
            0 = 'OFF', 1 = 'ON'
        
        Examples
        ========
        >>> s.resolution_bw_auto_query()
        1
        """
        self.com.send('BAND:AUTO?')
        ret = self.com.readline()
        self._error_check()
        ret = int(ret)
        return ret
        
    def video_bw_set(self, bw, unit='MHz'):
        """
        BAND:VID : Set Video Bandwidth
        ------------------------------
        Specifies the video bandwidth.        
        
        Args
        ====
        < bw : str or float : 10Hz-3MHz >
            The bandwidth to set.
            In str : '3 MHz', '10kHz'
            In float : 10, 3
                       NOTE: <unit> is referenced as the unit.
        
        < unit : str : 'MHz','kHz','Hz'>
            The unit of the specified <freq>.
            <unit> is ignored when <freq> is specified with str.
        
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.video_bw_set(3, 'MHz')
        >>> s.video_bw_set('100Hz')
        """
        freq = freq_value(bw, unit)
        self.com.send('BAND:VID %s'%(freq.query))
        self._error_check()
        return
        
    def video_bw_query(self):
        """
        BAND:VID? : Query Video Bandwidth
        ---------------------------------
        Query the video bandwidth.        
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < bw : float :  >
            The bandwidth. unit is Hz.
        
        Examples
        ========
        >>> s.video_bw_query()
        """
        self.com.send('BAND:VID?')
        ret = self.com.readline()
        self._error_check()
        ret = float(ret)
        return ret

    def video_bw_auto_set(self, auto):
        """
        BAND:VID:AUTO : Set Video Bandwidth AUTO/MANUAL
        -----------------------------------------------
        This command turns on/off auto video bandwidth state.
        
        Args
        ====
        < auto : int or str : 0,1,'OFF','ON' >
            The resolution BW state to set. 
            0 = 'OFF', 1 = 'ON'
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.video_bw_auto_set(0)
        >>> s.video_bw_auto_set('ON')
        """
        self.com.send('BAND:VID:AUTO %s'%(str(auto)))
        self._error_check()
        return
        
    def video_bw_auto_query(self):
        """
        BAND:AUTO? : Query Video Bandwidth AUTO/MANUAL
        ----------------------------------------------
        Query the AUTO status of the Video BW.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < auto : int or str : 0,1,'OFF','ON' >
            The resolution BW state. 
            0 = 'OFF', 1 = 'ON'
        
        Examples
        ========
        >>> s.resolution_bw_auto_query()
        1
        """
        self.com.send('BAND:VID:AUTO?')
        ret = self.com.readline()
        self._error_check()
        ret = int(ret)
        return ret
    
    def average_set(self, num, ch=1):
        """
        AVER:TRACn:COUN : Set Average Number
        -------------------------------
        Specifies the number of measurements that are combined.
        
        Args
        ====
        < num : int : 1-8192 >
            The number count of measurements that are combined.
        
        < ch : int : 1-4 >
            The number of a trace to set average.
            default = 1
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.average_set(1)
        >>> s.average_set(11, ch=2)
        """
        self.com.send('AVER:TRAC%d:COUN %d'%(ch, num))
        self._error_check()
        return
        
    def average_query(self, ch=1):
        """
        AVER:TRACn:COUN? : Query Average Number
        ---------------------------------------
        Query the average number.
        
        Args
        ====        
        < ch : int : 1-4 >
            The number of a trace to query average.
            default = 1
        
        Returns
        =======
        < num : int : 1-8192 >
            The number count of measurements that are combined.
                
        Examples
        ========
        >>> s.average_query()
        1
        
        >>> s.average_query(ch=2)
        11
        """
        self.com.send('AVER:TRAC%d:COUN?'%(ch))
        ret = self.com.readline()
        self._error_check()
        ret = int(ret)
        return ret
        
    def average_onoff_set(self, on_off, ch=1):
        """
        AVER:TRACn : Set Average ON/OFF
        -------------------------------
        Sets the ON/OFF of average process.
        
        Args
        ====
        < on_off : int or str : 0,1,'OFF','ON' >
            The average ON/OFF state. 
            0 = 'OFF', 1 = 'ON'
        
        < ch : int : 1-4 >
            The number of a trace to set average.
            default = 1
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.average_onoff_set(1)
        >>> s.average_onoff_set('OFF', ch=2)
        """
        self.com.send('AVER:TRAC%d %s'%(ch, str(on_off)))
        self._error_check()
        return
        
    def average_onoff_query(self, ch=1):
        """
        AVER:TRACn? : Query Average ON/OFF
        ----------------------------------
        Query the ON/OFF status of average process.
        
        Args
        ====
        < ch : int : 1-4 >
            The number of a trace to set average.
            default = 1
        
        Returns
        =======
        < on_off : int or str : 0,1,'OFF','ON' >
            The average ON/OFF state. 
            0 = 'OFF', 1 = 'ON'
        
        Examples
        ========
        >>> s.average_onoff_query()
        0
        
        >>> s.average_onoff_query(ch=2)
        1
        """
        self.com.send('AVER:TRAC%d?'%(ch))
        ret = self.com.readline()
        self._error_check()
        ret = int(ret)
        return ret
            
    def average_restart(self, ch=1):
        """
        AVER:TRACn:CLE : Restart Average 
        --------------------------------
        Restart the average process.
        
        Args
        ====
        < ch : int : 1-4 >
            The number of a trace to set average.
            default = 1
        
        Returns
        =======
        Nothing.
                
        Examples
        ========
        >>> s.average_restart()
        >>> s.average_restart(ch=2)
        """
        self.com.send('AVER:TRAC%d:CLE'%(ch))
        self._error_check()
        return
        
    def sweep_time_set(self, sweep):
        """
        SWE:TIME : Set Sweep Time
        -------------------------
        Specifies the time in which the instrument sweeps the display.
        A span value of 0 Hz causes the analyzer to enter zero span mode.
        In zero span the X-axis represents time rather than frequency.
        
        Args
        ====
        < sweep : float :  >
            The sweep time. unit is sec.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.sweep_time_set(5)
        """
        self.com.send('SWE:TIME %fs'%(sweep))
        self._error_check()
        return
        
    def sweep_time_query(self):
        """
        SWE:TIME? : Query Sweep Time
        ----------------------------
        Query sweep time.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < sweep : float :  >
            The sweep time. unit is sec.
        
        Examples
        ========
        >>> s.sweep_time_query()
        0.287
        """
        self.com.send('SWE:TIME?')
        ret = self.com.readline()
        self._error_check()
        ret = float(ret)
        return ret
            
    def gen_xaxis(self):
        start = self.frequency_start_query()
        stop = self.frequency_stop_query()
        num = len(self.trace_data_query())
        xaxis = numpy.linspace(start, stop, num)
        return xaxis



class N9342C(N9342):
    product_name = 'N9342C'
    
class N9343C(N9342):
    product_name = 'N9343C'
    
class N9344C(N9342):
    product_name = 'N9344C'
    


# ==============
# Helper Classes
# ==============

# Values
# ======
class freq_value(object):
    def __init__(self, value, unit):
        if type(value) == str:
            self.unit = value.strip('1234567890. ')
            self.value = float(value.strip(self.unit+' '))
        else:
            self.unit = unit.strip()
            self.value = float(value)
            pass
        self.query = '%.10f %s'%(self.value, self.unit)
        pass


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
        error_item(0, 'No error', ''),
        error_item(-410, 'Query INTERRUPTED', 'Indicates that a condition causing an INTERRUPTED query occurred (see IEEE 488.2, 6.3.2.7)'),
        error_item(-350, 'Query overflow', 'Indicates the SCPI remote interface error queue overflowed.'),
        error_item(-321, 'Out of memory', 'Indicates an internal operation needed more memory than that was available.'),
        error_item(-224, 'Illegal parameter value', 'Indicates you sent a parameter for this command that is NOT allowed.'),
        error_item(-223, 'Too much data', 'Indicates a legal program data element of block, expression or string type was received that contained more data than the device could handle due to related device-specific requirements or memory.'),
        error_item(-222, 'Data out of range', 'Indicates a legal data was parsed but could not be executed because of the interpreted value was outside the legal range defined by the analyzer. The displayed results may be clipped.'),
        error_item(-220, 'No matched module', 'Indicates no matched measurement or mode found.'),
        error_item(-200, 'Execution error', 'This is a generic execution error for devices that cannot detect more specific errors. The code indicates on those execution errors defined in IEEE 488.2, 11.5.1.1.4 has occurred.'),
        error_item(-171, 'Invalid expression', 'Indicates the data element was invalid, for example, unmatched parentheses, or an illegal character.'),
        error_item(-144, 'Character data long', 'Indicates the character data contained more than 12 characters. (see IEEE 488.2, 7.7.1.4)'),
        error_item(764, 'Unable to save file', 'Indicates a failure occurred while saving a file. The file was not saved.'),
        error_item(762, 'Unable to load file', 'Indicates a failure occurred while loading a file. The file was not loaded.'),
        error_item(612, 'File NOT found', 'Indicates the analyzer could not find the specified file.'),
        error_item(173, 'Lame package, please upgrade firmware', 'Indicates the current firmware is not mostly updated. The firmware needs upgrading.'),
        error_item(172, 'Option install fail, invalid option licence', 'Indicates the option could not be installed, because of the invalid option licence.'),
        error_item(171, 'File loaded', 'Indicates the file loading succeeded.'),
        error_item(170, 'The menu is unavailable in this case', 'Indicates the memo is invalid in this case.'),
        error_item(166, 'Marker counter opened in fast sweep', 'Indicates the counteris accuracy decreases when in fast sweep mode.'),
        error_item(162, 'Cannot open fast sweep in this case', 'Indicates current settings do not allow youtoopenfastsweep.Forexample, currently in FFT, zero span, or any measurement in power suite does not allow fast sweep.'),
        error_item(156, 'Incorrect alignment file on flash', 'Indicates an invalid alignment file.'),
        error_item(153, 'RF EEPROM operate fail', 'Indicates an error when writing alignment file.'),
        error_item(152, 'Alignment file oversize', 'Indicates the alignment file has error or invalid data.'),
        error_item(151, 'DSP boot fail', 'Indicates the analyzer cannot process measurement currently, wait the analyzer to reboot. If analyzer froze, try to restart the analyzer.'),
        error_item(150, 'Mixer overload', 'Indicates the first mixer in danger. Either increase input attenuation or decrease the input signal level.'),
        error_item(149, 'Mixer saturate', 'Indicates you need to either increase the input attenuation or decrease the input signal level.'),
        error_item(147, 'Incorrect alignment data in EEPROM', 'Indicates invalid alignment data occurred.'),
        error_item(143, 'Final IF overload', 'Indicates you need to either increase the input attenuation or decrease the input signal level.'),
        error_item(138, 'USB device NOT ready', 'Indicates the USB device is not detected.'),
        error_item(136, 'RBW limit to 30 kHz when in fast sweep', 'Indicates the analyzer automatically couple the RBW to 30 kHz when in fast sweep mode.'),
        error_item(130, 'Meas uncal', 'Indicates the measurement is uncalibrated due to fast sweeping through a narrow RBW filter. Check the sweep time, span, and bandwidth settings, or use auto coupling.'),
        error_item(119, 'RF Board Changed', 'Indicates the RF board was changed, the analyzer needs re-load the alignment data.'),
        error_item(116, 'Cannotcommunicate with RF', 'IndicatestheMCUcannotfindtheRF board.'),
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
    
    

