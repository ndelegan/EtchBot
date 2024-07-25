import signatone_driver as Signatone_Driver
import unittest
from io import StringIO
from contextlib import redirect_stdout
#To-Do - make it to be able to test different devices
#and make it user-friendly :) print if the tests were successfully
class SignatoneTest(unittest.TestCase):
    def setUp(self):
        self.my_string = 'Device name'
    def testingConnection(self):
        #using redirect_stdout to capture print statements from init function in the Signatone Driver class
        with StringIO() as buffer, redirect_stdout(buffer):
            device = Signatone_Driver.Signatone()
            output = buffer.getvalue().strip()
        #test is looking inside the print statements from the init function to match string variable
        string = 'Signatone CM400 MTS,SERIAL 22080139,VER 1.5.5'
        #Should print OK
        #i.e. self.assertIn(self.my_string,output)
        self.assertIn(string,output)
        print("device connection was successful")
    def testingSetDevice1(self):
        #initiziling driver class
        device = Signatone_Driver.Signatone()
        #setting device and checking if the set device is the same
        device.set_device("CAP1")
        check_device = device.get_device()
        #Should print ok
        self.assertEqual("CAP1",check_device)
    def testingSetDevice4(self):
        #initiziling driver class
        device = Signatone_Driver.Signatone()
        #setting device and checking if the set device is the same
        device.set_device("CAP4")
        check_device = device.get_device()
        #Should print ok
        self.assertEqual("CAP4",check_device)
    def testingSetDeviceW(self):
        #initiziling driver class
        device = Signatone_Driver.Signatone()
        #setting device and checking if the set device is the same
        device.set_device("WAFER")
        check_device = device.get_device()
        #Should print ok
        self.assertEqual("WAFER",check_device)
    #TO_DO: test other devices
    
if __name__ == "__main__":
    unittest.main()