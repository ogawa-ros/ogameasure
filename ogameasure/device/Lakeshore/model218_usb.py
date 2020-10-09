import sys
import datetime
from ..SCPI import scpi
import serial

class model218_usb(object):
    manufacturer = 'Lakeshore'
    product_name = 'model 218'
    classification = 'Temperature Monitor'

    _scpi_enable = '*CLS *ESE *ESE? *ESR? *IDN? *OPC *OPC? *RST *SRE ' \
                   + '*SRE? *STB? *TST? *WAI'

    def __init__(self, port):
        port = port
        self.com = serial.Serial(port=port,
                                baudrate=9600,
                                bytesize=7,
                                parity="O",
                                stopbits=1,
                                timeout=3,
                                write_timeout=3)
        pass

    def send(self,cmd):
        terminator = "\r\n"
        _cmd = cmd + terminator
        cmd_byte = _cmd.encode()
        self.com.write(cmd_byte)

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
        self.send('ALARM %d, %d, %d %.3f, %.3f, %.3f, %d'%
                      (ch, off_on, source, high_value, low_value, deadband,
                       latch_enable))
        return

    def alarm_query(self, ch=1, printlog=True):
        """
        ALARM? : Query Input Alarm Parameters
        -------------------------------------
        Returns the alarm parameters of an input.

        < ch : int : 1-8 >
            Specifies which input to configure (1-8).

        Returns:
            off_on, source, high_value, low_value, deadband, latch_enable
        """
        self.send('ALARM? %d'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        off_on = int(ret[0])
        source = int(ret[1])
        high_value = float(ret[2])
        low_value = float(ret[3])
        deadband = float(ret[4])
        latch_enable = int(ret[5])
        if printlog:
            print('ALARM? %d'%(ch))
            print('---------')
            print('off/on = %d'%(off_on))
            print('source = %d'%(source))
            print('high_value = %.3f'%(high_value))
            print('low_value = %.3f'%(low_value))
            print('deadband = %.3f'%(deadband))
            print('latch_enable = %d'%(latch_enable))
            print('')
            pass
        return off_on, source, high_value, low_value, deadband, latch_enable

    def alarm_query_all(self, printlog=True):
        """
        (Helper Method) ALARM? : Query Input Alarm Parameters
        -----------------------------------------------------
        Returns the alarm parameters of an input.

        Returns:
            off_on, source, high_value, low_value, deadband, latch_enable
        """
        off_on = []
        source = []
        high_value = []
        low_value = []
        deadband = []
        latch_enable = []
        for i in range(1, 9):
            ret = self.alarm_query(i, printlog=False)
            off_on.append(ret[0])
            source.append(ret[1])
            high_value.append(ret[2])
            low_value.append(ret[3])
            deadband.append(ret[4])
            latch_enable.append(ret[5])
            continue
        if printlog:
            sep = ''
            print('ALARM?')
            print('------')
            print('#   : ON/OFF, Sourse,    High,     Low, DeadBand, Latch')
            for i in range(8):
                print('ch%d :      %d,      %d, %07.3f, %07.3f,  %07.3f, %d'%
                      (i+1, off_on[i], source[i], high_value[i], low_value[i],
                       deadband[i], latch_enable[i]))
                continue
            print('')
            pass
        return off_on, source, high_value, low_value, deadband, latch_enable

    def alarm_status_query(self, ch=1, printlog=True):
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
        self.send('ALARMST? %d'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        high_status = int(ret[0])
        low_status = int(ret[1])
        if printlog:
            print('ALARMST? %d'%(ch))
            print('-----------')
            print('high_status = %d'%(high_status))
            print('low_status = %d'%(low_status))
            print('')
            pass
        return high_status, low_status

    def alarm_status_query_all(self, printlog=True):
        """
        (Helper Method) ALARMST? : Query Input Alarm Status
        ---------------------------------------------------
        Returns the alarm status of an input.

        Returns:
            high_status : Specifies high alarm status.
                          0 = Unactivated, 1 = Activated

            low_status : Specifies low alarm status.
                         0 = Unactivated, 1 = Activated
        """
        high_status = []
        low_status = []
        for i in range(1, 9):
            ret = self.alarm_status_query(i, printlog=False)
            high_status.append(ret[0])
            low_status.append(ret[1])
            continue
        if printlog:
            print('ALARMST?')
            print('--------')
            print('#   : High, Low')
            for i in range(8):
                print('ch%d :    %d,  %d'%(i+1, high_status[i], low_status[i]))
                continue
            print('')
            pass
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
        self.send('ALMB %d'%(off_on))
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
        self.send('ALMB?')
        ret = self.com.readline()
        ret = int(ret)
        print('ALMB?')
        print('-----')
        print('off_on = %d'%(ret))
        print('')
        return ret

    def alarm_reset(self):
        """
        ALMRST : Clear Alarm Status for All Inputs
        ------------------------------------------
        Resets a latched active alarm after the alarm condition has cleared.
        """
        self.send('ALMRST')
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
        self.send('ANALOG %d, %d, %d, %d, %d, %.3f, %.3f, %.3f'%
                      (ch, bipolar_enable, mode, monitor_ch, source,
                       high_value, low_value, manual))
        return

    def analog_outputs_query(self, ch=1, printlog=True):
        """
        ANALOG? : Query Analog Output Parameters
        ----------------------------------------

        < ch : int : 1,2 >
            Specifies analog output to query (1 or 2).

        Returns:
            bipolar_enable, mode, monitor_ch, source, high_value,
            low_value, manual_value
        """
        self.send('ANALOG? %d'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        bipolar_enable = int(ret[0])
        mode = int(ret[1])
        monitor_ch = int(ret[2])
        source = int(ret[3])
        high_value = float(ret[4])
        low_value = float(ret[5])
        manual = float(ret[6])
        if printlog:
            print('ANALOG? %d'%(ch))
            print('----------')
            print('bipolar_enable = %d'%(bipolar_enable))
            print('mode = %d'%(mode))
            print('monitor_ch = %d'%(monitor_ch))
            print('source = %d'%(source))
            print('high_value = %.3f'%(high_value))
            print('low_value = %.3f'%(low_value))
            print('manual = %.3f'%(manual))
            print('')
            pass
        return (bipolar_enable, mode, monitor_ch, source, high_value,
                low_value, manual)

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
        self.send('AOUT? %d'%(ch))
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
        self.send('BAUD %d'%(bps))
        return

    def serial_interface_baud_rate_query(self):
        """
        BAUD? : Query Serial Interface Baud Rate.
        -----------------------------------------
        Returns serial interface baud rate.

        Returns:
            bps : 0 = 300, 1 = 1200, 2 = 9600.
        """
        self.send('BAUD?')
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
        self.send('CRDG? %d'%(ch))
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
        self.send('CRVDEL %d'%(curve_num))
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
        self.send('CRVHDR %d, %s, %s, %d, %.3f, %d'%
                      (curve_num, name, SN, format, limit_value, coefficient))
        return

    def curve_header_query(self, curve_num, printlog=True):
        """
        CRVHDR? : Configure Curve Header
        --------------------------------

        < curve_num : int : 21-28 >
            Specifies which curve to configure (21-28) for inputs 1-8.

        Returns:
            name, SN, format, limit_value, coefficient
        """
        self.send('CRVHDR? %d'%(curve_num))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        name = ret[0].strip()
        SN = ret[1].strip()
        format = int(ret[2])
        limit_value = float(ret[3])
        coefficient = int(ret[4])
        if printlog:
            print('CRVHDR? %d'%(curve_num))
            print('----------')
            print('name = %s'%(name))
            print('SN = %s'%(SN))
            print('format = %d'%(format))
            print('limit_value = %.3f'%(limit_value))
            print('coefficient = %d'%(coefficient))
            print('')
            pass
        return name, SN, format, limit_value, coefficient

    def curve_header_query_all(self, printlog=True):
        """
        (Helper Method) CRVHDR? : Configure Curve Header
        ------------------------------------------------

        Returns:
            name, SN, format, limit_value, coefficient
        """
        name = []
        SN = []
        format = []
        limit_value = []
        coefficient = []
        for i in range(1, 10) + range(21, 29):
            ret = self.curve_header_query(i, printlog=False)
            name.append(ret[0])
            SN.append(ret[1])
            format.append(ret[2])
            limit_value.append(ret[3])
            coefficient.append(ret[4])
            continue
        if printlog:
            print('CRVHDR?')
            print('-------')
            print('#       : %15s, %10s, %6s, %7s, %5s'%
                  ('name', 'serial #', 'format', 'limit', 'coeff'))
            for i, num in enumerate(range(1, 10) + range(21, 29)):
                print('curve%02d : %15s, %10s, %6d, %7.3f,  %5d'%
                      (num, name[i], SN[i], format[i], limit_value[i],
                       coefficient[i]))
                continue
            print('')
            pass
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
        self.send('CRVPT %d %d %s %s'%(curve_num, index, units, temp))
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
        self.send('CRVPT? %d %d'%(curve_num, index))
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
        print('uploading...')
        for i,(unit, temp) in enumerate(zip(units_values, temp_values)):
            if i>199: break
            sys.stdout.write('\r[%-10s] %d/200 %.1f %.1f'%
                             ('='*int(i/19), i+1, unit, temp))
            sys.stdout.flush()
            self.curve_point_set(curve_num, i+1, unit, temp)
            continue
        print('')
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
        print('downloading...')
        for i in range(200):
            _u, _t = self.curve_point_query(curve_num, i+1)
            unit.append(_u)
            temp.append(_t)
            sys.stdout.write('\r[%-10s] %d/200 %.1f %.1f'%
                             ('='*int(i/19), i+1, _u, _t))
            sys.stdout.flush()
            continue
        print('')
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
        self.send('DATETIME %d, %d, %d, %d, %d, %d'%
                      (month, day, year, hour, minutes, seconds))
        return

    def datetime_set_now(self):
        """
        (Helper Method) DATETIME : Configure Date and Time
        --------------------------------------------------
        Configures date and time to current time.
        """
        fmt = '%m,%d,%y,%H,%M,%S'
        datetime_str = datetime.datetime.now().strftime(fmt)
        self.send('DATETIME %s'%(datetime_str))
        return

    def datetime_query(self):
        """
        DATETIME? : Query Date and Time
        --------------------------------
        Returns date and time.

        Returns:
            timestamp
        """
        self.send('DATETIME?')
        ret = self.com.readline().strip()
        fmt = '%m,%d,%y,%H,%M,%S'
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
        self.send('DFLT %d'%(param))
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
        self.send('DISPFLD %d, %d, %d'%(location, sensor, source))
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
        self.send('DISPFLD? %d'%(location))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        sensor = int(ret[0])
        source = int(ret[1])
        return sensor, source

    def display_field_query_all(self, printlog=True):
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
            continue
        if printlog:
            print('DISPFLD?')
            print('--------')
            print('#         : %6s, %6s'%('sensor', 'source'))
            for i in range(8):
                print('display%02d : %6d, %6d'%(i+1, sensors[i], sources[i]))
                continue
            print('')

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
        self.send('FILTER %d, %d, %d, %d'%(ch, off_on, points, window))
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
        FILTER? : Query Input Filter Parameters
        ---------------------------------------

        < ch : int : 1-8 >
            Specifies input to configure (1-8).

        Returns:
            off_on, points, window
        """
        self.send('FILTER? %d'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        off_on = int(ret[0])
        points = int(ret[1])
        window = int(ret[2])
        return off_on, points, window

    def filter_query_all(self, printlog=True):
        """
        (Helper Method) FILTER? : Query Input Filter Parameters
        -------------------------------------------------------
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
        if printlog:
            print('FILTER?')
            print('-------')
            print('#   : %6s, %6s, %6s'%('ON_OFF', 'points', 'window'))
            for i in range(8):
                print('ch%d : %6d, %6d, %6d'%
                      (i+1, off_on[i], points[i], window[i]))
                continue
            print('')
            pass
        return off_on, points, window

    def ieee488_set(self, terminator=0, eoi=0, address=30):
        """
        IEEE : Configure IEEE-488 Interface Parameters
        ----------------------------------------------
        Configures parameters of the IEEE interface.

        < terminator : int : 0-3 >
            Specifies the terminator.
            0 = <CR><LF>, 1 = <LF><CR>, 2 = <LF>, 3 = no terminator.

        < eoi : int : 0,1 >
            Disables/enables the EOI mode.
            0 = Enabled, 1 = Disabled.

        < address : int : >
            Specifies the IEEE address.
        """
        self.send('IEEE %d, %d, %d'%(terminator, eoi, address))
        return

    def ieee488_query(self):
        """
        IEEE? : Query IEEE-488 Interface Parameters
        -------------------------------------------
        Returns IEEE interface parameters.

        Returns:
            terminator, eoi, address
        """
        self.send('IEEE?')
        ret = self.com.readline()
        ret = ret.strip().split(',')
        terminator = int(ret[0])
        eoi = int(ret[1])
        address = int(ret[2])
        return terminator, eoi, address

    def input_curve_set(self, ch, curve_number):
        """
        INCRV : Configure Input Curve Number
        ------------------------------------
        Specifies the curve an input uses for temperature conversion.

        < ch : int : 1-8 >
            Specifies which input to configure (1-8).

        < curve_number : int : 0-9,21-28 >
            Specifies which curve the input uses.
            0 = none, 1-5 = Standard Diode Curves,
            6-9 = Standard Platinum Curves, 21-28 = User curves.
            Note: Curve locations 10-20 not used.
        """
        self.send('INCRV %d %d'%(ch, curve_number))
        return

    def input_curve_query(self, ch):
        """
        INCRV? : Query Input Curve Number
        ---------------------------------
        Returns the input curve number.

        < ch : int : 1-8 >
            Specifies which input to configure (1-8).

        Returns:
            curve_number
        """
        self.send('INCRV? %d'%(ch))
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def input_curve_query_all(self, printlog=True):
        """
        (Helper Method) INCRV? : Query Input Curve Number
        -------------------------------------------------
        Returns the list of input curve numbers.

        Returns:
            curve_numbers
        """
        curves = [self.input_curve_query(i) for i in range(1, 9)]
        if printlog:
            print('INCRV?')
            print('------')
            print('#   : %7s'%('curve #'))
            for i in range(8):
                print('ch%d : %7d'%(i+1, curves[i]))
                continue
            print('')
            pass
        return curves

    def input_control_set(self, ch, off_on):
        """
        INPUT : Configure Input Control Parameter
        -----------------------------------------
        Turns selected input on or off.

        < ch : int : 1-8 >
            Specifies which input to configure(1-8).

        < off_on : int : 0,1 >
            Disables/Enables input.
            0 = Off, 1 = On.
        """
        self.send('INPUT %d %d'%(ch, off_on))
        return

    def input_control_query(self, ch):
        """
        INPUT? : Query Input Control Parameter
        --------------------------------------
        Returns selected input status.

        < ch : int : 1-8 >
            Specifies which input to configure(1-8).

        Returns:
            input_stauts
        """
        self.send('INPUT? %d'%(ch))
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def input_control_query_all(self, printlog=True):
        """
        (Helper Method) INPUT? : Query Input Control Parameter
        ------------------------------------------------------
        Returns all input status.

        Returns:
            input_stauts
        """
        status = [self.input_control_query(i) for i in range(1, 9)]
        if printlog:
            print('INPUT?')
            print('------')
            print('#   : %6s'%('status'))
            for i in range(8):
                print('ch%d : %6d'%(i+1, status[i]))
                continue
            print('')
            pass
        return status

    def input_type_set(self, group, sensor_type):
        """
        INTYPE : Configure Input Type Parameters
        ----------------------------------------
        Configures input type parameters for a group of inputs.

        < group : str[1] : A,B >
            Specifies input group to configure.
            A = inputs 1-4, B = inputs 5-8.

        < sensor_type : int :  >
            Specifies input sensor type. Valid entries:
            0 = 2.5V Diode, 1 = 7.5V Diode, 2 = 250ohm Platinum,
            3 = 500ohm Platinum, 4 = 5kohm Platinum, 5 = Cernox
        """
        self.send('INTYPE %s, %d'%(group, sensor_type))
        return

    def input_type_query(self, group):
        """
        INTYPE? : Query Input Type Parameters
        -------------------------------------
        Returns input type parameters.

        < group : str[1] : A,B >
            Specifies input group to configure.
            A = inputs 1-4, B = inputs 5-8.

        Returns:
            sensor_type
        """
        self.send('INTYPE? %s'%(group))
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def input_type_query_all(self):
        """
        (Helper Method) INTYPE? : Query Input Type Parameters
        -----------------------------------------------------
        Returns list of input type parameters.

        Returns:
            sensor_types
        """
        sensor_types = [self.input_type_query(g) for g in ('A', 'B')]
        return sensor_types

    def keypad_status_query(self):
        """
        KEYST? : Query Keypad Status
        ----------------------------
        Returns keypad status since the last KEYST?.

        Returns:
            status : 1 = key pressed,
                     0 = no key pressed.
                     NOTE: KEYST? returns 1 after initial power-up.
        """
        self.send('KEYST?')
        ret = self.com.readline()
        ret = int(ret)
        return ret

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
        self.send('KRDG? %d '%(ch))
        ret = self.com.readline()
        ret = map(float, ret.decode('utf-8').strip().split(','))
        if ch!=0: ret = ret[0]
        return ret

    def linear_equation_set(self, ch, m, source, b):
        """
        LINEAR : Configure Input Linear Equation Parameters
        ---------------------------------------------------
        Configures the linear equation for an input.
        y = m * x(source) + b

        < ch : int : 1-8 >
            Specifies input to configure (1-8).

        < m : float :  >
            Specifies a value for m in the equation.

        < source : int : 1-3 >
            Specifies input data.
            1 = Kelvin, 2 = Celsius, 3 = sensor units.

        < b : float :  >
            Specifies a value for b in the equation.
        """
        self.send('LINEAR %d, %.3f, %d, %.3f'%(ch, m, source, b))
        return

    def linear_equation_query(self, ch):
        """
        LINEAR? : Query Input Linear Equation Parameters
        ------------------------------------------------
        Returns input linear equation configuration.
        y = m * x(source) + b

        < ch : int : 1-8 >
            Specifies input to configure (1-8).

        Returns:
            m, source, b
        """
        self.send('LINEAR? %d'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        m = float(ret[0])
        source = int(ret[1])
        b = float(ret[2])
        return m, source, b

    def linear_equation_query_all(self, printlog=True):
        """
        (Helper Method) LINEAR? : Query Input Linear Equation Parameters
        ---------------------------------------------------------------
        Returns input linear equation configuration for all ch.
        y = m * x(source) + b

        Returns:
            m, source, b
        """
        m = []
        source = []
        b = []
        for i in range(1, 9):
            _m, _s, _b = self.linear_equation_query(i)
            m.append(_m)
            source.append(_s)
            b.append(_b)
            continue
        if printlog:
            print('LINEAR?')
            print('-------')
            print('#   : %7s, %6s, %7s'%('m', 'source', 'b'))
            for i in range(8):
                print('ch%d : %7.3f, %6d, %7.3f'%
                      (i+1, m[i], source[i], b[i]))
                continue
            print('')
            pass
        return m, source, b

    def lockout_set(self, off_on=0, code=123):
        """
        LOCK : Configure Lock-out and Lock-out Code
        -------------------------------------------
        Configures keypad lock-out and lock-out code.

        < off_on : int : 0,1 >
            Disables/enables the keypad lock-out.
            0 = OFF, 1 = ON

        < code : int : 0-999 >
            Specifies lock-out code. 000 - 999.
        """
        self.send('LOCK %d %d'%(off_on, code))
        return

    def lockout_query(self):
        """
        LOCK? : Query Lock-out and Lock-out Code
        ----------------------------------------
        Returns lock-out status and lock-out code.

        Returns:
            off_on, code
        """
        self.send('LOCK?')
        ret = self.com.readline()
        ret = ret.strip().split(',')
        off_on = int(ret[0])
        code = int(ret[1])
        return off_on, code

    def logging_on_off(self, off_on):
        """
        LOG : Turns Logging On and Off
        ------------------------------
        Turns logging on and off.

        < off_on : int : 0,1 >
            0 = Off, 1 = On.
        """
        self.send('LOG %d'%(off_on))
        return

    def logging_on_off_query(self):
        """
        LOG? : Query Logging Status
        ---------------------------
        Returns logging status.

        Returns:
            off_on
        """
        self.send('LOG?')
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def logging_number_query(self):
        """
        LOGNUM? : Query Number of Last Data Log Record Stored
        ----------------------------------------------------
        Returns number of last data log record stored.

        Returns:
            log_num
        """
        self.send('LOGNUM?')
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def logging_records_set(self, reading_number, ch, source):
        """
        LOGREAD : Configure Log Records
        -------------------------------
        Configures log records.

        < reading_number : int : 1-8 >
            The individual reading number (1-8) within a log record to
            configure.

        < ch : int : 1-8 >
            The input number to log (1-8).

        < source : int : 1-4 >
            Specifies data source to log.
            1 = Kelvin, 2 = Celsius, 3 = sensor units, 4 = linear data.
        """
        self.send('LOGREAD %d, %d, %d'%(reading_number, ch, source))
        return

    def logging_records_query(self, reading_number):
        """
        LOGREAD? : Query Log Records
        ----------------------------
        Returns log record parameters.

        < reading_number : int : 1-8 >
            The individual reading number (1-8) within a log record to
            configure.

        Returns:
            ch, source
        """
        self.send('LOGREAD? %d'%(reading_number))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        ch = int(ret[0])
        source = int(ret[1])
        return ch, source

    def logging_records_query_all(self, printlog=True):
        """
        (Helper Method) LOGREAD? : Query Log Records
        --------------------------------------------
        Returns log record parameters for all records.

        Returns:
            ch, source
        """
        ch = []
        source = []
        for i in range(1, 9):
            _c, _s = self.logging_records_query(i)
            ch.append(_c)
            source.append(_s)
            continue
        if printlog:
            print('LOGREAD?')
            print('--------')
            print('#   : %6s, %6s'%('sensor', 'source'))
            for i in range(8):
                print('ch%d : %6d, %6d'%
                      (i+1, ch[i], source[i]))
                continue
            print('')
            pass
        return ch, source

    def logging_parameter_set(self, mode, overwrite, start, period, readings):
        """
        LOGSET : Configure Logging Parameters
        -------------------------------------
        Configures logging parameters.

        < mode : int : 0-4 >
            Specifies logging mode.
            0 = Off, 1 = Log Continuous, 2 = Log event,
            3 = Print Continuous, 4 = Print Event.

        < overwrite : int : 0,1 >
            Specifies overwrite mode.
            0 = Do not overwrite data, 1 = overwrite data.

        < start : int : 0,1 >
            Specifies start mode. 0 = Clear, 1 = Continue.

        < period : int : 1-3600 >
            Specifies period in seconds (1-3600).
            If mode is Print Continuous, minimum period is 10.

        < readings : int : 1-8 >
            Specifies number of readings per record (1-8).
        """
        self.send('LOGSET %d, %d, %d, %d, %d'%(mode, overwrite, start,
                                                   period, readings))
        return

    def logging_parameter_query(self):
        """
        LOGSET? : Query Logging Parameters
        ----------------------------------
        Returns logging parameters.

        Returns:
            mode, overwrite, start, period, readings
        """
        self.send('LOGSET?')
        ret = self.com.readline()
        ret = ret.strip().split(',')
        mode = int(ret[0])
        overwrite = int(ret[1])
        start = int(ret[2])
        period = int(ret[3])
        readings = int(ret[4])
        return mode, overwrite, start, period, readings

    def log_data_query(self, record_number, reading_number):
        """
        LOGVIEW? : Querya Logged Data Record
        ------------------------------------
        Returns a single reading from a logged data record.

        < record_number : int :  >

        < reading_number : int : 1-8 >
            The individual reading number (1-8) within a log record to
            configure.

        Returns:
            datetime, reading, status, source
        """
        self.send('LOGVIEW? %d, %d'%(record_number, reading_number))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        date = ret[0]
        time = ret[1]
        fmt = '%m/%d/%y%H:%M:%S'
        datime = datetime.datetime.strptime(date+time, fmt)
        reading = float(ret[2])
        status = int(ret[3])
        source = int(ret[4])
        return datime, reading, status, source

    def linear_equation_input_data_query(self, ch=0):
        """
        LRDG? : Query Linear Equation Data for a Single Input or All Inputs.
        --------------------------------------------------------------------
        Returns the linear equation data for an input.

        < ch : int : 0-8 >
            0 = all inputs. Return a list of float values.
            1-8 = individual input. Return a float value.

        NOTE: Use 0 (all inputs) when reading two or more inputs
              at the maximum update rate of 16 rdg/s.
        """
        self.send('LRDG? %d'%(ch))
        ret = self.com.readline()
        ret = map(float, ret.strip().split(','))
        if ch!=0: ret = ret[0]
        return ret

    def minmax_set(self, ch, source):
        """
        MNMX : Configure Minimum and Maximum Input Function Parameters
        --------------------------------------------------------------
        Configures the minimum and maximum input functions.

        < ch : int : 1-8 >
            Specifies input to configure (1-8).

        < source : int : 1-4 >
            Specifies input data to process through max/min.
            1 = Kelvin, 2 = Celsius, 3 = sensor units, 4 = linear data.
        """
        self.send('MNMX %d %d'%(ch, source))
        return

    def minmax_query(self, ch):
        """
        MNMX? : Query Minimum and Maximum Input Function Parameters
        -----------------------------------------------------------
        Returns an input min/max configuration.

        < ch : int : 1-8 >
            Specifies input to configure (1-8).

        Returns:
            source
        """
        self.send('MNMX? %d'%(ch))
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def minmax_data_query(self, ch):
        """
        MNMXRDG? : Query Min/Max Data for an Input
        ------------------------------------------
        Returns the minimum and maximum input data.

        < ch : int : 1-8 >
            Specifies input to configure (1-8).

        Returns:
            min_value, max_value
        """
        self.send('MNMXRDG? %d'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        min_value = float(ret[0])
        max_value = float(ret[1])
        return min_value, max_value

    def minmax_function_reset(self):
        """
        MNMXRST : Resets Min/Max Function for All Inputs
        ------------------------------------------------
        Resets the minimum and maximum data for all inputs.
        """
        self.send('MNMXRST')
        return

    def local_remote_mode_set(self, mode):
        """
        MODE : Configure Remote Interface Mode
        --------------------------------------
        Configures the remote interface mode.

        < mode : int : 0-2 >
            specifies which mode to operate.
            0 = local, 1 = remote, 2 = remote with local lockout.
        """
        self.send('MODE %d'%(mode))
        return

    def local_remote_mode_query(self):
        """
        MODE? : Query Remote Interface Mode
        -----------------------------------
        Returns the remote interface mode.

        Returns:
            mode
        """
        self.send('MODE?')
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def reading_status_query(self, ch):
        """
        RDGST? : Query Input Status
        ---------------------------
        The integer returned represents the sum of the bit weighting of the
        input status flag bits.

        < ch : int : 1-8 >
            specifies which input to query.

        Returns:
            status
        """
        self.send('RDGST? %d'%(ch))
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def relay_set(self, relay_number, mode, input_alarm, alarm_type):
        """
        RELAY : Configure Relay Control Parameters
        ------------------------------------------
        Configures relay control.

        < relay_number : int : 1-8 >
            Specifies which relay to configure (1-8).

        < mode : int : 0-2 >
            Specifies relay mode. 0 = Off, 1 = On, 2 = Alarms

        < input_alarm : int : 1-8 >
            Specifies which input alarm activates the relay when the relay
            is in alarm mode (1-8).

        < alarm_type : int : 0-2 >
            Specifies the input alarm type that activates the relay when the
            relay is in alarm mode.
            0 = Low alarm, 1 = High Alarm, 2 = Both Alarms.
        """
        self.send('RELAY %d, %d, %d, %d'%(relay_number, mode,
                                              input_alarm, alarm_type))
        return

    def relay_query(self, relay_number):
        """
        RELAY? : Query Relay Control Parameters
        ---------------------------------------
        The integer returned represents the sum of the bit weighting of the
        relay status.

        < relay_number : int : 1-8 >
            Specifies which relay to configure (1-8).

        Returns:
            mode, input_alarm, alarm_type
        """
        self.send('RELAY? %d'%(relay_number))
        ret = self.com.readline()
        ret = self.com.readline()
        ret = ret.strip().split(',')
        mode = int(ret[0])
        input_alarm = int(ret[1])
        alarm_type = int(ret[2])
        return mode, input_alarm, alarm_type

    def relay_status_query(self):
        """
        RELAYST? : Query Relay Status
        -----------------------------
        The integer returned represents the sum of the bit weighting of the
        relay status.

        Returns:
            status
        """
        self.send('RELAYST?')
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def softcal_curve_generate(self, std, dest, SN, T1, U1, T2, U2, T3, U3):
        """
        SCAL : Generate SoftCal Curve
        -----------------------------

        < std : int : 1,6,7 >
        < dest : int : 21-28 >
        < SN : str[10] :  >
        < T1 : float : >
        < U1 : float : >
        < T2 : float : >
        < U2 : float : >
        < T3 : float : >
        < U3 : float : >
        """
        self.send('SCAL %d, %d, %s, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f'%
                      (std, dest, SN, T1, U1, T2, U2, T3, U3))
        return

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
        self.send('SRDG? %d'%(ch))
        ret = self.com.readline()
        ret = map(float, ret.strip().split(','))
        if ch!=0: ret = ret[0]
        return ret

    _shortcut_command = {'ALARM': 'alarm_set',
                         'ALARMQ': 'alarm_query',
                         'ALARMSTQ': 'alarm_status_query',
                         'ALMB': 'audible_alarm_set',
                         'ALMBQ': 'audible_alarm_query',
                         'ALMRST': 'alarm_reset',
                         'ANALOG': 'analog_outputs_set',
                         'ANALOGQ': 'analog_outputs_query',
                         'AOUTQ': 'analog_output_data_query',
                         'BAUD': 'serial_interface_baud_rate_set',
                         'BAUDQ': 'serial_interface_baud_rate_query',
                         'CRDGQ': 'celsius_reading_query',
                         'CRVDEL': 'curve_delete',
                         'CRVHDR': 'curve_header_set',
                         'CRVHDRQ': 'curve_header_query',
                         'CRVPT': 'curve_point_set',
                         'CRVPTQ': 'curve_point_query',
                         'DATETIME': 'datetime_set',
                         'DATETIMEQ': 'datetime_query',
                         'DFLT': 'factory_defaults_reset',
                         'DISPFLD': 'display_field_set',
                         'DISPFLDQ': 'display_field_query',
                         'FILTER': 'filter_set',
                         'FILTERQ': 'filter_query',
                         'IEEE': 'ieee488_set',
                         'IEEEQ': 'ieee488_query',
                         'INCRV': 'input_curve_set',
                         'INCRVQ': 'input_curve_query',
                         'INPUT': 'input_control_set',
                         'INPUTQ': 'input_control_query',
                         'INTYPE': 'input_type_set',
                         'INTYPEQ': 'input_type_query',
                         'KEYSTQ': 'keypad_status_query',
                         'KRDGQ': 'kelvin_reading_query',
                         'LINEAR': 'linear_equation_set',
                         'LINEARQ': 'linear_equation_query',
                         'LOCK': 'lockout_set',
                         'LOCKQ': 'lockout_query',
                         'LOG': 'logging_on_off',
                         'LOGQ': 'logging_on_off_query',
                         'LOGNUMQ': 'logging_number_query',
                         'LOGREAD': 'logging_records_set',
                         'LOGREADQ': 'logging_records_query',
                         'LOGSET': 'logging_parameter_set',
                         'LOGSETQ': 'logging_parameter_query',
                         'LOGVIEWQ': 'log_data_query',
                         'LRDGQ': 'linear_equation_input_data_query',
                         'MNMX': 'minmax_set',
                         'MNMXQ': 'minmax_query',
                         'MNMXRDGQ': 'minmax_data_query',
                         'MNMXRST': 'minmax_function_reset',
                         'MODE': 'local_remote_mode_set',
                         'MODEQ': 'local_remote_mode_query',
                         'RDGSTQ': 'reading_status_query',
                         'RELAY': 'relay_set',
                         'RELAYQ': 'relay_query',
                         'RELAYSTQ': 'relay_status_query',
                         'SCAL': 'softcal_curve_generate',
                         'SRDGQ': 'sensor_units_reading_query'}
