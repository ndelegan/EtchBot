import functions as func
import signatone_driver as Signatone
import siglent_driver as Siglent
import time
import keyboard
import numpy as np

def main():
    bubble_url = 'https://hooks.slack.com/services/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'
    area_url = 'https://hooks.slack.com/services/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'
    # signatone = Signatone.Signatone()
    # siglent = Siglent.Siglent()
    
    stop = input("Press s to start etching:")
    
    start_time = time.time()
    
    # siglent.output_on()
    # siglent.set_volt(8)
    # siglent.set_curr(4)
    # siglent.get_output()
    
    corners = func.calculate_corner_coords(9, 50, 50, 250) # w/out trench 250 microns, w/ 200 microns
    src_points = np.array(corners)
    dst_points = np.array([[-12395, -8640], [-12460, -11890], [-15705, -11820]])
    
    matrix = func.get_affine_transform(src_points, dst_points)
    
    gds_coor = func.get_mem_coords(9, 50, 50, 250)
    
    dev_coor = func.apply_affine_all_mems(matrix, gds_coor, 9)
    
    print(dev_coor)
    
    counter = 0
    # while True:
    #     curr_time = time.time()
        
    #     if curr_time - start_time > 20:
    #         counter+=1
    #         image = func.take_image(counter)
    #         signatone.save_image(image)
    #         print("image name:", image)
            
    #         start_time = time.time()
            
    #         # time.sleep(5)
    #         bubble_count = 1
    #         if bubble_count > 0:
    #             bubble_count = func.bubble_detect(bubble_count, image)

    #             # check if bubbles are gone
    #             if bubble_count > 0:
    #                 func.send_slack_message(bubble_url, "Bubble Obstruction!")
    #                 # water pump
            
    #     if keyboard.is_pressed('q'):
    #         # siglent.reset_values()
    #         # siglent.output_off()
    #         break
        
    print(counter)
    # func.delete_image(counter)
    # siglent.reset_values()
    # siglent.output_off()
    print("end")
        
        
if __name__ == '__main__':
    main()