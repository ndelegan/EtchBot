"""

    Automation program for the etching of diamond membranes from a 9x9 sample grid.

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

    etch_one_membrane : etches a single membrane
    
    Args:
        siglent : object
        signatone : object
    Returns:
        None.
    Raises:
        None.
    Citations: 
        None. 

"""
def etch_one_membrane(siglent, signatone):
    # slack channel urls
    bubble_url = 'https://hooks.slack.com/services/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'
    area_url = 'https://hooks.slack.com/services/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'
    
    # initializing our variables
    start_time = time.time()
    tether = False
    img_count = 0
    # bubble_count = 0
    # dark_area = 0 
            
    # run while tether not found
    while True:
        # get the current time
        curr_time = time.time()
        
        bubble_count = 0
        dark_area = 0 
        
        # if 20 seconds have passed, check on the membrane
        if curr_time - start_time > 20:
            img_count+=1
            
            # take picture through scope
            image_name = Functions.take_image(img_count, " ")
            signatone.save_image(image_name)
            print(image_name)
                    
            # check whether the etch is in process or on a new square
            if (siglent.get_output() == 0):
                square_coor = Functions.square_detect(image_name)
                Functions.probe_adjustment(square_coor)
                        
                if Functions.area_detect(image_name) > 97:
                    siglent.output_on()
                else:
                    square_coor = Functions.square_detect(image_name)
                        
                    # move probes according to full square or partial etch
                    Functions.probe_adjustment(image_name)
                        
                    Functions.area_detect(image_name) 
                    
                # detect bubble and clean 
                while bubble_count > 0:
                    bubble_count = Functions.bubble_detect(bubble_count, image_name)

                    # check if bubbles are gone
                    if bubble_count > 0:
                        Functions.send_slack_message("Bubble Obstruction!")
                        # water pump
                    
                # check tether percentage
                Functions.area_detect()
                    
                # end of etch
                if dark_area <= 7:
                    siglent.output_off()
                    Functions.send_slack_message("Tether Minimum Reached! Etch Complete.")
            
            # keyboard waits for you to press 'q' if you want to end etch early
            if keyboard.is_pressed('q'):
                siglent.reset_values()
                siglent.output_off()
                break
            
    Functions.delete_image(img_count)
    siglent.reset_values()
    siglent.output_off()
    print("single etch end")

    
"""

    full_grid_etch : runs the cut function for a full membrane
    
    Args:
        row_len : integer
        col_len : integer
    Returns:
        None.
    Raises:
        None.
    Citations: 
        None. 

"""
def full_grid_etch(row_len, col_len):
    # setting up our devices
    siglent = Siglent.Siglent()
    signatone = Signatone.Signatone()
    
    # Assume that sample is set up in center as start point
    for x in range(0, row_len):
        for y in range(0, col_len):
            etch_one_membrane(siglent, signatone)
                    
        # move to next square
        
        
    # check that the Siglent output has fully dropped to 0V
    volt_output = siglent.get_output()

    while volt_output != 0:
        siglent.output_off()
        volt_output = siglent.get_output()
        
    print("Siglent Voltage at 0V.")

    # disconnect from devices    
    siglent.close()
    signatone.close()