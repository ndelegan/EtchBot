import functions as func
import signatone_driver
import signatone_driver as Signatone
import siglent_driver as Siglent
import time

def main():
    filename = None
    signatone = Signatone.Signatone()
    siglent_var = Siglent.Siglent()
    stop = input("Press e to stop etching:")
    siglent_var.output_on()
    siglent_var.set_volt(1)
    siglent_var.get_output()
    while stop != "e":
            time.sleep(20)
            image= func.take_image(1,filename)
            signatone.save_image(image)
    if stop == "e":
        siglent_var.reset_values()
        siglent_var.output_off()
        
if __name__ == '__main__':
    main()