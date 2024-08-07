import functions as func
import signatone_driver as Signatone
import siglent_driver as Siglent
import time
import keyboard
import numpy as np

def main():
    bubble_url = 'https://hooks.slack.com/services/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'
    area_url = 'https://hooks.slack.com/services/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'
    signatone = Signatone.Signatone()
    # siglent = Siglent.Siglent()
    
    start_time = time.time()
    
    # siglent.output_on()
    # siglent.set_volt(8)
    # siglent.set_curr(4)
    # siglent.get_output()
    
    corners = func.calculate_corner_coords(9, 75, 250) # w/out trench 250 microns, w/ 200 microns
    src_points = np.array(corners)
    dst_points = np.array([[-23313, -9700], [-23234, -12522], [-26064, -12588]]) # LL, UL, UR corners 
    
    matrix = func.get_affine_transform(src_points, dst_points)
    
    gds_coor = func.get_mem_coords(9, 75, 250)
    
    dev_coor = func.apply_affine_all_mems(matrix, gds_coor, 9)
    
    # check which device we're set to
    print(signatone.get_device())
    
    # move to next square membrane
    signatone.set_device('WAFER') # in the program, chuck is actually called wafer, WAFER/wafer both work
    
    for x in range(0, 81):
        signatone.move_abs(dev_coor[x][0], dev_coor[x][1])
    
    # signatone.set_device('CAP4')
    # signatone.move_abs(-10452, )
    
    # signatone.set_device('CAP1')
    
    # # check coordinates
    # print(signatone.get_cap())
    
    counter = 0
    print("end")
        
        
if __name__ == '__main__':
    main()