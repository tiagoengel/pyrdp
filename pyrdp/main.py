'''
Created on 20/08/2013

@author: tiago
'''
from PyQt4 import QtGui
from pyrdp.rdp import Settings, RdpConnection
from pyrdp.ui import MainWindow
import socket
import sys

if __name__ == '__main__':
#     app = QtGui.QApplication(sys.argv)
#     screen_rect = app.desktop().screenGeometry()
#     width, height = screen_rect.width(), screen_rect.height()
#     
#     main_window = MainWindow(width * 0.95, height * 0.90)
#     main_window.show()
#     
#     sett = Settings()
#     sett.u = 'tiago.h'
#     sett.p = 'tiagost1'    
#     sett.v = 'intersys.com.br'
#     
#     conn = RdpConnection(sett)
#         
#     main_window.add_tab(conn)
#     
#     app.exec_()
#     
#     main_window.close_all()
    HOST, PORT = "localhost", 9999
    data = " ".join(sys.argv[1:])
    
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes('intersys.com.br', 'UTF-8'))
            
    finally:
        sock.close()