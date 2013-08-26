'''
Created on 20/08/2013

@author: tiago
'''

from PyQt4 import QtGui
class MainWindow(QtGui.QWidget):    
    '''
    PyRdp Main Window
    '''
    
    _tabs = None
    
    def __init__(self, width, height):
        '''
        Constructor
        '''        
        super().__init__()
        self.resize(width, height);
        self.setWindowTitle('PyRdp')        
        self.move_center()
        self.setFixedSize(self.size())        
        self._tabs = QtGui.QTabWidget(self) 
        self._tabs.resize(width, height)       

    def move_center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def add_tab(self, rdp_conn):
        tab = ConnectionTab(rdp_conn, self._tabs.width(), self._tabs.height())
        self._tabs.addTab(tab, tab.name)
        tab.open_connection()
    
    def close_all(self):
        for tab_index in range(self._tabs.count()):
            tab = self._tabs.widget(tab_index)
            tab.close_connection()
    
    
        
    
        
class ConnectionTab(QtGui.QWidget):
    
    _conn = None
    
    def __init__(self, conn, width, height):
        super().__init__()
        
        if conn is None:
            raise ValueError("Connection can't be None")
        
        self._conn = conn;
        self.resize(width, height)
        self._conn.cfg.size = ('%dx%d' % (self.width() - 10, self.height() - 25))
        
    @property
    def name(self):
        return self._conn.cfg.v
        
    def open_connection(self):
        self._conn.connect(self.winId())
    
    def close_connection(self):
        self._conn.close()
        
        
    
    
    

        