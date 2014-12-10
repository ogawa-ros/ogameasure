#! /usr/bin/env python

class device(object):
    manufacturer = ''
    product_name = ''
    classification = ''
    
    com = None
    
    def __init__(self, com):
        self.com = com
        self.com.open()
        pass
