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
    Exceptions:
        None.

"""
def etch_one_membrane(siglent:object, signatone:object):
    # initializing our variables
    start_time = time.time()
    tether = False
    img_count = 0
    bubble_count = 0
    siglent.set_volt(8)
    siglent.set_curr(4)
            
    # run while tether is yet to be finished or q is pressed
    while not tether:
        # initialize variables: get current time, how much time has passed and dark area
        curr_time = time.time()
        lap_time = curr_time - start_time
        dark_area = 0
            
        if (siglent.get_output()[0] < 0.5):
            lap_time = 21
        
        # if 20 seconds have passed or start of new membrane: check on the membrane
        if lap_time > 20:
            # increase image counter
            img_count += 1
                
            # take picture through scope
            img_path = Functions.take_image(img_count)
            signatone.save_image(img_path)
            print(img_path)
                    
            # crop image to get targeted square
            crop_name = 'CIM_' + str(img_count) + '.bmp'
            crop_path = 'C:\\CM400\\photos\\'
            crop_img_path = crop_path + crop_name
            Functions.crop_image(625, 340, 0, 0, 550, 450, img_path, crop_name, crop_path)
            # Functions.crop_image(825, 380, 0, 0, 325, 325, img_path, crop_name, crop_path)
            
            # TESTING: get current coordinates of square
            x, y, w, h, detected = Functions.square_detect(crop_img_path)
            print(x, ' ', y, ' ', w, ' ', h, ' ', detected)
                    
            detected, cap1, cap4 = Functions.probe_adjustment(crop_img_path)
            
            # NOT READY: adjust probes until aligned with square
            #            pixel to micron for probes
            
            # check current unetched area
            dark_area = Functions.areaDetectColorBinary(crop_img_path)
            
            print('dark area: ', dark_area)
            if dark_area > 50 and siglent.get_output()[0] < 0.5:
                print('Confirmed Etchable Square.')
                
                on = input('\nStart Etching? Check probe placement, lower them and enter any letter to start or \'q\' to quit: ')
                
                if on == 'q':
                    # disconnect from devices
                    siglent.close()
                    signatone.close()
                    quit()
                
                siglent.output_on()
               
            # detect bubbles, notify team on slack, clean bubbles
            bubble_count = Functions.bubble_detect(bubble_count, img_path)
            
            if bubble_count > 0:
                Functions.send_slack_message(config.Bubbles,"Bubble Obstruction!")
                # NOT READY: water pump
                    
            # check tether percentage
            dark_area = Functions.areaDetectColorBinary(img_path)
                    
            # end of etch
            if dark_area <= 7:
                siglent.output_off()
                signatone.set_device('CAP4')
                signatone.move_z(-5)
                signatone.set_device('CAP4')
                signatone.move_z(-5)
                Functions.send_slack_message(config.Diamonds,"Diamond Tether Appeared. Etch Complete!")
                tether = True
            
            # start the 20 second counter again
            start_time = time.time()
        
        # if anything starts to go wrong user can enter 'a' to abort
        check = ''
        if keyboard.is_pressed('a'):
            print('ABORTED ACTION')
            signatone.abort_motion()
            siglent.output_off()
            
            while check != 'c' or check != 'q':
                check = input('\nPlease re-adjust probes, chuck or scope through PM40 before starting the etch again. Enter any letter to start etching again or \'q\' to quit: ')
            
            if check != 'q':
                siglent.voltage_on()
            
        # keyboard waits for you to press 'q' pr checks if you pressed q during abort process if you want to end etch early
        if keyboard.is_pressed('q') or check == 'q':
            siglent.reset_values()
            siglent.output_off()
            break
            
        
    # double check that output is off, delete images taken during etch  
    Functions.delete_image(img_count)
    siglent.reset_values()
    siglent.output_off()
    
    print('single etch end')

    
"""

    full_grid_etch : moves from one membrane to the next while calling etch_one_membrane between every movement
    
    Args:
        num_mem: integer -> # of membranes
        row_mem: integer -> # of membranes in a row
        street: integer -> street width
        grid_len: integer -> length of one side of the grid
        x_ll: integer -> lower-left grid X coordinate
        y_ll: integer -> lower-left grid Y coordinate
        x_ul: integer -> upper-left grid X coordinate
        y_ul: integer -> upper-left grid Y coordinate
        x_ur: integer -> upper-right grid X coordinate
        y_ur: integer -> upper-right grid Y coordinate
    Returns:
        None.
    Exceptions:
        None.

"""
def full_grid_etch(num_mem:int, row_mem:int, street:int, grid_len:int, x_ll:int, y_ll:int, x_ul:int, y_ul:int, x_ur:int, y_ur:int):
    # setting up our devices
    siglent = Siglent.Siglent()
    signatone = Signatone.Signatone()
    
    # begin creating the square membranes center coordinates list
    corners = Functions.calculate_corner_coords(row_mem, street, grid_len) # w/out trench 250 microns, w/ 200 microns
    src_points = np.array(corners)
    dst_points = np.array([[x_ll, y_ll], [x_ul, y_ul], [x_ur, y_ur]])
    matrix = Functions.get_affine_transform(src_points, dst_points)
    gds_coor = Functions.get_mem_coords(row_mem, street, grid_len)
    dev_coor = Functions.apply_affine_all_mems(matrix, gds_coor, row_mem)
    
    # begin grid movement
    for x in range(0, num_mem):
        # change current device to wafer
        signatone.set_device('WAFER') # in the program, chuck is actually called wafer, WAFER/wafer both work
        # move wafer 
        signatone.move_abs(dev_coor[x][0], dev_coor[x][1])
        # start etching
        etch_one_membrane(siglent, signatone)
        
    # check that the Siglent output has fully dropped to 0V
    volt_output = siglent.get_output()

    while volt_output != 0:
        siglent.output_off()
        volt_output = siglent.get_output()
        
    print('Siglent Voltage at 0V.')
    print('full grid end')

    # disconnect from devices    
    siglent.close()
    signatone.close()
    
    
if __name__ == '__main__':
    '''
        manually enter the following info in the given order:
        
        full_grid_etch(# of membranes, 
                       # of membranes in a row,
                       street width,
                       length of one side of the grid,
                       lower-left grid X coordinate,
                       lower-left grid Y coordinate,
                       upper-left grid X coordinate,
                       upper-left grid Y coordinate,
                       upper-right grid X coordinate,
                       upper-right grid Y coordinate)
    '''
    full_grid_etch(1 , 9 , 75 , 250 , -23313 , -9700 , -23234 , -12522 , -26064 , -12588)