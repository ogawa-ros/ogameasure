#! /usr/bin/env python

class device(object):
    manufacturer = ''
    product_name = ''
    classification = ''
    
    com = None
    _shortcut_command = {}
    
    def __init__(self, com):
        self.com = com
        self.com.open()
        self._add_shortcut_command()
        pass

    def _add_shortcut_command(self):
        items = self._shortcut_command.items()
        for shortcut, method in items:
            self.__setattr__(shortcut,
                             self.__getattribute__(method))
            continue
        return
