"""
Created on 20/08/2013

@author: tiago
"""

from pyrdp.ui import QtSingleApplication, MainWindow
import sys

if __name__ == '__main__':
    
    app_id = 'pyrdp1'
    app = QtSingleApplication(app_id, sys.argv)
    
    if app.isRunning():
        app.sendMessage('open:connName')
        sys.exit(0)
    
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    
    main_window = MainWindow(width * 0.95, height * 0.90)
    main_window.handle_message("teste")
    main_window.show()
    
    app.setActivationWindow(main_window)
    
    sys.exit(app.exec_())
    