import  os
import configparser
from pyrdp.rdp import Settings

PATH = os.path.expanduser(os.environ['HOME'])
PATH = os.path.join(PATH, '.pyrdp')

if not os.path.exists(PATH):
    os.mkdir(PATH)


class ConnectionFile(object):

    def __init__(self, conn_name):
        self._file_name = os.path.join(PATH, conn_name)

    def file_exists(self):
        return os.path.exists(self._file_name)

    def write(self, cfg):
        file = open(self._file_name, 'w')
        print("[settings]", file=file)
        for key, value in cfg.itens():
            print(("%s=%s" % (key, value)), file=file)

        print("[plugins]", file=file)
        for key, value in cfg.plugins():
            print(("%s=%s" % (key, value)), file=file)

        file.close()

    def read(self):
        conf = configparser.ConfigParser()
        conf.read(self._file_name, 'UTF-8')
        vars = dict(conf.items('settings'))
        return Settings(args=vars)
