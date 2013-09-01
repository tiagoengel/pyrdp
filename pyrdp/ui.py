"""
Created on 20/08/2013

@author: tiago
"""

from PyQt4 import QtCore, QtGui, QtNetwork, Qt
from PyQt4.QtCore import pyqtSignal
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
        self.setWindowIcon(QtGui.QIcon('../pyrdp.ico'))
        self.move_center()
        self.setFixedSize(self.size())        
        self._tabs = QtGui.QTabWidget(self)
        self._tabs.setTabsClosable(True)
        self.connect(self._tabs, QtCore.SIGNAL("tabCloseRequested(int)"), self.close)
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

    def close(self, index):
        tab = self._tabs.widget(index)
        tab.close_connection()
        self._tabs.removeTab(index)
    
    def close_all(self):
        for tab_index in range(self._tabs.count()):
            self.close(tab_index)
    
    def handle_message(self, msg):
        cmd, arg = msg.split(':')
        if cmd == 'open':
            self.open_connection(arg)

    def open_connection(self, conn_name):
        conn_file = file.ConnectionFile(conn_name)

        if not conn_file.file_exists():
            self._conn_form = ConnectionDialog(conn_name)
            self._conn_form.exec_()

        cfg = conn_file.read()
        self.add_tab(rdp.RdpConnection(cfg))

    def closeEvent(self, event):
        self.close_all()
        super(MainWindow, self).closeEvent(event)


class ConnectionDialog(QtGui.QDialog):

    def __init__(self, conn_name):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle('New Connection - ' + conn_name)

        self._fields = []
        self._conn_name = conn_name

        mainLayout = QtGui.QVBoxLayout()

        self._form_layout = QtGui.QFormLayout()

        self.add_field('Host:', Field.Type.TEXT, 'v')
        self.add_field('User:', Field.Type.TEXT, 'u')
        self.add_field('Password:', Field.Type.PASSWORD, 'p')

        mainLayout.addLayout(self._form_layout)

        self.create_save_button(mainLayout)
        self.setLayout(mainLayout)

        self.resize(300, 150)
        self.setFixedSize(self.size())

    def add_field(self, label, type, name):
        field = Field(label, type, name)
        self._fields.append(field)
        self._form_layout.addRow(field.lb, field.field)

    def save(self):
        cfg = {}
        for field in self._fields:
            cfg[field.name] = field.field.text()

        conn_file = file.ConnectionFile(self._conn_name)
        conn_file.write(rdp.Settings(cfg))

        self.close()

    def create_save_button(self, mainLayout):
        layout = QtGui.QHBoxLayout()
        button = QtGui.QPushButton("Save")
        button.setMaximumSize(QtCore.QSize(60, 30))
        self.connect(button, QtCore.SIGNAL("clicked()"), self.save)
        layout.setAlignment(QtCore.Qt.AlignRight)
        layout.addWidget(button)
        mainLayout.addLayout(layout)


class Field(object):

    class Type(object):
        TEXT = 0
        PASSWORD = 1

    def __init__(self, label, type, name):
        self.lb = QtGui.QLabel(label)
        self.field = QtGui.QLineEdit()
        if type == Field.Type.PASSWORD:
            self.field.setEchoMode(QtGui.QLineEdit.Password)

        self.name = name


class ConnectionTab(QtGui.QFrame):
    
    _conn = None
    
    def __init__(self, conn, width, height):
        super().__init__()
        
        if conn is None:
            raise ValueError("Connection can't be None")
        
        self._conn = conn
        self.resize(width, height)
        self._conn.cfg.size = ('%dx%d' % (self.width() - 10, self.height() - 25))

        self._log = QtGui.QTextEdit(self)

        log_w = self.width() * 0.80
        log_h = self.height() * 0.80

        log_left = (self.width() - log_w) / 2
        log_top = (self.height() - log_h) / 2

        self._log.setGeometry(QtCore.QRect(log_left, log_top, log_w, log_h))
        p = self._log.palette()
        p.setColor(QtGui.QPalette.Base, QtGui.QColor(0, 0, 0))
        self._log.setPalette(p)
        self._log.setTextColor(QtGui.QColor(255, 255, 255))
        
    @property
    def name(self):
        return self._conn.cfg.v
        
    def open_connection(self):
        self._conn.connect(self.winId())
        self._conn.connect_output(self.print_out)

    def close_connection(self):
        self._conn.close()

    def print_out(self, str):
        self._log.append(str)
        
        
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
        self.activation_window.setWindowState(QtCore.Qt.WindowMaximized)
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
