import functions as func
import signatone_driver as Signatone
import siglent_driver as Siglent
import time
import keyboard

def main():
    filename = None
    bubble_url = 'https://hooks.slack.com/services/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'
    area_url = 'https://hooks.slack.com/services/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'
    signatone = Signatone.Signatone()
    siglent_var = Siglent.Siglent()
    
    stop = input("Press s to start etching:")
    
    start_time = time.time()
    
    siglent_var.output_on()
    siglent_var.set_volt(8)
    siglent_var.set_curr(4)
    siglent_var.get_output()
    
    counter = 0
    while True:
        curr_time = time.time()
        
        if curr_time - start_time > 20:
            counter+=1
            image = func.take_image(counter,filename)
            signatone.save_image(image)
            print("image name:", image)
            
            start_time = time.time()
            
            # time.sleep(5)
            bubble_count = 1
            if bubble_count > 0:
                bubble_count = func.bubble_detect(bubble_count, image)

                # check if bubbles are gone
                if bubble_count > 0:
                    func.send_slack_message(bubble_url, "Bubble Obstruction!")
                    # water pump
            
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