import siglent_driver as Siglent_Driver
import unittest

class SiglentTest(unittest.TestCase):
	def testingoutput(self):
		device = Siglent_Driver.Siglent()
		set_voltage = device.set_volt(1)
		check = device.get_output()
		self.assertEqual(check,set_voltage)
		device.output_off()
	def testingonnoff(self):
		device = Siglent_Driver.Siglent()
		device.output_on()
		device.set_volt(1)
		device.output_off()
		check = device.get_output()
		self.assertEqual(0,check)
if __name__ == "__main__":
	unittest.main()
