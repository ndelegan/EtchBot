"""

    Automation program for the etching of diamond membranes of a 9x9 sample grid.

    Authors: UIC Chicago Tech Circle Team 2024 (Lisset Rico, Fernanda Villalpando)
             UIC Chicago Tech Circle Team 2025()
    Collaborator(s): Argonne National Laboratory (Nazar Delegan, Clayton Devault)
    Date Created: 06/26/2024
    Date Updated: 06/02/2025

"""
# test test
import time
import keyboard
import siglent_driver as Siglent
import signatone_driver as Signatone
import functions as Functions
import numpy as np
import config
import cv2
import threading
from queue import Queue
 
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
def etch_one_membrane(siglent:object, signatone:object,  x, z_to_lower_1, z_to_lower_4):
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

        # if output is low assume 21 seconds for instant image taking
        if (siglent.get_output()[0] < 0.5):
            lap_time = 21
        
        # if 20 seconds have passed or start of new membrane: check on the membrane
        if lap_time > 20:
            # increase image counter
            img_count += 1
                
            # take picture through scope
            img_path = Functions.take_image(img_count)
            signatone.save_image(img_path)
            print("Full image:", img_path)
            
            
            #stop=input("check pic")       
            # crop image to get targeted square
            crop_name = 'CIM_' + str(img_count) + '.bmp'
            crop_path = 'C:\\CM400\\photos\\'
            crop_img_path = crop_path + crop_name


            #Functions.crop_image(700, 390, 350, 350, img_path, crop_name, crop_path)
            #Functions.testing_square(  crop_img_path)
            #need to correct measurements for targeted square (MANUAL RN)
            #Functions.crop_image(1100, 1100, 200, 200, img_path, crop_name, crop_path)
            #Functions.crop_image(700, 390, 340, 340, img_path, crop_name, crop_path)
            
            #6/4: testing automatic crop detection
            
            # cropped_img = Functions.crop_using_square_detect(img_path, crop_img_path)
            # if not cropped_img:
            #     print("skip due to no square detection")
            #     continue
            # print("cropped image:", cropped_img)
            
            # cv2.imshow("cropped membrane", cv2.imread(crop_img_path))
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
                        
            # image = cv2.imread(img_path)
            
            # x, y, w, h, _ = Functions.square_detect(img_path)
            
            # square_crop = image[y:y+h, x:x+w]
            # cv2.imwrite(crop_img_path, square_crop)
            
            # TESTING: get current coordinates of square in pixels
            #x, y, w, h, detected_square = Functions.square_detect(crop_img_path)
            #rint(x, y, w, h, detected_square)

            #print(x, ' ', y, ' ', w, ' ', h, ' ', detected_square)
            # TESTING: get current coordinates of probes in pixels    
            #detected_probes, cap1, cap4 = Functions.probe_detection(crop_img_path)
            # what shuld be an eroor if we dont see probes or square??? 
            # if not detected_square or not detected_probes:
            #     print('Square or probes not detected. Please re-adjust probes, chuck or scope through PM40 before starting the etch again.')
            #     # disconnect from devices
            #     siglent.close()
            #     signatone.close()
            #     quit()

            # NOT READY: adjust probes until aligned with square
            #            pixel to micron for probes
            # Currently probes are being adjusted for first membrane manually
            #  but we can automate it later
            bubble_count=0#Functions.bubble_detect(bubble_count, img_path)
            while bubble_count > 0:
                siglent.output_off()
                # here add water
                time.sleep(10)
                
                img_count += 1
                
                # take picture through scope
                img_path = Functions.take_image(img_count)
                signatone.save_image(img_path)
                print(img_path)
                
                        
                # crop image to get targeted square
                crop_name = 'CIM_' + str(img_count) + '.bmp'
                crop_path = 'C:\\CM400\\photos\\'
                crop_img_path = crop_path + crop_name

                #need to correct measurements for targeted square (MANUAL RN)
                Functions.crop_image(765, 345, 340, 340, img_path, crop_name, crop_path)
                
                x, y, w, h, detected_square = Functions.square_detect(crop_img_path)
                print(x, y, w, h, detected_square)
                
                bubble_count=Functions.bubble_detect(bubble_count, img_path)
             
                
                

            # check current unetched area
            dark_area =  77# Functions.areaDetectColorBinary(crop_img_path)
            
            print('dark area: ', dark_area)
            # current square in unetched and output is off/low
            if dark_area > 7 and siglent.get_output()[0] < 0.5 and bubble_count==0:
                print('Confirmed Etchable Square.')
                # currenty this is a manual check for every membrane
                # we need to make manual check only for first membrane
                # and then automate it for the rest of the membranes
                if x==0:
                    on = input('\nStart Etching? Check probe placement, lower them and enter any letter to start or \'q\' to quit: ')
                    
                if x!=0:
                    signatone.set_device("CAP1")
                    signatone.move_z(z_to_lower_1) # move to the z height of the first probe
                    signatone.set_device("CAP4")                
                    signatone.move_z(z_to_lower_4) # move to the z height of the second probe
                
                # change it to be "keyboard" check
                if keyboard.is_pressed('q') :
                    # disconnect from devices
                    siglent.close()
                    signatone.close()
                    quit()
                
                siglent.output_on()
 
        #     detect bubbles, notify team on slack, clean bubbles
        #    bubble_count = Functions.bubble_detect(bubble_count, img_path)
        #    if bubble_count > 0:
        #         fix error "config.Bubbles"
        #         Functions.send_slack_message(config.Bubbles,"Bubble Obstruction!")
        #         NOT READY: water pump
        #         maybe trun off signatone output? add water? loop till no bubble on the square? turn machine back on?
                    
            # check tether percentage
            print("Checking dark area again")
            dark_area = 6#  Functions.areaDetectColorBinary(crop_img_path)
            print('dark area2: ', dark_area)       
            # end of etch
            if dark_area <= 7:
                siglent.output_off()
                signatone.move_probes_z(500) # move up by 100 microns
                #sending confirmation message to slack
                #Functions.send_slack_message(config.Diamonds,"Diamond Tether Appeared. Etch Complete!")
                tether = True
            
            # start the 20 second counter again
            start_time = time.time()
        # maybe keep same letter for all the time? a or q?
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
            
      
        if keyboard.is_pressed('q') or check == 'q':
            siglent.reset_values()
            siglent.output_off()
            break
            
    print("before pic delete")  
    # double check that output is off, delete images taken during etch  
    Functions.delete_image(img_count)
    siglent.reset_values()
    siglent.output_off()
    
    print('single etch end')    
    
def display_feed(frame_queue):
    while True:
        frame = frame_queue.get()
        cv2.imshow("Display", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    
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
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened() is True: 
        print("yes")
    else: print("No")
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
    
     # get z height of middle of every membrane (should it be height of the probes? whci one? cuz thechicaaly i need both) 
    z_heights_1=Functions.get_z_heights(num_mem, -4853, -4852, -4783,dev_coor, dst_points)# in relation to coordintes of cap1
    z_heights_4=Functions.get_z_heights(num_mem, -7058, -7014, -6985,dev_coor, dst_points) # in relation to coordintes of cap4
    # z of what? probes? which one? techinally need boths
    z_when_touching_first_membrane_1=-7044
    z_when_ready_to_etch_first_1=-6985 # couple of microns above the membrane, so probes are not touching it
    diff_z_1 = z_when_ready_to_etch_first_1 - z_when_touching_first_membrane_1 # how much do we being it up after touching the first membrane

    z_when_touching_first_membrane_4=0
    z_when_ready_to_etch_first_4=0 # couple of microns above the membrane, so probes are not touching it
    diff_z_4 = z_when_ready_to_etch_first_4 - z_when_touching_first_membrane_4 # how much do we being it up after touching the first membrane
        

    print("before queue")
    frame_queue = Queue()
    thread = threading.Thread(target=display_feed, args=(frame_queue,))
    thread.start()
    print("before loop")
    while True:
        print("in loop")
        ret, frame = cap.read()
        if not ret:
            break
        frame_queue.put(frame.copy())  # Share frame to another output 
        
   
    for x in range(0, num_mem):
        # change current device to wafer
        signatone.set_device('WAFER') # in the program, chuck is actually called wafer, WAFER/wafer both work
        # move wafer 
        signatone.move_abs(dev_coor[x][0], dev_coor[x][1])
      
        # start etching
        z_to_lower_1 = z_heights_1[x] + diff_z_1  # lower probe 1 to the membrane
        z_to_lower_4 = z_heights_4[x] + diff_z_4  # lower probe 1 to the membrane
        etch_one_membrane(siglent, signatone, x, z_to_lower_1, z_to_lower_4) 
        
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
    
    # siglent = Siglent.Siglent()
    # signatone = Signatone.Signatone()
    
    # signatone.set_device("CAP1")
    # signatone.move_z(-5000)
    
    # img_count = 79
                
    # # take picture through scope
    # img_path = Functions.take_image(img_count)
    # signatone.save_image(img_path)
    # print(img_path)
            
    # # crop image to get targeted square
    # crop_name = 'CIM_' + str(img_count) + '.bmp'
    # crop_path = 'C:\\CM400\\photos\\'
    # crop_img_path = crop_path + crop_name
    # Functions.crop_image(750, 350, 500, 500, img_path, crop_name, crop_path)
    # #Functions.crop_using_square_detect(img_path, crop_img_path)
    # Functions.testing_square(crop_img_path)
    
    #full_grid_etch(12 , 9 , 75 , 250 , -18149 , -7293, -18058, -10097 , -20899 , -10174)
    
    # signatone = Signatone.Signatone()
    
    # img_path = Functions.take_image(900)
    # signatone.save_image(img_path)
    # img = cv2.imread(img_path)

    # if img is None:
    #     print("Error: Failed to load image at", img_path)
    # else:
    #     Functions.auto_crop_from_dark_probes(img_path)