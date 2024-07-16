import functions as func
import signatone_driver
import signatone_driver as Signatone
import siglent_driver as Siglent
import time
import keyboard

def main():
    time_tuple = time.localtime()
    filename = None
    signatone = Signatone.Signatone()
    siglent_var = Siglent.Siglent()
    
    stop = input("Press s to start etching:")
    
    start_time = time.time()
    
    siglent_var.output_on()
    siglent_var.set_volt(5)
    siglent_var.set_curr(3.57)
    siglent_var.get_output()
    
    counter = 0
    while True:
        curr_time = time.time()
        
        if curr_time - start_time > 20:
            counter+=1
            image= func.take_image(counter,filename)
            signatone.save_image(image)
            print("image name: ", image)
            
            start_time = time.time()
            
        if keyboard.is_pressed('q'):
            siglent_var.reset_values()
            siglent_var.output_off()
            break
        
    print(counter)
    func.delete_image(counter)
    siglent_var.reset_values()
    siglent_var.output_off()
    print("end")
        
if __name__ == '__main__':
    main()