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
    # slack channel urls
    bubble_url = 'https://hooks.slack.com/services/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'
    area_url = 'https://hooks.slack.com/services/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'
    
    # initializing our variables
    start_time = time.time()
    tether = False
    img_count = 0
    siglent.set_volt(8)
    siglent.set_curr(4)
    bubble_count = 0
    
    # check if siglent is off and prepare for new etch
    if (siglent.get_output()[0] < 1):
        # increase image counter
        img_count += 1
            
        # take picture through scope
        img_path = Functions.take_image(img_count)
        signatone.save_image(img_path)
        print(img_path)
            
        # TESTING: get current coordinates of square
        # x, y, w, h, detected = Functions.square_detect(img_path)
        # print(x, y, w, h, detected)
                
        # NOT READY: adjust proes until alidned with square
        # Functions.probe_adjustment(square_coor)
                
        # confirm if on a new square
        dark_area = Functions.areaDetectColorBinary(img_path)
        print(dark_area)
        if dark_area > 97:
            siglent.output_on()
            print("confirmed new etch")
            
    # run while tether is yet to be finished or q is pressed
    while not tether:
        # get the current time
        curr_time = time.time()
        dark_area = 0
            
        # if 20 seconds have passed, check on the membrane
        if curr_time - start_time > 20:
            # increase image counter
            img_count += 1
            
            # take picture through scope
            img_path = Functions.take_image(img_count)
            signatone.save_image(img_path)
            print(img_path)
               
            # detect bubbles, notify team on slack, clean bubbles
            bubble_count = Functions.bubble_detect(bubble_count, img_path)
            
            if bubble_count > 0:
                Functions.send_slack_message(bubble_url, "Bubble Obstruction!")
                # NOT READY: water pump
                    
            # check tether percentage
            Functions.area_detect()
                    
            # end of etch
            if dark_area <= 7:
                siglent.output_off()
                Functions.send_slack_message("Tether Minimum Reached! Etch Complete.")
                tether = True
            
            # start the 20 second counter again
            start_time = time.time()
                
        # keyboard waits for you to press 'q' if you want to end etch early
        if keyboard.is_pressed('q'):
            siglent.reset_values()
            siglent.output_off()
            break
        
    # double check that output is off, disconnect from device and end function    
    Functions.delete_image(img_count)
    siglent.reset_values()
    siglent.output_off()
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
    
    # begin etching the grid
    for x in range(0, int(row_len)):
        for y in range(0, int(col_len)):
            etch_one_membrane(siglent, signatone)
                    
        # move to next square
        
    # check that the Siglent output has fully dropped to 0V
    volt_output = siglent.get_output()

    while volt_output != 0:
        siglent.output_off()
        volt_output = siglent.get_output()
        
    print("Siglent Voltage at 0V.")
    print("full grid end")

    # disconnect from devices    
    siglent.close()
    signatone.close()