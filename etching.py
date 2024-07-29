"""

    Automation program for the etching of diamond membranes of a 9x9 sample grid.

    Authors: UIC Chicago Tech Circle Team (Lisset Rico, Fernanda Villalpando)
    Collaborator(s): Argonne National Laboratory (Nazar Delegan, Clayton Devault)
    Date Created: 06/26/2024

"""

import time
import keyboard
import siglent_driver as Siglent
import signatone_driver as Signatone
import functions as Functions
import numpy as np
import config


"""

    etch_one_membrane : etches a single diamond membrane
    
    Args:
        siglent: object
        signatone: object
    Returns:
        None.
    Raises:
        None.
    Citations: 
        None. 

"""
def etch_one_membrane(siglent:object, signatone:object):
    # initializing our variables
    start_time = time.time()
    tether = False
    img_count = 0
    bubble_count = 0
    # siglent.set_volt(8)
    # siglent.set_curr(4)
    
    # check if siglent is off and prepare for new etch
    # if (siglent.get_output()[0] < 1):
    if not tether:
        # increase image counter
        img_count += 1
            
        # take picture through scope
        img_path = Functions.take_image(img_count)
        signatone.save_image(img_path)
        print(img_path)
                
        # crop image to get targeted square
        crop_img_name = 'CIM_' + str(img_count) + '.bmp'
        crop_img_path = 'C:\\CM400\\photos\\'
        # Functions.crop_image(700, 340, 0, 0, 400, 400, img_path, crop_img_name, crop_img_path)
        Functions.crop_image(825, 380, 0, 0, 325, 325, img_path, crop_img_name, crop_img_path)
        
        # TESTING: get current coordinates of square
        # x, y, w, h, detected = Functions.square_detect(img_path)
        # print(x, y, w, h, detected)
                
        # NOT READY: adjust proes until alidned with square
        # Functions.probe_adjustment(square_coor)
        
        # confirm if on a new square
        crop_img = crop_img_path + crop_img_name
        print(crop_img)
        dark_area = Functions.areaDetectColorBinary(crop_img)
        print("heres", dark_area)
        if dark_area > 97:
            # siglent.output_on()
            print("confirmed new etch")
            
    # run while tether is yet to be finished or q is pressed
    # while not tether:
    #     # get the current time
    #     curr_time = time.time()
    #     dark_area = 0
            
    #     # if 20 seconds have passed, check on the membrane
    #     if curr_time - start_time > 20:
    #         # increase image counter
    #         img_count += 1
            
    #         # take picture through scope
    #         img_path = Functions.take_image(img_count)
    #         signatone.save_image(img_path)
    #         print(img_path)
               
    #         # detect bubbles, notify team on slack, clean bubbles
    #         bubble_count = Functions.bubble_detect(bubble_count, img_path)
            
    #         if bubble_count > 0:
    #             Functions.send_slack_message(config.Bubbles,"Bubble Obstruction!")
    #             # NOT READY: water pump
                    
    #         # check tether percentage
    #         dark_area = Functions.areaDetectColorBinary(img_path)
                    
    #         # end of etch
    #         if dark_area <= 7:
    #             # siglent.output_off()
    #             Functions.send_slack_message(config.Diamonds,"Diamond Tether Appeared. Etch Complete!")
    #             tether = True
            
    #         # start the 20 second counter again
    #         start_time = time.time()
                
    #     # keyboard waits for you to press 'q' if you want to end etch early
    #     if keyboard.is_pressed('q'):
    #         # siglent.reset_values()
    #         # siglent.output_off()
    #         break
        
    # # double check that output is off, disconnect from device and end function    
    # Functions.delete_image(img_count)
    # siglent.reset_values()
    # siglent.output_off()
    print("single etch end")

    
"""

    full_grid_etch : runs the cut function for a full grid
    
    Args:
        row_len: integer
        col_len: integer
    Returns:
        None.
    Raises:
        None.
    Citations: 
        None. 

"""
def full_grid_etch(row_len:int, col_len:int):
    # setting up our devices
    siglent = Siglent.Siglent()
    signatone = Signatone.Signatone()
    
    corners = Functions.calculate_corner_coords(9, 75, 250) # w/out trench 250 microns, w/ 200 microns
    src_points = np.array(corners)
    dst_points = np.array([[-15060, -9988], [-15000, -12822], [-17958, -12886]])
    
    matrix = Functions.get_affine_transform(src_points, dst_points)
    
    gds_coor = Functions.get_mem_coords(9, 75, 250)
    
    dev_coor = Functions.apply_affine_all_mems(matrix, gds_coor, 9)
    
    # begin etching the grid
    for x in range(0, int(row_len)):
        # move to next square membrane
        signatone.set_device('WAFER') # in the program, chuck is actually called wafer, WAFER/wafer both work
        signatone.move_abs(dev_coor[x][0], dev_coor[x][1])
            
        etch_one_membrane(siglent, signatone)
        
    # check that the Siglent output has fully dropped to 0V
    # volt_output = siglent.get_output()

    # while volt_output != 0:
    #     siglent.output_off()
    #     volt_output = siglent.get_output()
        
    print("Siglent Voltage at 0V.")
    print("full grid end")

    # disconnect from devices    
    # siglent.close()
    # signatone.close()