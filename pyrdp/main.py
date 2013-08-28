"""
Created on 20/08/2013

@author: tiago
"""


from pyrdp.ui import QtSingleApplication, MainWindow
import sys

APP_ID = "1faaffb1-cd45-485d-948b-c101fd793a92"

def usage():
    hlp = """Usage:
    pyrp [connection name]"""
    print(hlp)

if __name__ == '__main__':


    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    msg = 'open:' + sys.argv[1]

    app = QtSingleApplication(APP_ID, sys.argv)
    
    if app.is_running():
        app.send_message(msg)
        sys.exit(0)
    
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    
    main_window = MainWindow(width * 0.95, height * 0.90)
    main_window.handle_message(msg)
    main_window.show()

    app.set_activation_window(main_window)

    sys.exit(app.exec_())
    