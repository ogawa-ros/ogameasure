#! /usr/bin/env python

import datetime
from ..SCPI import scpi

class model218(scpi.scpi_family):
    manufacturer = 'Lakeshore'
    product_name = 'model 218'
    classification = 'Temperature Monitor'
    
    _scpi_enable = '*CLS *ESE *ESE? *ESR? *IDN? *OPC *OPC? *RST *SRE ' \
                   + '*SRE? *STB? *TST? *WAI'
    
    def __init__(self, com):
        scpi.scpi_family.__init__(self, com)
        self.com.com.readline()
        pass
    
    def alarm_set(self, ch=1, off_on=1, source=1, high_value=300,
                  low_value=100, deadband=1, latch_enable=0):
        """
        ALARM : Configure Input Alarm Parameters
        ----------------------------------------
        Configures the alarm parameters for an input.
        
        < ch : int : 1-8 >
            Specifies which input to configure (1-8).
        
        < off_on : int : 0,1 >
            Determines whether the instrument checks the alarm for this input.
            0 = OFF, 1 = ON
        
        < source : int : 1-4 >
            Specifies input data to check.
            1 = Kelvin, 2 = Celsius, 3 = sensor units, 4 = linear data.
        
        < high_value : float :  >
            Sets the value the source is checked against to activate the
            high alarm.
        
        < low_value : float :  >
            Sets the value the source is checked against to activate low
            alarm.
        
        < deadband : float :  >
            Sets the value that the source must change outside of an alarm
            condition to deactivate an unlatched alarm.
        
        < latch_enable : int : >
            Specifies a latched alarm (remains active after alarm condition
            correction).
        """
        self.com.send('ALARM %d, %d, %d %.3f, %.3f, %.3f, %d'%
                      (ch, off_on, source, high_value, low_value, deadband,
                       latch_enable))
        return

    def alarm_query(self, ch=1):
        """
        ALARM? : Query Input Alarm Parameters
        -------------------------------------
        Returns the alarm parameters of an input.
        
        < ch : int : 1-8 >
            Specifies which input to configure (1-8).
        
        Returns:
            off_on, source, high_value, low_value, deadband, latch_enable
        """
        self.com.send('ALARM? %d'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        off_on = int(ret[0])
        source = int(ret[1])
        high_value = float(ret[2])
        low_value = float(ret[3])
        deadband = float(ret[4])
        latch_enable = int(ret[5])
        print('ALARM? %d'%(ch))
        print('---------')
        print('off/on = %d'%(off_on))
        print('source = %d'%(source))
        print('high_value = %.3f'%(high_value))
        print('low_value = %.3f'%(low_value))
        print('deadband = %.3f'%(deadband))
        print('latch_enable = %d'%(latch_enable))
        return off_on, source, high_value, low_value, deadband, latch_enable
        
    def alarm_status_query(self, ch=1):
        """
        ALARMST? : Query Input Alarm Status
        -----------------------------------
        Returns the alarm status of an input.
        
        < ch : int : 1-8 >
            Specifies which input to configure (1-8).
        
        Returns:
            high_status : Specifies high alarm status.
                          0 = Unactivated, 1 = Activated

            low_status : Specifies low alarm status.
                         0 = Unactivated, 1 = Activated
        """
        self.com.send('ALARMST? %d'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        high_status = int(ret[0])
        low_status = int(ret[1])
        print('ALARMST? %d'%(ch))
        print('-----------')
        print('high_status = %d'%(high_status))
        print('low_status = %d'%(low_status))
        return high_status, low_status
    
    def audible_alarm_set(self, off_on=0):
        """
        ALMB : Configure Audible Alarm
        ------------------------------
        Enables or disables system alarm beeper.
        
        < off_on : int : 0,1 >
            disables/enables beeper.
            1 = On, 0 = Off
        """
        self.com.send('ALMB %d'%(off_on))
        return
        
    def audible_alarm_query(self):
        """
        ALMB? : Query Audible Alarm
        -----------------------------------
        Returns system beeper parameters.
        
        Returns:
            off_on : disables/enables beeper.
                     1 = On, 0 = Off
        """
        self.com.send('ALMB?')
        ret = self.com.readline()
        ret = int(ret)
        print('ALMB?')
        print('-----')
        print('off_on = %d'%(ret))
        return ret
        
    def alarm_reset(self):
        """
        ALMRST : Clear Alarm Status for All Inputs
        ------------------------------------------
        Resets a latched active alarm after the alarm condition has cleared.
        """
        self.com.send('ALMRST')
        return
    
    def analog_outputs_set(self, ch=1, bipolar_enable=0, mode=1, monitor_ch=1,
                           source=1, high_value=200, low_value=2, manual=0):
        """
        ANALOG : Configure Analog Output Parameters
        -------------------------------------------
        Configure Analog Output Parameters.
        
        < ch : int : 1,2 >
            Specifies which analog output to configure (1 or 2).
        
        < bipolar_enable : int : 0,1 >
            Specifies analog output:
            0 = positive only, 1 = bipolar.
        
        < mode : int : 0,1,2 >
            Specifies data the analog output monitors: 
            0 = off, 1 = input, 2 = manual.
        
        < monitor_ch : int : 1-8 >
            Specifies which input to monitor if <mode> = 1 (1-8).
        
        < source : int : 1-4 >
            Specifies input data.
            1 = Kelvin, 2 = Celsius, 3 = sensor units, 4 = linear equation.
        
        < high_value : float :  >
            If <mode> = 1, this parameter represents the data at which the
            analog output reaches +100% output.
        
        < low_value : float :  >
            If <mode> = 1, this parameter represents the data at which the
            analog output reaches -100% output if bipolar, or 0% output if
            positive only.
        
        < manual : float :  >
            If <mode> = 2, this parameter is the output of the analog output.
        """
        self.com.send('ANALOG %d, %d, %d, %d, %d, %.3f, %.3f, %.3f'%
                      (ch, bipolar_enable, mode, monitor_ch, source,
                       high_value, low_value, manual))
        return
        
    def alalog_outputs_query(self, ch=1):
        """
        ANALOG? : Query Analog Output Parameters
        ----------------------------------------
        
        < ch : int : 1,2 >
            Specifies analog output to query (1 or 2).
        
        Returns:
            bipolar_enable, mode, monitor_ch, source, high_value,
            low_value, manual_value
        """
        self.com.send('ANALOG? %d'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        bipolar_enable = int(ret[0])
        mode = int(ret[1])
        monitor_ch = int(ret[2])
        source = int(ret[3])
        high_value = float(ret[4])
        low_value = float(ret[5])
        manual = int(ret[6])
        print('ANALOG? %d'%(ch))
        print('----------')
        print('bipolar_enable = %d'%(bipolar_enable))
        print('mode = %d'%(mode))
        print('monitor_ch = %d'%(monitor_ch))
        print('source = %d'%(source))
        print('high_value = %.3f'%(high_value))
        print('low_value = %.3f'%(low_value))
        print('manual = %d'%(manual))
        return bipolar_enable, mode, monitor_ch, source, high_value,
               low_value, manual_value

    def analog_output_data_query(self, ch=1):
        """
        AOUT? : Query Analog Output Data
        --------------------------------
        Returns the percentage of output.
        
        < ch : int : 1,2 >
            Specifies analog output to query (1 or 2).
        
        Returns:
            output
        """
        self.com.send('AOUT? %d'%(ch))
        ret = self.com.readline()
        ret = float(ret)
        return ret
        
    def serial_interface_baud_rate_set(self, bps=2):
        """
        BAUD : Configure Serial Interface Baud Rate.
        --------------------------------------------
        Configures to serial interface baud rate.
        
        < bps : int : 0,1,2 >
            Specifies bits per second (bps) rate.
            0 = 300, 1 = 1200, 2 = 9600.
        """
        self.com.send('BAUD %d'%(bps))
        return
    
    def serial_interface_baud_rate_query(self):
        """
        BAUD? : Query Serial Interface Baud Rate.
        -----------------------------------------
        Returns serial interface baud rate.
        
        Returns:
            bps : 0 = 300, 1 = 1200, 2 = 9600.
        """
        self.com.send('BAUD?'%(bps))
        ret = self.com.readline()
        ret = int(ret)
        return ret
        
    def celsius_reading_query(self, ch=0):
        """
        CRDG? : Query Celsius Reading for Single Input or All Inputs
        ------------------------------------------------------------
        Returns the Celsius reading for a single input or all inputs.
        
        < ch : int : 0-8 >
            0 = all inputs. Return a list of float values.
            1-8 = individual input. Return a float value.
        
        NOTE: Use 0 (all inputs) when reading two or more inputs
              at the maximum update rate of 16 rdg/s.
        """
        self.com.send('CRDG? %d'%(ch))
        ret = self.com.readline()
        ret = map(float, ret.strip().split(','))
        if ch!=0: ret = ret[0]
        return ret
        
    def curve_delete(self, curve_num):
        """
        CRVDEL : Delete User Curve
        --------------------------
        Deletes a user curve.
        
        < curve_num : int : 21-28 >
            Specifies which curve to delete (21-28) for inputs 1-8.
        """
        self.com.send('CRVDEL %d'%(curve_num))
        return
        
    def curve_header_set(self, curve_num, name, SN, format, limit_value,
                         coefficient):
        """
        CRVHDR : Configure Curve Header
        -------------------------------
        
        < curve_num : int : 21-28 >
            Specifies which curve to configure (21-28) for inputs 1-8.
        
        < name : str[15] : >
            Specifies curve name. Limited to 15 characters.
        
        < SN : str[10] :  >
            Specifies curve serial number. Limited to 10 characters.
        
        < format : int : 2-4 >
            Specifies curve data format.
            2 = V/K, 3 = Ohm/K, 4 = log Ohm/K
        
        < limit_value : float : >
            Specifies curve temperature limit in Kelvin.
        
        < coefficient : int : 1,2 >
            Specifies curve temperature coefficient.
            1 = negative, 2 = positive.
        """
        self.com.send('CRVHDR %d, %s, %s, %d, %.3f, %d'%
                      (curve_num, name, SN, format, limit_value, coefficient))
        return

    def curve_header_query(self, curve_num):
        """
        CRVHDR? : Configure Curve Header
        --------------------------------
        
        < curve_num : int : 21-28 >
            Specifies which curve to configure (21-28) for inputs 1-8.
        
        Returns:
            name, SN, format, limit_value, coefficient
        """
        self.com.send('CRVHDR? %d'%(curve_num))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        name = ret[0]
        SN = ret[1]
        format = int(ret[2])
        limit_value = float(ret[3])
        coefficient = int(ret[4])
        latch_enable = int(ret[5])
        print('CRVHDR? %d'%(ch))
        print('----------')
        print('name = %s'%(name))
        print('SN = %s'%(SN))
        print('format = %d'%(format))
        print('limit_value = %.3f'%(limit_value))
        print('coefficient = %d'%(coefficient))
        return name, SN, format, limit_value, coefficient
        
    def curve_point_set(self, curve_num, index, units_value, temp_value):
        """
        CRVPT : Configure Curve Data Point
        ----------------------------------
        Configures a user curve data point.
        
        < curve_num : int : 21-28 >
            Specifies which curve to configure (21-28) for inputs 1-8.
        
        < index : int : 1-200 >
            Specifies the points index in the curve (1 - 200).
        
        < units_value : float : >
            Specifies sensor units for this point.
        
        < temp_value : float : >
            Specifies corresponding temperature in Kelvin for this point.
            6 digits.
        """
        units = ('%f'%(units_value))[:7]
        temp = ('%f'%(temp_value))[:7]
        self.com.send('CRVPT %d %d %s %s'%(curve_num, index, units, temp))
        return
        
    def curve_point_query(self, curve_num, index):
        """
        CRVPT? : Query Curve Data Point
        -------------------------------
        Returns a standard or user curve data point.
        
        < curve_num : int : 1-9,21-28 >
            Specifies which curve to query.
            1-5 = Standard Diode Curves,
            6-9 = Standard Platinum Curves,
            21-28 = User Curves.
            NOTE: Curve locations 10-20 not used.
        
        < index : int : 1-200 >
            Specifies the points index in the curve (1 - 200).
        
        Returns: 
            units_value, temp_value
        """
        self.com.send('CRVPT? %d %d'%(curve_num, index))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        units_value = float(ret[0])
        temp_value = float(ret[1])        
        return units_value, temp_value
    
    def curve_point_set_line(self, curve_num, units_values, temp_values):
        """
        (Helper Method) CRVPT : Configure Curve Data Point
        --------------------------------------------------
        Configures a user curve data point at one time.
        
        < curve_num : int : 21-28 >
            Specifies which curve to configure (21-28) for inputs 1-8.
        
        < units_values : list : >
            A list of sensor units for the curve.
            Max length is 200 (first 200 items will be used in excess case).
        
        < temp_value : list : >
            A list of corresponding temperatures in Kelvin for the curve.
            Max length is 200 (first 200 items will be used in excess case).
        """
        for i,(unit, temp) in enumerate(zip(units_values, temp_values)):
            if i>199: break
            self.curve_point_set(curve_num, i+1, unit, temp)
            continue
        return        
        
    def curve_point_query_line(self, curve_num):
        """
        (Helper Method) CRVPT? : Query Curve Data Point
        -----------------------------------------------
        Returns a standard or user curve data as a 1-d data.
        
        < curve_num : int : 1-9,21-28 >
            Specifies which curve to query.
            1-5 = Standard Diode Curves,
            6-9 = Standard Platinum Curves,
            21-28 = User Curves.
            NOTE: Curve locations 10-20 not used.

        Returns:
            units_values, temp_values
        """
        unit = []
        temp = []
        for i in range(200):
            _u, _t = self.curve_point_query(curve_num, i+1)
            unit.append(_u)
            temp.append(_t)
            continue
        return unit, temp
        
    def datetime_set(self, year, month, day, hour, minutes, seconds):
        """
        DATETIME : Configure Date and Time
        ----------------------------------
        Configures date and time using 24-hour format.
        
        < year : int : 00-99 >
            Specifies year. Valid entries are: 00 - 99.
        
        < month : int : 1-12 > 
            Specifies month. Valid entries are: 1 - 12.
        
        < day : int : 1-31 >
            Specifies day. Valid entries are 1 - 31.
        
        < hour : int : 0-23 >
            Specifies hour. Valid entries are: 0 - 23.
        
        < minutes : int : 0-59 >
            Specifies minutes. Valid entries are: 0 - 59.
        
        < seconds : int : 0-59 >
            Specifies seconds. Valid entries are: 0 - 59.
        """
        self.com.send('DATETIME %d, %d, %d, %d, %d, %d'%
                      (month, day, year, hour, minutes, seconds))
        return

    def datetime_set_now(self):
        """
        (Helper Method) DATETIME : Configure Date and Time
        --------------------------------------------------
        Configures date and time to current time.        
        """
        fmt = '%m, %d, %y, %H, %M, %S'
        datetime_str = datetime.datetime.now().strftime(fmt)
        self.com.send('DATETIME %s'%(datetime_str))
        return
        
    def datetime_query(self):
        """
        DATETIME? : Query Date and Time
        --------------------------------
        Returns date and time.
        
        Returns:
            timestamp
        """
        self.com.send('DATETIME?')
        ret = self.com.readline().strip()
        fmt = '%m, %d, %y, %H, %M, %S'
        timestamp = datetime.datetime.strptime(ret, fmt)
        return timestamp
        
    def factory_defaults_reset(self, param=0):
        """
        DFLT : Set to Factory Defaults
        ------------------------------
        Sets all configuration values to factory defaults and resets the
        instrument. Does not clear user curves or instrument calibration.
        
        < param : int : 99 >
            The 99 is required to prevent accidentally setting the
            unit to defaults.
        """
        self.com.send('DFLT %d'%(param))
        return
        
    def display_field_set(self, location, sensor, source):
        """
        DISPFLD : Configure Display Parameters
        --------------------------------------
        Configures the display parameters.
        
        < location : int : 1-8 >
            Specifies display location to configure (1-8).
        
        < sensor : int : 0-8 >
            Specifies input to display in the display location (0-8).(0=none).
        
        < source : int : 1-4 >
            Specifies input data to display.
            1 = Kelvin, 2 = Celsius, 3 = sensorunits, 4 = linear data,
            5 = minimum data, 6 = maximum data.
        """
        self.com.send('DISPFLD %d, %d, %d'%(location, sensor, source))
        return
        
    def display_field_set_all_kelvin(self):
        """
        (Helper Method) DISPFLD : Configure Display Parameters
        ------------------------------------------------------
        Set all display fields to show Kelvin value.
        """
        for i in range(1,9):
            self.display_field_set(i, i, 1)
            continue
        return
        
    def display_field_query(self, location):
        """
        DISPFLD? : Query Display Field
        ------------------------------
        Returns the parameters for a displayed field.
        
        < location : int : 1-8 >
            Specifies display location to configure (1-8).
        
        Returns:
            sensor, source
        """
        self.com.send('DISPFLD? %d'%(location))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        sensor = int(ret[0])
        source = int(ret[1])
        return sensor, source
        
    def display_field_query_all(self):
        """
        (Helper Method) DISPFLD? : Query Display Field
        -----------------------------------------------
        Returns the parameters for all displayed fields.
        
        Returns:
            sensors, sources
        """
        sensors = []
        sources = []
        for i in range(1,9):
            _se, _so = self.display_field_query(i)
            sensors.append(_se)
            sources.append(_so)
        return sensors, sources
    
    def filter_set(self, ch, off_on=1, points=5, window=2):
        """
        FILTER : Configure Input Filter Parameters
        ------------------------------------------
        
        < ch : int : 1-8 > 
            Specifies input to configure (1-8).

        < off_on : int : 0,1 > 
            Specifies whether the filter function is off or on.
            0 = Off, 1 = On.

        < points : int : 2-64 > 
            Specifies how many data points the filtering function uses (2-64).
        
        < window : int : 1-10 >
            Specifies what percent of full scale reading limits the
            filtering function (1-10). Reading changes greater than this
            percentage reset the filter.
        """
        self.com.send('FILTER %d, %d, %d, %d'%(ch, off_on, points, window))
        return
    
    def filter_set_all(self, off_on=1, points=5, window=2):
        """
        (Helper Method) FILTER : Configure Input Filter Parameters
        ----------------------------------------------------------
        Set same configurations for all input sensors.
        
        < off_on : int : 0,1 > 
            Specifies whether the filter function is off or on.
            0 = Off, 1 = On.

        < points : int : 2-64 > 
            Specifies how many data points the filtering function uses (2-64).
        
        < window : int : 1-10 >
            Specifies what percent of full scale reading limits the
            filtering function (1-10). Reading changes greater than this
            percentage reset the filter.
        """
        for i in range(1, 9):
            self.filter_set(i, off_on, points, window)
            continue
        return
    
    def filter_query(self, ch):
        """
        FILTER : Configure Input Filter Parameters
        ------------------------------------------
        
        < ch : int : 1-8 > 
            Specifies input to configure (1-8).

        Returns:
            off_on, points, window
        """
        self.com.send('FILTER? %d'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        off_on = int(ret[0])
        points = int(ret[1])
        window = int(ret[2])
        return off_on, points, window
    
    def filter_query(self):
        """
        (Helper Method) FILTER : Configure Input Filter Parameters
        ----------------------------------------------------------
        Query input filter parameters for all input sensors.
        
        Returns:
            off_on, points, windows
        """
        off_on = []
        points = []
        window = []
        for i in range(1, 9):
            _o, _p, _w = self.filter_query(i)
            off_on.append(_o)
            points.append(_p)
            window.append(_w)
            continue
        return off_on, points, window
    
    
        
    

        
    def kelvin_reading_query(self, ch=0):
        """
        KRDG? : Query Kelvin Reading for Single Input or All Inputs
        -----------------------------------------------------------
        Returns the Kelvin reading for a single input or all inputs. 
        
        < ch : int : 0-8 >
            0 = all inputs. Return a list of float values.
            1-8 = individual input. Return a float value.
        
        NOTE: Use 0 (all inputs) when reading two or more inputs
              at the maximum update rate of 16 rdg/s.
        """
        self.com.send('KRDG? %d'%(ch))
        ret = self.com.readline()
        ret = map(float, ret.strip().split(','))
        if ch!=0: ret = ret[0]
        return ret

    def sensor_units_reading_query(self, ch=0):
        """
        SRDG? : Query Sensor Units Reading for Single Input or All Inputs
        -----------------------------------------------------------------
        Returns the Sensor Units reading for a single input or all inputs. 
        
        < ch : int : 0-8 >
            0 = all inputs. Return a list of float values.
            1-8 = individual input. Return a float value.
        
        NOTE: Use 0 (all inputs) when reading two or more inputs
              at the maximum update rate of 16 rdg/s.
        """
        self.com.send('SRDG? %d'%(ch))
        ret = self.com.readline()
        ret = map(float, ret.strip().split(','))
        if ch!=0: ret = ret[0]
        return ret

        
    
    _shortcut_command = {'KRDGQ': 'kelvin_reading_query',
                         'SRDGQ': 'sensor_units_reading_query'}

