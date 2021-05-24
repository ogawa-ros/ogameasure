import sys
import datetime
from ..SCPI import scpi

class model331(scpi.scpi_family):
    manufacturer = 'Lakeshore'
    product_name = 'model 331'
    classification = 'Temperature Controller'

    _scpi_enable = '*CLS *ESE *ESE? *ESR? *IDN? *OPC *OPC? *RST *SRE ' \
                   + '*SRE? *STB? *TST? *WAI'

    """
    def __init__(self, com):
        scpi.scpi_family.__init__(self, com)
        self.com.com.readline()
        pass
    """

    def alarm_set(self, ch='A', off_on=1, source=1, high_value=300,
                  low_value=100, deadband=1, latch_enable=0):
        """
        ALARM : Configure Input Alarm Parameters
        ----------------------------------------
        Configures the alarm parameters for an input.

        < ch : char : A, B >
            Specifies which input to configure (A or B).

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

        < latch_enable : int : 0,1>
            Specifies a latched alarm (remains active after alarm condition
            correction) where 0 = off (no latch) and 1 = on.
        """
        self.com.send('ALARM %s, %d, %d %.3f, %.3f, %.3f, %d'%
                      (ch, off_on, source, high_value, low_value, deadband,
                       latch_enable))
        return

    def alarm_query(self, ch='A', printlog=True):
        """
        ALARM? : Query Input Alarm Parameters
        -------------------------------------
        Returns the alarm parameters of an input.

        < ch : char : A, B >
            Specifies which input to configure (A or B).

        Returns:
            off_on, source, high_value, low_value, deadband, latch_enable
        """
        self.com.send('ALARM? %s'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        off_on = int(ret[0])
        source = int(ret[1])
        high_value = float(ret[2])
        low_value = float(ret[3])
        deadband = float(ret[4])
        latch_enable = int(ret[5])
        if printlog:
            print('ALARM? %s'%(ch))
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
        for i in ['A', 'B']:
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
            for i, ch in enumerate(['A', 'B']):
                print('ch %s :      %d,      %d, %07.3f, %07.3f,  %07.3f, %d'%
                      (ch, off_on[i], source[i], high_value[i], low_value[i],
                       deadband[i], latch_enable[i]))
                continue
            print('')
            pass
        return off_on, source, high_value, low_value, deadband, latch_enable

    def alarm_status_query(self, ch='A', printlog=True):
        """
        ALARMST? : Query Input Alarm Status
        -----------------------------------
        Returns the alarm status of an input.

        < ch : char : A, B >
            Specifies which input to configure (A or B).

        Returns:
            high_status : Specifies high alarm status.
                          0 = Off, 1 = On

            low_status : Specifies low alarm status.
                         0 = Off, 1 = On
        """
        self.com.send('ALARMST? %s'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        high_status = int(ret[0])
        low_status = int(ret[1])
        if printlog:
            print('ALARMST? %s'%(ch))
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
                          0 = Off, 1 = On

            low_status : Specifies low alarm status.
                         0 = Off, 1 = On
        """
        high_status = []
        low_status = []
        for i in ['A','B']:
            ret = self.alarm_status_query(i, printlog=False)
            high_status.append(ret[0])
            low_status.append(ret[1])
            continue
        if printlog:
            print('ALARMST?')
            print('--------')
            print('#   : High, Low')
            for i, ch in enumerate(['A', 'B']):
                print('ch %s :    %d,  %d'%(ch, high_status[i], low_status[i]))
                continue
            print('')
            pass
        return high_status, low_status

    def alarm_reset(self):
        """
        ALMRST : Clear Alarm Status for All Inputs
        ------------------------------------------
        Resets a latched active alarm after the alarm condition has cleared.
        """
        self.com.send('ALMRST')
        return

    def analog_outputs_set(self, bipolar_enable=0, mode=1, monitor_ch='A',
                           source=1, high_value=200, low_value=2, manual=0):
        """
        ANALOG : Configure Analog Output Parameters
        -------------------------------------------
        Configure Analog Output Parameters.

        < bipolar_enable : int : 0,1 >
            Specifies analog output:
            0 = positive only, 1 = bipolar.

        < mode : int : 0,1,2,3 >
            Specifies data the analog output monitors:
            0 = off, 1 = input, 2 = manual, 3 = loop.

        < monitor_ch : char : A, B >
            Specifies which input to monitor if <mode> = 1 (A or B).

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
        self.com.send('ANALOG %d, %d, %s, %d, %.3f, %.3f, %.3f'%
                      (bipolar_enable, mode, monitor_ch, source,
                       high_value, low_value, manual))
        return

    def analog_outputs_query(self, printlog=True):
        """
        ANALOG? : Query Analog Output Parameters
        ----------------------------------------
        
        Returns:
            bipolar_enable, mode, monitor_ch, source, high_value,
            low_value, manual_value
        """
        self.com.send('ANALOG?')
        ret = self.com.readline()
        ret = ret.strip().split(',')
        bipolar_enable = int(ret[0])
        mode = int(ret[1])
        monitor_ch = ret[2].strip()
        source = int(ret[3])
        high_value = float(ret[4])
        low_value = float(ret[5])
        manual = float(ret[6])
        if printlog:
            print('ANALOG?')
            print('-------')
            print('bipolar_enable = %d'%(bipolar_enable))
            print('mode = %d'%(mode))
            print('monitor_ch = %s'%(monitor_ch))
            print('source = %d'%(source))
            print('high_value = %.3f'%(high_value))
            print('low_value = %.3f'%(low_value))
            print('manual = %.3f'%(manual))
            print('')
            pass
        return (bipolar_enable, mode, monitor_ch, source, high_value,
                low_value, manual)

    def analog_output_data_query(self):
        """
        AOUT? : Query Analog Output Data
        --------------------------------
        Returns the percentage of output.

        Returns:
            output
        """
        self.com.send('AOUT?')
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

    def serial_interface_baud_rate_query(self, printlog=True):
        """
        BAUD? : Query Serial Interface Baud Rate.
        -----------------------------------------
        Returns serial interface baud rate.

        Returns:
            bps : 0 = 300, 1 = 1200, 2 = 9600.
        """
        self.com.send('BAUD?')
        ret = self.com.readline()
        ret = int(ret)

        bps = {
            0: 300,
            1: 1200,
            2: 9600,
        }
        
        if printlog:
            print('BAUD?')
            print('-----')
            print('bps = %d bps'%(bps[ret]))
            print('')
            pass
        
        return ret

    def alarm_beeper_command(self, state=1):
        """
        BEEP : Alarm Beeper Command.
        ----------------------------
        Enables or disables system beeper sound when an alarm condition is met.
        
        < state : int : 0, 1>
            State of alarm beep : 0 = Off, 1 = On
        """
        self.com.send('BEEP %d'%(state))
        return

    def alarm_beeper_query(self):
        """
        BEEP? : Alarm Beeper Query.
        ---------------------------
        Returns state of alarm beeper.
        
        Returns:
            state : 0 = Off, 1 = On
        """
        self.com.send('BEEP?')
        ret = self.com.readline()
        ret = int(ret)
        return ret
    
    def display_brightness_command(self, bright=2):
        """
        BRIGT : Display Brightness Command.
        -----------------------------------
        Sets display brightness.
        
        < bright : int : 0,1,2,3 >
            0 = 25%, 1 = 50%, 2 = 75%, 3 = 100%
            (Default = 2)
        """
        self.com.send('BRIGT %d'%(bright))
        return

    def display_brightness_query(self, printlog=True):
        """
        BRIGT? : Display Brightness Query.
        ----------------------------------
        Returns display brightness.
        
        Returns:
            brightness : 0 = 25%, 1 = 50%, 2 = 75%, 3 = 100%
        """
        self.com.send('BRIGT?')
        ret = self.com.readline()
        ret = int(ret)

        brightness = {
            0: '25%',
            1: '50%',
            2: '75%',
            3: '100%',
        }
        
        if printlog:
            print('BRIGT?')
            print('------')
            print('brightness = %s'%(brightness[ret]))
            print('')
            pass

        return ret
    
    def control_loop_mode_command(self, loop=1, mode=1):
        """
        CMODE : Control Loop Mode Command.
        ----------------------------------
        Sets control loop mode.
        
        < loop : int : 1,2 >
            Specifies which loop to configure (1, 2).
        
        < mode : int : 1-6 >
            Specifies the control mode:
              1 = Manual PID
              2 = Zone
              3 = Open Loop
              4 = Auto Tune PID
              5 = Auto Tune PI
              6 = Auto Tune P
        """
        self.com.send('CMODE %d, %d'%(loop, mode))
        return

    def control_loop_mode_query(self, loop=1, printlog=True):
        """
        CMODE? : Control Loop Mode Query.
        ---------------------------------
        Returns control loop mode.
        
        < loop : int : 1,2 >
            Specifies which loop to configure (1, 2).
        
        Returns:
            loop : loop number (1, 2)
            mode : control mode
                1 = Manual PID
                2 = Zone
                3 = Open Loop
                4 = Auto Tune PID
                5 = Auto Tune PI
                6 = Auto Tune P
        """
        self.com.send('CMODE? %d'%(loop))
        
        ret = self.com.readline()
        ret = int(ret)
        
        mode = {
            0: 'Manual PID',
            1: 'Zone',
            2: 'Open Loop',
            3: 'Auto Tune PID',
            4: 'Auto Tune PI',
            5: 'Auto Tune P',
        }
        
        if printlog:
            print('CMODE? %d'%(loop))
            print('---------')
            print('mode = %s'%(mode[ret]))
            print('')
            pass

        return ret
        return

    def celsius_reading_query(self, ch='A'):
        """
        CRDG? : Query Celsius Reading for Single Input
        ----------------------------------------------
        Returns the Celsius reading for a single input.

        < ch : int : A, B >
            channel to read (A, B).
        """
        self.com.send('CRDG? %s'%(ch))
        ret = self.com.readline()
        ret = float(ret)
        return ret

    def curve_delete(self, curve_num):
        """
        CRVDEL : Delete User Curve
        --------------------------
        Deletes a user curve.

        < curve_num : int : 21-41 >
            Specifies which curve to delete (21-41).
        """
        self.com.send('CRVDEL %d'%(curve_num))
        return

    def curve_header_set(self, curve_num, name, SN, format, limit_value,
                         coefficient):
        """
        CRVHDR : Configure Curve Header
        -------------------------------

        < curve_num : int : 21-41 >
            Specifies which curve to configure (21-41).

        < name : str[15] : >
            Specifies curve name. Limited to 15 characters.

        < SN : str[10] :  >
            Specifies curve serial number. Limited to 10 characters.

        < format : int : 1-4 >
            Specifies curve data format.
            1 = mV/K, 2 = V/K, 3 = Ohm/K, 4 = log Ohm/K

        < limit_value : float : >
            Specifies curve temperature limit in Kelvin.

        < coefficient : int : 1,2 >
            Specifies curve temperature coefficient.
            1 = negative, 2 = positive.
        """
        self.com.send('CRVHDR %d, %s, %s, %d, %.3f, %d'%
                      (curve_num, name, SN, format, limit_value, coefficient))
        return

    def curve_header_query(self, curve_num, printlog=True):
        """
        CRVHDR? : Configure Curve Header
        --------------------------------

        < curve_num : int : 1-41 >
            Specifies which curve to configure (1-41).
        
        Returns:
            name, SN, format, limit_value, coefficient
        """
        self.com.send('CRVHDR? %d'%(curve_num))
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

    def curve_point_set(self, curve_num, index, units_value, temp_value):
        """
        CRVPT : Configure Curve Data Point
        ----------------------------------
        Configures a user curve data point.

        < curve_num : int : 21-41 >
            Specifies which curve to configure (21-41).

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
        self.com.send('CRVPT %d, %d, %s, %s'%(curve_num, index, units, temp))
        return

    def curve_point_query(self, curve_num, index):
        """
        CRVPT? : Query Curve Data Point
        -------------------------------
        Returns a standard or user curve data point.

        < curve_num : int : 1-41 >
            Specifies which curve to query.
        
        < index : int : 1-200 >
            Specifies the points index in the curve (1 - 200).

        Returns:
            units_value, temp_value
        """
        self.com.send('CRVPT? %d, %d'%(curve_num, index))
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

        < curve_num : int : 21-41 >
            Specifies which curve to configure (21-41).

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

        < curve_num : int : 1-41 >
            Specifies which curve to query.

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

    def control_loop_parameter_command(self, loop, input_, units, powerup, current_power):
        """
        CSET : Control Loop Parameter Command
        -------------------------------------
        Configutes control loop parameters

        < loop : int : 1, 2 >
            Specifies which loop to configure (1 or 2).

        < input_ : cahr : A, B >
            Specifies which input to control from: A or B.

        < units : int : 1, 2, 3 >
            Specifies setpoint units.
                1 = Kelvin, 2 = Celsius, 3 = Sensor units.

        < powerup : int : 0,1 >
            Specifies whether the control loop is on or off after power-up
                0 = power-up enable off
                1 = power-up enable on
        
        < current_power : int : 1, 2 >
            Specifies whether the heater output displays in current or power.
                1 = current
                2 = power
        """
        self.com.send('CSET %d, %s, %d, %d'%(curve_num, index, units, temp))
        return

    def control_loop_parameter_query(self, loop, printlog=True):
        """
        CSET? : Query Control Loop Parameter 
        ------------------------------------
        Returns control loop parameters.

        < loop : int : 1,2 >
            Specifies which loop to query (1 or 2).
        
        Returns:
            input : A or B
            units : 1 = Kelvin, 2 = Celsius, 3 = Sensor units
            powerup : 0 = enable, 1 = disable
            current_power : 1 = current, 2 = power
        """
        self.com.send('CSET? %d'%(loop))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        input_ = ret[0]
        units = int(ret[1])
        powerup = int(ret[2])
        current_power = int(ret[3])

        if printlog:
            print('CSET? %d'%(loop))
            print('--------')
            print('input = %s'%(input_))
            print('units = %d'%(units))
            print('powerup_enable = %d'%(powerup))
            print('current_power = %d'%(current_power))
            print('')
            pass
        
        return input_, units, powerup, current_power
    
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

    def display_field_set(self, location, item, source):
        """
        DISPFLD : Configure Display Parameters
        --------------------------------------
        Configures the display parameters.

        < location : int : 1-4 >
            Specifies display location to configure (1-4).

        < item : int : 0-4 >
            Specifies item to display:
                0 = Off
                1 = Input A
                2 = Input B
                3 = Setpoint
                4 = Heater Output

        < source : int : 1-6 >
            Specifies input data to display.
            1 = Kelvin, 2 = Celsius, 3 = sensorunits, 4 = linear data,
            5 = minimum data, 6 = maximum data.
        """
        self.com.send('DISPFLD %d, %d, %d'%(location, sensor, source))
        return

    def display_field_query(self, location):
        """
        DISPFLD? : Query Display Field
        ------------------------------
        Returns the parameters for a displayed field.

        < location : int : 1-4 >
            Specifies display location to configure (1-4).

        Returns:
            sensor, source
        """
        self.com.send('DISPFLD? %d'%(location))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        item = int(ret[0])
        source = int(ret[1])
        return item, source

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
        
        ret2item = {
            0: 'OFF',
            1: 'Input A',
            2: 'Input B',
            3: 'Setpoint',
            4: 'Heater Out',
        }

        ret2source = {
            1: 'K',
            2: 'C',
            3: 'Sensour unit',
            4: 'Linear data',
            5: 'Min. data',
            6: 'Max. data',
        }
        
        for i in range(1,5):
            _se, _so = self.display_field_query(i)
            sensors.append(_se)
            sources.append(_so)
            continue
        if printlog:
            print('DISPFLD?')
            print('--------')
            print('#  : %10s, %12s'%('sensor', 'source'))
            for i in range(4):
                print('%02d : %10s, %12s'%(i+1,
                                           ret2item[sensors[i]],
                                           ret2source[sources[i]]))
                continue
            print('')
            
        return sensors, sources

    def filter_set(self, ch='A', off_on=1, points=5, window=2):
        """
        FILTER : Configure Input Filter Parameters
        ------------------------------------------

        < ch : char : A, B >
            Specifies input to configure (A, B).

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
        self.com.send('FILTER %s, %d, %d, %d'%(ch, off_on, points, window))
        return

    def filter_query(self, ch='A'):
        """
        FILTER? : Query Input Filter Parameters
        ---------------------------------------

        < ch : char : A, B >
            Specifies input to configure (A, B).

        Returns:
            off_on, points, window
        """
        self.com.send('FILTER? %s'%(ch))
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
        for i in ['A', 'B']:
            _o, _p, _w = self.filter_query(i)
            off_on.append(_o)
            points.append(_p)
            window.append(_w)
            continue
        if printlog:
            print('FILTER?')
            print('-------')
            print('#   : %6s, %6s, %6s'%('ON_OFF', 'points', 'window'))
            for i, ch in enumerate(['A', 'B']):
                print('ch %s : %6d, %6d, %6d'%
                      (ch, off_on[i], points[i], window[i]))
                continue
            print('')
            pass
        return off_on, points, window
    
    def heater_output_query(self):
        """
        HTR? : Heater Output Query
        --------------------------
        Returns heater value

        Returns:
            heater_output (%)
        """
        self.com.send('HTR?')
        ret = self.com.readline()
        ret = float(ret)
        return ret

    def heater_status_query(self, printlog=True):
        """
        HTRST? : Query Heater status
        ----------------------------
        Returns heater status

        Returns:
            status
                0 = no error
                1 = heater open load
                2 = heater short
        """
        self.com.send('HTRST?')
        ret = self.com.readline()
        ret = int(ret)
        
        status = {
            0: 'No error',
            1: 'Open load',
            2: 'Short',
        }
        if printlog:
            print('HTRST?')
            print('------')
            print('status = %s'%(status[ret]))
            print('')
        return ret

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
        self.com.send('IEEE %d, %d, %d'%(terminator, eoi, address))
        return

    def ieee488_query(self):
        """
        IEEE? : Query IEEE-488 Interface Parameters
        -------------------------------------------
        Returns IEEE interface parameters.

        Returns:
            terminator, eoi, address
        """
        self.com.send('IEEE?')
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

        < ch : char : A, B >
            Specifies which input to configure (A or B).

        < curve_number : int : 0-41 >
            Specifies which curve the input uses.
                0 = none,
                1-20 = Standard Diode Curves,
                21-41 = User curves.
        """
        self.com.send('INCRV %s %d'%(ch, curve_number))
        return

    def input_curve_query(self, ch):
        """
        INCRV? : Query Input Curve Number
        ---------------------------------
        Returns the input curve number.

        < ch : int : A, B >
            Specifies which input to configure (A or B).

        Returns:
            curve_number
        """
        self.com.send('INCRV? %s'%(ch))
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def input_type_set(self, ch, sensor_type, compensation):
        """
        INTYPE : Configure Input Type Parameters
        ----------------------------------------
        Configures input type parameters for a group of inputs.

        < ch : str[1] : A,B >
            Specifies input ch to configure (A or B).

        < sensor_type : int : 0-9 >
            Specifies input sensor type:
                0 = Silicon Diode
                1 = GaAlAs Diode
                2 = 100 Ohm Platinum / 250
                3 = 100 Ohm Platinum / 500
                4 = 1000 Ohm Platinum
                5 = NTC RTD
                6 = Thermocouple 25 mV
                7 = Thermocouple 50 mV
                8 = 2.5 V, 1 mA
                9 = 7.5 V, 1 mA
        
        < compensation : int : 0, 1 >
            Specifies input compensation:
                0 = off, 1 = on
        """
        self.com.send('INTYPE %s, %d, %d'%(ch, sensor_type, compensation))
        return

    def input_type_query(self, ch):
        """
        INTYPE? : Query Input Type Parameters
        -------------------------------------
        Returns input type parameters.

        < ch : str[1] : A,B >
            Specifies input ch to configure.

        Returns:
            sensor_type, compensation
        """
        self.com.send('INTYPE? %s'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        sensor = int(ret[0])
        comp = int(ret[1])
        return sensor, comp

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
        self.com.send('KEYST?')
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def kelvin_reading_query(self, ch='A'):
        """
        KRDG? : Query Kelvin Reading for Single Input
        ---------------------------------------------
        Returns the Kelvin reading for a single input.

        < ch : int : A, B >
            Specifies channel to read (A or B).

        Returns:
            temp : float : K
        """
        self.com.send('KRDG? %s'%(ch))
        ret = self.com.readline()
        ret = float(ret)
        return ret

    def linear_equation_data_query(self, ch='A'):
        """
        LDAT? : Linear Equation Data Query
        ----------------------------------
        Returns linear equation data

        < ch : int : A, B >
            Specifies channel to read (A or B).
        """
        self.com.send('LDAT? %s'%(ch))
        ret = self.com.readline()
        ret = float(ret)
        return ret

    def linear_equation_set(self, ch, eq, m, source, b_source, b):
        """
        LINEAR : Configure Input Linear Equation Parameters
        ---------------------------------------------------
        Configures the linear equation for an input.
        
        < ch : char : A, B >
            Specifies input to configure (A or B).

        < eq : int : 1,2 >
            Specifies inear equation to use:
                1 : y = m * x(source) + b
                2 : y = m * (x(source + b)

        < m : float :  >
            Specifies a value for m in the equation.

        < source : int : 1-3 >
            Specifies input data.
            1 = Kelvin, 2 = Celsius, 3 = sensor units.

        < b_source : int : 1-5 >
            Specifies what to use for 'b' in equation
                1 = a value
                2 = +SP1
                3 = -SP1
                4 = +SP2
                5 = -SP2
        
        < b : float : >
            Specifies a value for 'b' in the equation if <b_source> is 1.
        """
        self.com.send('LINEAR %s, %d, %.3f, %d, %d, %.3f'%(ch, eq, m, source,
                                                           b_source, b))
        return

    def linear_equation_query(self, ch):
        """
        LINEAR? : Query Input Linear Equation Parameters
        ------------------------------------------------
        Returns input linear equation configuration.

        < ch : char : A, B >
            Specifies input to configure (A or B).

        Returns:
            eq, m, source, b_source, b
        """
        self.com.send('LINEAR? %s'%(ch))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        eq = int(ret[0])
        m = float(ret[1])
        source = int(ret[2])
        b_source = int(ret[3])
        b = float(ret[4])
        return eq, m, source, b_source, b

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
        self.com.send('LOCK %d, %d'%(off_on, code))
        return

    def lockout_query(self):
        """
        LOCK? : Query Lock-out and Lock-out Code
        ----------------------------------------
        Returns lock-out status and lock-out code.

        Returns:
            off_on, code
        """
        self.com.send('LOCK?')
        ret = self.com.readline()
        ret = ret.strip().split(',')
        off_on = int(ret[0])
        code = ret[1]
        return off_on, code
    
    def min_max_data_query(self, ch):
        """
        MDAT? : Query Minimum/Maximum Data 
        -----------------------------------
        Returns Min/Max data.

        < ch : char : A, B >
            Specifies input to configure (A or B).
        
        Returns:
            min, max
        """
        self.com.send('MDAT?')
        ret = self.com.readline()
        ret = ret.strip().split(',')
        dmin = float(ret[0])
        dmax = float(ret[1])
        return dmin, dmax
    
    def minmax_set(self, ch, source):
        """
        MNMX : Configure Minimum and Maximum Input Function Parameters
        --------------------------------------------------------------
        Configures the minimum and maximum input functions.

        < ch : char : A, B >
            Specifies input to configure (A or B).

        < source : int : 1-4 >
            Specifies input data to process through max/min.
            1 = Kelvin, 2 = Celsius, 3 = sensor units, 4 = linear data.
        """
        self.com.send('MNMX %s, %d'%(ch, source))
        return

    def minmax_query(self, ch):
        """
        MNMX? : Query Minimum and Maximum Input Function Parameters
        -----------------------------------------------------------
        Returns an input min/max configuration.

        < ch : char : A, B >
            Specifies input to configure (A or B).

        Returns:
            source
        """
        self.com.send('MNMX? %s'%(ch))
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def minmax_function_reset(self):
        """
        MNMXRST : Resets Min/Max Function for All Inputs
        ------------------------------------------------
        Resets the minimum and maximum data for all inputs.
        """
        self.com.send('MNMXRST')
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
        self.com.send('MODE %d'%(mode))
        return

    def local_remote_mode_query(self):
        """
        MODE? : Query Remote Interface Mode
        -----------------------------------
        Returns the remote interface mode.

        Returns:
            mode
        """
        self.com.send('MODE?')
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def control_loop_manual_heater_power_output_command(self, loop, value):
        """
        MOUT : Manual Heater Power Output Command
        -----------------------------------------
        Configures the manual heater power output

        < loop : int : 1,2 >
            specifies loop to configure (1 or 2).
        
        < value : float : >
            specifies value for manual output (%)
        """
        self.com.send('MOUT %d, %f'%(loop, value))
        return

    def control_loop_manual_heater_power_output_query(self, loop):
        """
        MOUT? : Manual Heater Power Output Query
        -----------------------------------------
        Returns the manual heater power output

        < loop : int : 1,2 >
            specifies loop to configure (1 or 2).
        
        Returns:
            value : heater output (%)
        """
        self.com.send('MOUT? %d'%(loop))
        ret = self.com.readline()
        ret = float(ret)
        return ret

    def control_loop_pid_command(self, loop, p, i, d):
        """
        PID : Control Loop PID Values Command
        -------------------------------------
        Configures the PID values for control loop.

        < loop : int : 1,2 >
            specifies loop to configure (1 or 2).
        
        < p : float : >
            The value for control loop Proportional (gain)
            range : 0.1 -- 1000

        < i : float : >
            The value for control loop Integral (reset)
            range : 0.1 -- 1000

        < d : float : >
            The value for control loop Derivative (rate)
            range : 0 -- 200
        """
        self.com.send('PID %d, %f, %f, %f'%(loop, p, i, d))
        return

    def control_loop_pid_query(self, loop):
        """
        PID? : Control Loop PID Values Query
        -------------------------------------
        Returns the PID values for control loop.
        
        < loop : int : 1,2 >
            specifies loop to configure (1 or 2).
        
        Returns:
            p, i, d
        """
        self.com.send('PID? %d'%(loop))        
        ret = self.com.readline()
        ret = ret.strip().split(',')
        p = float(ret[0])
        i = float(ret[1])
        d = float(ret[2])
        return p, i, d

    def control_setpoint_ramp_parameter_command(self, loop, off_on, rate):
        """
        RAMP : Control Setpoint Ramp Parameter Command
        ----------------------------------------------
        Configures the ramp parameter.

        < loop : int : 1,2 >
            specifies loop to configure (1 or 2).
        
        < off_on : int : 0, 1 >
            Specifies whether ramping is 0 = Off, 1 = On.

        < rate : float : >
            Specifies setpoint ramp rate in Kelvin/minute.
            range : 0.1 -- 100
        """
        self.com.send('RAMP %d, %d, %f'%(loop, off_on, rate))
        return

    def control_setpoint_ramp_parameter_query(self, loop):
        """
        RAMP? : Control Setpoint Ramp Parameter Query
        ----------------------------------------------
        Returns the ramp parameter.

        < loop : int : 1,2 >
            specifies loop to configure (1 or 2).
        
        Returns:
            off_on, rate
        """
        self.com.send('RAMP? %d'%(loop))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        off_on = int(ret[0])
        rate = float(ret[1])
        return off_on, rate

    def control_setpoint_ramp_status_query(self, loop):
        """
        RAMPST? : Control Setpoint Ramp Status Query
        ----------------------------------------------
        Returns the ramp status.

        < loop : int : 1,2 >
            specifies loop to configure (1 or 2).
        
        Returns:
            status : int : 0 = Not ramping, 1 = Setpoint is ramping
        """
        self.com.send('RAMPST? %d'%(loop))
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def heater_range_command(self, range_):
        """
        RANGE : Heater Range Command
        ----------------------------
        Configures heater range.

        < range_ : int : 0-3 >
            0 = Off
            1 = Low (0.5 W)
            2 = Medium (5 W)
            3 = High (50 W)
        """
        self.com.send('RANGE %d'%(range_))
        return

    def heater_range_query(self):
        """
        RANGE? : Heater Range Query
        ----------------------------
        Returns heater range.
        
        Returns:
            range
        """
        self.com.send('RANGE?')
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def reading_status_query(self, ch):
        """
        RDGST? : Query Input Status
        ---------------------------
        The integer returned represents the sum of the bit weighting of the
        input status flag bits.

        < ch : int : A, B >
            specifies which input to query.

        Returns:
            status
        """
        self.com.send('RDGST? %s'%(ch))
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def relay_set(self, relay_number, mode, input_alarm, alarm_type):
        """
        RELAY : Configure Relay Control Parameters
        ------------------------------------------
        Configures relay control.

        < relay_number : int : 1, 2 >
            Specifies which relay to configure (1 or 2).

        < mode : int : 0-2 >
            Specifies relay mode. 0 = Off, 1 = On, 2 = Alarms

        < input_alarm : char : A, B >
            Specifies which input alarm activates the relay when the relay
            is in alarm mode (A or B).

        < alarm_type : int : 0-2 >
            Specifies the input alarm type that activates the relay when the
            relay is in alarm mode.
            0 = Low alarm, 1 = High Alarm, 2 = Both Alarms.
        """
        self.com.send('RELAY %d, %d, %s, %d'%(relay_number, mode,
                                              input_alarm, alarm_type))
        return

    def relay_query(self, relay_number):
        """
        RELAY? : Query Relay Control Parameters
        ---------------------------------------
        The integer returned represents the sum of the bit weighting of the
        relay status.

        < relay_number : int : 1, 2 >
            Specifies which relay to configure (1-8).

        Returns:
            mode, input_alarm, alarm_type
        """
        self.com.send('RELAY? %d'%(relay_number))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        mode = int(ret[0])
        input_alarm = ret[1]
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
        self.com.send('RELAYST?')
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def softcal_curve_generate(self, std, dest, SN, T1, U1, T2, U2, T3, U3):
        """
        SCAL : Generate SoftCal Curve
        -----------------------------

        < std : int : 1,6,7 >
        < dest : int : 21-41 >
        < SN : str[10] :  >
        < T1 : float : >
        < U1 : float : >
        < T2 : float : >
        < U2 : float : >
        < T3 : float : >
        < U3 : float : >
        """
        self.com.send('SCAL %d, %d, %s, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f'%
                      (std, dest, SN, T1, U1, T2, U2, T3, U3))
        return

    def control_setpoint_command(self, loop, value):
        """
        SETP : Control Setpoint Command
        -------------------------------
        Configures setpoint.
        
        < loop : int : 1,2 >
            Specifies which loop to configure (1 or 2).
        
        < value : float :  >
            The value for the setpoint.
        """
        self.com.send('SETP %d, %f'%(loop, value))
        return

    def control_setpoint_query(self, loop):
        """
        SETP? : Control Setpoint Query
        ------------------------------
        Returns setpoint.
        
        < loop : int : 1,2 >
            Specifies which loop to configure (1 or 2).
        
        Returns:
            value: The value of the setpoint.
        """
        self.com.send('SETP? %d'%(loop))
        ret = self.com.readline()
        ret = float(ret)
        return ret

    def sensor_units_reading_query(self, ch=0):
        """
        SRDG? : Query Sensor Units Reading for Single Input or All Inputs
        -----------------------------------------------------------------
        Returns the Sensor Units reading for a single input or all inputs.

        < ch : char : A, B >
            Channel to be read (A or B).
        """
        self.com.send('SRDG? %s'%(ch))
        ret = self.com.readline()
        ret = float(ret)
        return ret

    def thermocouple_junction_temperature_query(self):
        """
        TEMP? : Thermocouple Junction Temperature Query
        -----------------------------------------------
        Returns temperature

        Returns:
            junction_temperatuer (K)
        """
        self.com.send('TEMP?')
        ret = self.com.readline()
        ret = float(ret)
        return ret

    def control_tuning_status_query(self):
        """
        TUNEST? : Control Tuning Status Query
        -------------------------------------
        Returns tuning status

        Returns:
            status : 0 = no active tuning, 1 = active tuning
        """
        self.com.send('TUNEST?')
        ret = self.com.readline()
        ret = int(ret)
        return ret

    def control_loop_zone_table_parameter_command(self, loop, zone, top,
                                                  p, i, d, mout, range_):
        """
        ZONE : Control Loop Zone Table Parameter Command
        -------------------------------------------------
        Configures loop zone table
        
        < loop : int : 1,2 >
            Specifies which loop to configute (1 or 2).

        < zone : int : 1-10 >
            Specifies which zone in the table to configure (1-10).
        
        < top : float : >
            Specifies the top temperature of this zone.
        
        < p : value : >
            Specifies the P for the zone (0.1-1000).
        
        < i : value : >
            Specifies the I for the zone (0.1-1000).
        
        < d : value : >
            Specifies the D for the zone (0-200).
        
        < mout : float : >
            Specifies the manual output for this zone (0-100%).
        
        < range_ : int : 0-3 >
            Specifies the heater range for this zone if <loop> = 1 (0-3).
        """
        self.com.send('ZONE %d, %d, %f, %f, %f, %f, %f, %d'%(loop, zone, top,
                                                             p, i, d, mout,
                                                             range_))
        return

    def control_loop_zone_table_parameter_query(self, loop, zone):
        """
        ZONE? : Control Loop Zone Table Parameter Query
        -----------------------------------------------
        Returns Loop zone parameters
        
        < loop : int : 1,2 >
            Specifies which loop to query (1 or 2).

        < zone : int : 1-10 >
            Specifies which zone in the table to query (1-10).
        
        Returns:
            top, p, i, d, mout, range_
        """
        self.com.send('ZONE? %d, %d'%(loop, zone))
        ret = self.com.readline()
        ret = ret.strip().split(',')
        top = float(ret[0])
        p = float(ret[1])
        i = float(ret[2])
        d = float(ret[3])
        mout = float(ret[4])
        range_ = int(ret[5])
        return top, p, i, d, mout, range_
        
    def control_loop_zone_table_parameter_query_all(self, printlog=True):
        """
        ZONE? : Control Loop Zone Table Parameter Query All
        ---------------------------------------------------
        
        Returns:
            top, p, i, d, mout, range_
        """
        items1 = []
        items2 = []
        zones = range(1, 11)

        for z in zones:
            items1.append(self.control_loop_zone_table_parameter_query(1, z))
            items2.append(self.control_loop_zone_table_parameter_query(2, z))
            continue

        if printlog:
            print('ZONE?')
            print('-----')
            print(':loop1:')
            print('zone : top  , P    , I    , D    , out  , range')
            for i, item in enumerate(items1):
                print('%4d : %5.2f, %5.2f, %5.2f, %5.2f, %5.2f, %d'%(i+1, item[0], item[1],
                                                           item[2], item[3],
                                                           item[4], item[5]))
                continue
            print('')
            print(':loop2:')
            print('zone : top  , P    , I    , D    , out  , range')
            for i, item in enumerate(items2):
                print('%4d : %5.2f, %5.2f, %5.2f, %5.2f, %5.2f, %d'%(i+1, item[0], item[1],
                                                           item[2], item[3],
                                                           item[4], item[5]))
                continue
            print('')
            pass
        return items1, items2
        
    _shortcut_command = {'ALARM': 'alarm_set',
                         'ALARMQ': 'alarm_query',
                         'ALARMSTQ': 'alarm_status_query',
                         'ALMRST': 'alarm_reset',
                         'ANALOG': 'analog_outputs_set',
                         'ANALOGQ': 'analog_outputs_query',
                         'AOUTQ': 'analog_output_data_query',
                         'BAUD': 'serial_interface_baud_rate_set',
                         'BAUDQ': 'serial_interface_baud_rate_query',
                         'BEEP': 'alarm_beeper_command',
                         'BEEPQ': 'alarm_beeper_query',
                         'BRIGT': 'display_brightness_command',
                         'BRIGTQ': 'display_brightness_query',
                         'CMODE': 'control_loop_mode_command',
                         'CMODQ': 'control_loop_mode_query',
                         'CRDGQ': 'celsius_reading_query',
                         'CRVDEL': 'curve_delete',
                         'CRVHDR': 'curve_header_set',
                         'CRVHDRQ': 'curve_header_query',
                         'CRVPT': 'curve_point_set',
                         'CRVPTQ': 'curve_point_query',
                         'CSET': 'control_loop_parameter_command',
                         'CSETQ': 'control_loop_parameter_query',
                         'DFLT': 'factory_defaults_reset',
                         'DISPFLD': 'display_field_set',
                         'DISPFLDQ': 'display_field_query',
                         'FILTER': 'filter_set',
                         'FILTERQ': 'filter_query',
                         'HTRQ': 'heater_output_query',
                         'HTRSTQ': 'heater_status_query',
                         'IEEE': 'ieee488_set',
                         'IEEEQ': 'ieee488_query',
                         'INCRV': 'input_curve_set',
                         'INCRVQ': 'input_curve_query',
                         'INTYPE': 'input_type_set',
                         'INTYPEQ': 'input_type_query',
                         'KEYSTQ': 'keypad_status_query',
                         'KRDGQ': 'kelvin_reading_query',
                         'LDATQ': 'linear_equation_data_query',
                         'LINEAR': 'linear_equation_set',
                         'LINEARQ': 'linear_equation_query',
                         'LOCK': 'lockout_set',
                         'LOCKQ': 'lockout_query',
                         'MDATQ': 'min_max_data_query',
                         'MNMX': 'minmax_set',
                         'MNMXQ': 'minmax_query',
                         'MNMXRST': 'minmax_function_reset',
                         'MODE': 'local_remote_mode_set',
                         'MODEQ': 'local_remote_mode_query',
                         'MOUT': 'control_loop_manual_heater_power_output_command',
                         'MOUTQ': 'control_loop_manual_heater_power_output_query',
                         'PID': 'control_loop_pid_command',
                         'PIDQ': 'control_loop_pid_query',
                         'RAMP': 'control_setpoint_ramp_parameter_command',
                         'RAMPQ': 'control_setpoint_ramp_parameter_query',
                         'RAMPSTQ': 'control_setpoint_ramp_status_query',
                         'RANGE': 'heater_range_command',
                         'RANGEQ': 'heater_range_query',
                         'RDGSTQ': 'reading_status_query',
                         'RELAY': 'relay_set',
                         'RELAYQ': 'relay_query',
                         'RELAYSTQ': 'relay_status_query',
                         'SCAL': 'softcal_curve_generate',
                         'SETP': 'control_setpoint_command',
                         'SETPQ': 'control_setpoint_query',
                         'SRDGQ': 'sensor_units_reading_query',
                         'TEMPQ': 'thermocouple_junction_temperature_query',
                         'TUNESTQ': 'control_tuning_status_query',
                         'ZONE': 'control_loop_zone_table_parameter_command',
                         'ZONEQ': 'control_loop_zone_table_parameter_query',}
