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

def etch_one_membrane(siglent:object, signatone:object, affine_matrix, dev_xy:tuple, img_count_offset:int):
    start_time = time.time()
    tether = False
    img_count = img_count_offset
    bubble_count = 0
    siglent.set_volt(8)
    siglent.set_curr(4)

    while not tether:
        curr_time = time.time()
        lap_time = curr_time - start_time
        dark_area = 0

        if siglent.get_output()[0] < 0.5:
            lap_time = 21

        if lap_time > 20:
            img_count += 1
            img_path = Functions.take_image(img_count)
            signatone.save_image(img_path)
            print("Full image:", img_path)

            pred_x_img, pred_y_img = Functions.predict_crop_pixel_from_affine(dev_xy, affine_matrix)
            print(f"Predicted crop center in image: ({pred_x_img}, {pred_y_img})")

            crop_img = Functions.crop_from_prediction(img_path, pred_x_img, pred_y_img, box_size=290)

            cv2.imshow("Cropped Membrane", crop_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            temp_crop_path = "C:\\CM400\\photos\\temp_crop.bmp"
            cv2.imwrite(temp_crop_path, crop_img)

            # dark_area = Functions.areaDetectColorBinary(temp_crop_path)
            # print('dark area:', dark_area)
            
            dark_area = Functions.areaDetectColorRange(temp_crop_path, (130, 25, 95), (175, 90, 205))
            print('dark area:', dark_area)
            

            if dark_area > 50 and siglent.get_output()[0] < 0.5:
                print('Confirmed Etchable Square.')
                on = input('\nStart Etching? Check probe placement, lower them and enter any letter to start or \'q\' to quit: ')
                
                if keyboard.is_pressed('q') or on == 'q':
                    siglent.close()
                    signatone.close()
                    quit()

                siglent.output_on()

            #dark_area = Functions.areaDetectColorBinary(temp_crop_path)

            if dark_area <= 7:
                siglent.output_off()
                signatone.set_device('CAP4')
                x = signatone.get_cap()
                xc = x.split(",")
                #signatone.move_z(str(float(xc[2]) + 100.0))
                signatone.set_device('CAP1')
                x = signatone.get_cap()
                #signatone.move_z(str(float(xc[2]) + 100.0))
                tether = True

            start_time = time.time()

        check = ''
        if keyboard.is_pressed('a'):
            print('ABORTED ACTION')
            signatone.abort_motion()
            siglent.output_off()

            while check != 'c' or check != 'q':
                check = input('\nPlease re-adjust probes. Enter any letter to continue or \'q\' to quit: ')

            if check != 'q':
                siglent.voltage_on()

        if keyboard.is_pressed('q') or check == 'q':
            siglent.reset_values()
            siglent.output_off()
            break

    Functions.delete_image(img_count)
    siglent.reset_values()
    siglent.output_off()

    print('single etch end')

def full_grid_etch(num_mem:int, row_mem:int, street:int, grid_len:int, x_ll:int, y_ll:int, x_ul:int, y_ul:int, x_ur:int, y_ur:int):
    siglent = Siglent.Siglent()
    signatone = Signatone.Signatone()

    corners = Functions.calculate_corner_coords(row_mem, street, grid_len)
    src_points = np.array(corners)
    dst_points = np.array([[x_ll, y_ll], [x_ul, y_ul], [x_ur, y_ur]])
    matrix = Functions.get_affine_transform(src_points, dst_points)
    gds_coor = Functions.get_mem_coords(row_mem, street, grid_len)
    dev_coor = Functions.apply_affine_all_mems(matrix, gds_coor, row_mem)

    # CALIBRATION STEP - FULL AFFINE
    print("\n--- Starting Full Affine Calibration Helper ---")
    affine_matrix = Functions.calibration_helper_affine(signatone, dev_coor)
    print("\n--- Calibration Done ---\n")

    for x in range(num_mem):
        if x != 0:
            signatone.set_device('CAP4')
            xf = signatone.get_cap()
            xc = xf.split(",")
            #signatone.move_z(str(float(xc[2]) - 100.0))
            signatone.set_device('CAP1')
            #signatone.move_z(str(float(xc[2]) - 100.0))

        signatone.set_device('WAFER')
        signatone.move_abs(dev_coor[x][0], dev_coor[x][1])
        print(f"\n--- Moving to Membrane {x} at stage XY: {dev_coor[x]} ---")

        etch_one_membrane(siglent, signatone, affine_matrix, dev_coor[x], img_count_offset=x*10)

    volt_output = siglent.get_output()
    while volt_output != 0:
        siglent.output_off()
        volt_output = siglent.get_output()

    print('Siglent Voltage at 0V.')
    print('full grid end')
    siglent.close()
    signatone.close()

if __name__ == '__main__':
    full_grid_etch(3, 9, 75, 250, -18240, -6840, -18157, -9667, -20981, -9744)