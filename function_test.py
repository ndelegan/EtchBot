import signatone_driver as Signatone_Driver
import functions as Functions
import unittest
from io import StringIO
from contextlib import redirect_stdout


class Function_Test(unittest.TestCase):
    def testingImageCapturing(self):
        filename= ""
        image = Signatone_Driver.Signatone.save_image(Functions.take_image(1,filename))
        print(image.shape)
        self.assertEqual(image.shape, ())




if __name__ == "__main__":
    unittest.main()