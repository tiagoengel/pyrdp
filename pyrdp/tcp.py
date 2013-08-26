'''
Created on 25/08/2013

@author: tiago
'''

from PyQt4 import QtGui
from pyrdp.rdp import Settings, RdpConnection
from pyrdp.ui import MainWindow
import socketserver
import sys
import threading

class AppWindow(threading.Thread):
    
    _app = None
    _main_window = None
    _server = None
    
    def __init__(self, server):
        threading.Thread.__init__(self)
        self._server = server
    
    def run(self):
        self._app = QtGui.QApplication(sys.argv)
        screen_rect = self._app.desktop().screenGeometry()
        width, height = screen_rect.width(), screen_rect.height()
        
        self._main_window = MainWindow(width * 0.95, height * 0.90)
        self._main_window.show()
        
        self._app.exec_()
        
    def connect(self, conn_name):
        cfg = Settings()
        cfg.u = 'tiago.h'
        cfg.p = 'tiagost1'    
        cfg.v = 'intersys.com.br'
         
        conn = RdpConnection(cfg)             
        self._main_window.add_tab(conn)

class PyRdpServer(socketserver.BaseRequestHandler):        
            
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print('Connecting to %s...' % self.data)
        APP.connect(self.data)
                        
if __name__ == "__main__":
        
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), PyRdpServer)
    
    APP = AppWindow(server) 
    APP.start()           
    

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever() 
            
       
        