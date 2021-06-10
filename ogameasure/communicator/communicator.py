class communicator(object):
    method = 'communicator_base_class'
    connection = False
    
    terminator = '\n'
    
    def __init__(self, *args):
        if len(args)!=0:
            self.open(*args)
            pass
        pass
    
    def set_terminator(self, term_char):
        self.terminator = term_char
        return
        
    def open(self, *args):
        pass
    
    def close(self):
        pass
    
    def send(self, msg):
        pass
    
    def recv(self, byte):
        pass
        
    def readline(self):
        pass


