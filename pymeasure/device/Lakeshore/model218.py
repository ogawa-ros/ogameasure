#! /usr/bin/env python

from .. import device
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
