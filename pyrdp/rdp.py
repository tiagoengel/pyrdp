from subprocess import Popen


class RdpConnection(object):
    
    _cfg = None
    _conn = None
    
    def __init__(self, cfg):
        self._cfg = cfg
    
    def connect(self, parent_window=None): 
        cmd = str(self._cfg)               
        if not parent_window is None:
            cmd += ' /parent-window:%d' % parent_window
        
        cmd = 'xfreerdp ' + cmd   
        self._conn = Popen(cmd, shell=True)
    
    def close(self):
        self._conn.terminate()
        
    @property    
    def cfg(self):
        return self._cfg
                

class Settings(object):
      
    _args = None  
      
    def __init__(self):
        self._args = {}

    def __init__(self, args):
        self._args = args

    def __setattr__(self, name, value):
        if name == '_args':
            object.__setattr__(self, name, value)
        else:            
            self._args[name] = value
            
    def __getattr__(self, attr):
        return self._args[attr]

    def itens(self):
        return self._args.items()

    def __repr__(self):
        return ''.join([('/%s:%s ' % (key, value)) for key, value in self._args.items()])      
