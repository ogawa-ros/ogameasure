#! /usr/bin/env python

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

