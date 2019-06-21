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

    def help(self):
        method_list = []
        doc_list = []
        for method in dir(self):
            if method[0]=='_': continue
            if method in self._shortcut_command.keys(): continue
            mt = self.__getattribute__(method)
            if type(mt) in [type(None), int, float, str]: continue
            if mt.__doc__ is None: continue            
            method_help = self.__getattribute__(method).__doc__
            short_help = method_help.split('\n')[1].strip()
            method_list.append(method)
            doc_list.append(short_help)
            continue
        
        length = max(len(m) for m in method_list)
        hlength = max(len(d) for d in doc_list)
        help_fmt = '%-' + '%d'%(length+1) + 's : %s\n'
        separation = '-'*length + '- : ' + '-'*hlength + '\n'
        
        help_str = ''
        help_str += separation
        help_str += help_fmt%('method name', 'description')
        for i in range(len(method_list)):
            if i%20==0: help_str += separation
            help_str += help_fmt%(method_list[i], doc_list[i])
            continue
        help_str += separation
        print(help_str)
        return
