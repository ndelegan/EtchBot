import siglent_driver as Siglent_Driver
import unittest

class SiglentTest(unittest.TestCase):
	def testingoutput(self):
		device = Siglent_Driver.Siglent()
		setCurrent = device.set_curr(1)
		setVoltage = device.set_volt(1)
		check =device.getoutput()
		self.assert(check,set)
	def testingonnoff(self):
		device = Siglent_Driver.Siglent()
		on = device.output_on()
		setvolt=device.set_volt(1)
		off = device.output_off()
		check=device.get_output()
		self.assert(0,check)
