"""
Created on 20/08/2013

@author: tiago
"""

from PyQt4 import QtCore, QtGui, QtNetwork, Qt
from pyrdp import rdp, file
from uno import unicode


class MainWindow(QtGui.QWidget):
    """
    PyRdp Main Window
    """
    
    _tabs = None
    
    def __init__(self, width, height):
        """
        Constructor
        """
        super().__init__()
        self.resize(width, height)
        self.setWindowTitle('PyRdp')        
        self.move_center()
        self.setFixedSize(self.size())        
        self._tabs = QtGui.QTabWidget(self) 
        self._tabs.resize(width, height)
        self._conn_form = None

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
    
    def handle_message(self, msg):
        cmd, arg = msg.split(':')
        if cmd == 'open':
            self.open_connection(arg)

    def open_connection(self, conn_name):
        conn_file = file.ConnectionFile(conn_name)

        if not conn_file.file_exists():
            self._conn_form = ConnectionForm()
            self._conn_form.setGeometry(Qt.QRect(100, 100, 400, 200))
            self._conn_form.exec_()

        cfg = conn_file.read()
        self.add_tab(rdp.RdpConnection(cfg))


class ConnectionForm(QtGui.QDialog):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle('Connection Form')
    

class ConnectionTab(QtGui.QWidget):
    
    _conn = None
    
    def __init__(self, conn, width, height):
        super().__init__()
        
        if conn is None:
            raise ValueError("Connection can't be None")
        
        self._conn = conn
        self.resize(width, height)
        self._conn.cfg.size = ('%dx%d' % (self.width() - 10, self.height() - 25))
        
    @property
    def name(self):
        return self._conn.cfg.v
        
    def open_connection(self):
        self._conn.connect(self.winId())
    
    def close_connection(self):
        self._conn.close()
        
        
class QtSingleApplication(QtGui.QApplication):

    messageReceived = QtCore.pyqtSignal(unicode)

    def __init__(self, appid, *argv):

        super(QtSingleApplication, self).__init__(*argv)
        self._id = appid
        self._activation_window = None
        self._activateOnMessage = False

        self._outSocket = QtNetwork.QLocalSocket()
        self._outSocket.connectToServer(self._id)
        self._isRunning = self._outSocket.waitForConnected()

        if self._isRunning:
            self._outStream = QtCore.QTextStream(self._outSocket)
            self._outStream.setCodec('UTF-8')
        else:
            self._outSocket = None
            self._outStream = None
            self._inSocket = None
            self._inStream = None
            self._server = QtNetwork.QLocalServer()
            self._server.listen(self._id)
            self._server.newConnection.connect(self._on_new_connection)

    def is_running(self):
        return self._isRunning

    def id(self):
        return self._id

    @property
    def activation_window(self):
        return self._activation_window

    def set_activation_window(self, activationWindow, activateOnMessage=True):
        self._activation_window = activationWindow
        self._activateOnMessage = activateOnMessage
        self.messageReceived.connect(self.activation_window.handle_message)

    def activate_window(self):
        if not self.activation_window:
            return
#         self._activationWindow.setWindowState(
#             self._activationWindow.windowState() & Qt.WindowMinimized)
        self.activation_window.raise_()
        self.activation_window.activateWindow()

    def send_message(self, msg):
        if not self._outStream:
            return False
        self._outStream << msg << '\n'
        self._outStream.flush()
        
        return self._outSocket.waitForBytesWritten()

    def _on_new_connection(self):
        if self._inSocket:
            self._inSocket.readyRead.disconnect(self._on_ready_read)
        self._inSocket = self._server.nextPendingConnection()
        if not self._inSocket:
            return
        self._inStream = QtCore.QTextStream(self._inSocket)
        self._inStream.setCodec('UTF-8')
        self._inSocket.readyRead.connect(self._on_ready_read)
        if self._activateOnMessage:
            self.activate_window()

    def _on_ready_read(self):
        while True:
            msg = self._inStream.readLine()
            if not msg:
                break
            self.messageReceived.emit(msg)        
        

