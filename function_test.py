import os.path

import signatone_driver as Signatone_Driver
import functions as Functions
import unittest
from io import StringIO
from contextlib import redirect_stdout
import os

class Function_Test(unittest.TestCase):
    
    # def testingImageCapturing(self):
    #     signatone = Signatone_Driver.Signatone()
    #     filename = ""
    #     for i in range(11):
    #         image = Functions.take_image(i,filename)
    #         signatone.save_image(image)
    #     print(i)
    #     self.assertEqual(os.path.exists(f"C:\\CM400\\photos\\imgCapture{i}.bmp"),True)
    def testingImagDeletion(self):
        signatone = Signatone_Driver.Signatone()
        filename = ""
        for i in range(11):
            image = Functions.take_image(i,filename)
            signatone.save_image(image)
        print(i)
        Functions.delete_image(i)
        self.assertEqual(os.path.exists("C:\\CM400\\photos\\imgCapture0.bmp"),False)
    def testingImageDeletion(self):
        counter = 9
        Functions.delete_image(counter)
        self.assertEqual(os.path.exists("C:\\CM400\\photos\\imgCapture0.bmp"), False)


if __name__ == "__main__":
    unittest.main()