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

    def __init__(self, **kwargs):
        self._args = {}
        self._plugins = {}
        for key, value in kwargs.items():
            if key == 'args':
                self._args = value
            elif key == "plugins":
                self._plugins = value

    def __setattr__(self, key, value):
        if key == "_args" or key == "_plugins":
            object.__setattr__(self, key, value)
        else:
            self._args[key] = value

    def __getattr__(self, name):
        try:
            value = self._args[name]
        except KeyError:
            value = object.__getattribute__(self, name)

        return value

    def itens(self):
        return self._args.items()

    def plugins(self):
        return self._plugins.items()

    def as_list(self):
        return str(self).split(' ')

    def __repr__(self):
        return ''.join([('/%s:%s ' % (key, value)) for key, value in self._args.items()])
