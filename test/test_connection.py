'''
Created on 10/08/2013

@author: tiago
'''
import unittest


class Test(unittest.TestCase):


    def testConnection(self):
        from pyrdp import RdpConnection, Settings
        
        conn = RdpConnection()
        #cfg = Settings(host='intersys.com.br', user='tiago.h', passwd='tiagost1');
        
        conn.connect()
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConnection']
    unittest.main()