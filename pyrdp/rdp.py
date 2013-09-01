from PyQt4.QtCore import QProcess


class RdpConnection(object):
    
    _cfg = None
    _conn = None
    
    def __init__(self, cfg):
        self._cfg = cfg
    
    def connect(self, parent_window=None):
        if not parent_window is None:
            setattr(self._cfg, 'parent-window', parent_window)

        self._conn = QProcess()
        # print(self._cfg.as_list())
        self._conn.start('xfreerdp', self._cfg.as_list())
        self._conn.readyReadStandardOutput.connect(self._read_out)
        self._conn.readyReadStandardError.connect(self._read_err)
    
    def close(self):
        self._conn.close()
        self._conn.terminate()

    def connect_output(self, out_listener):
        self._out_listener = out_listener

    def _read_out(self):
        if not self._out_listener is None:
            self._out_listener(str(self._conn.readAllStandardOutput()))

    def _read_err(self):
        if not self._out_listener is None:
            self._out_listener(str(self._conn.readAllStandardError()))
        
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

    def as_list(self):
        return str(self).split(' ')

    def __repr__(self):
        return ''.join([('/%s:%s ' % (key, value)) for key, value in self._args.items()])      
