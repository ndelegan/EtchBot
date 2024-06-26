"""

    Automation program for the etching of diamond membranes from a 9x9 sample grid.

    Authors: UIC Chicago Tech Circle Team (Andrea Munoz, Fernanda Villalpando, Claudia Jimenez, Lisette Ruano, Aima , Lisset Rico)
    Collaborator(s): Argonne National Laboratory (Nazar Delegan, Clayton Devault)
    Date Created: 06/26/2024

"""

import time
import siglent_driver as Siglent
import signatone_driver as Signatone
import functions as Functions

bubble_url = 'https://hooks.slack.com/services/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'
area_url = 'https://hooks.slack.com/services/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'

# setting up our devices
siglent = Siglent.Siglent()
signatone = Signatone.Signatone()

# initializing our variables
row_len = 9
col_len = 9
img_count = 0
tether = False


# Assume that sample is set up in center as start point

for x in range(0, row_len):
    for y in range(0, col_len):
        
        # run while tether not found
        while not tether:
            time.sleep(120)
            
            bubble_count = 0
            dark_area = 0
            light_area = 0
            
            # take picture through scope
            image_name = Functions.take_image(1, " ")   
            print(image_name)
            
            # move probes according to image
            
            # detect current unetched area
            
            # beginning of etch
            if dark_area > 98:
                siglent.output_on()
            
            # detect bubble
            bubble_count = Functions.bubble_detect(bubble_count, image_name)
            
            if bubble_count > 0:
                Functions.send_slack_message("Bubble Obstruction!")
            
            # check tether percentage
            
            # end of etch
            if light_area <= 7:
                siglent.output_off()
                Functions.send_slack_message("Tether Minimum Reached! Etch Complete.")
                
                
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