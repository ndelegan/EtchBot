import functions as func
import signatone_driver as Signatone
import siglent_driver as Siglent
import time
import keyboard

def main():
    bubble_url = 'https://hooks.slack.com/services/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'
    area_url = 'https://hooks.slack.com/services/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'
    signatone = Signatone.Signatone()
    siglent = Siglent.Siglent()
    
    stop = input("Press s to start etching:")
    
    start_time = time.time()
    
    # siglent.output_on()
    # siglent.set_volt(8)
    # siglent.set_curr(4)
    # siglent.get_output()
    
    coor = func.apply_affine_all_mems()
    
    print(coor)
    
    counter = 0
    while True:
        curr_time = time.time()
        
        if curr_time - start_time > 20:
            counter+=1
            image = func.take_image(counter)
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
            # siglent.reset_values()
            # siglent.output_off()
            break
        
    print(counter)
    func.delete_image(counter)
    # siglent.reset_values()
    # siglent.output_off()
    print("end")
        
        
if __name__ == '__main__':
    main()