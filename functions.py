"""

    Functions that are used in the etching process within the 'etching.py' file.
    
    Each function was written by different students from the UIC Chicago Tech Circle Team:
        Take Image Author(s): Andrea Munoz
        Bubble Detect Author(s): Fernanda Villalpando
        Area Detect Author(s): Lisette Ruano
        Send Slack Message Author(s): Andrea Munoz
        Square Detect Author(s): Claudia Jimenez, Aima Qutbuddin, Kyle Cheek, Lisette Ruano
        Innermost Square Author(s): Kyle Cheek, Claudia Jimenez
        Calculate Corner Coordinates Author(s): Claudia Jimenez, Aima Qutbuddin
        Get Membrane Coordinates Author(s): Claudia Jimenez, Aima Qutbuddin
        Get Affine Transformation Author(s): Clayton DeVault, Claudia Jimenez
        Apply Affine Transformation Author(s): Claudia Jimenez
        Apply Affine Transformation for All Membranes Author(s): Claudia Jimenez
        *************************************************************************
        Crop From Prediction Author(s):  Michelle Montesinos
        Compute Affine Pixel Stage Transform Author(s):  Michelle Montesinos
        Pedict Crop Pixel From Affine Author(s): Michelle Montesinos
        Calibration Helper Affine Author(s): Michelle Montesinos
        Area Detect Color Range Author(s): Michelle Montesinos
        Get Z Heights Author(s): Yana Ninovska
        Run Water Pump Author(s): Elizabeth Ng
        
        
    Commenting/Code Structure was implemented by Lisset Rico.
        
    Collaborator(s): Argonne National Laboratory (Nazar Delegan, Clayton DeVault), Break Through Tech (Kyle Cheek)
    Date Created: 06/26/2024
    Date Updated: 06/03/2025


"""

import time
import cv2
import requests
import json
import os
import random
import numpy as np
import water_pump

"""
    
    take_image : takes an image and saves it in a certain file path.
    
    Args:
        counter: integer
    Returns:
        img_path: string
    Raises:
        None.
    
"""
def take_image(counter:int):
    string = "C:\\CM400\\photos\\imgCapture"
    string2 = ".bmp"
    img_path = f'{string}{counter}{string2}'
    
    return img_path


"""
    
    delete_image : deletes an image from a given file path.
    
    Args:
        counter: integer
    Returns:
        None.
    Raises:
        None.
    
"""
def delete_image(counter:int):
    string = "C:\\CM400\\photos\\imgCapture"
    string2 = ".bmp"
    
    while True:
        if os.path.exists("C:\\CM400\\photos\\imgCapture1.bmp") is False:
            return False 
        filename = f'{string}{counter}{string2}'
        print(filename)
        os.remove(filename)
        counter-=1
        
        
"""
    
    crop_image : given the path of an image it crops the image, saves it and returns the path.
    
    Args:
        tbd
    Returns:
        None.
    Raises:
        None.
    
"""
def crop_image(start_x, start_y, pixel_w, pixel_h, img_path, crop_img_name, crop_img_path):
    os.chdir(crop_img_path)
    image = cv2.imread(img_path)
    # zoom = cv2.resize(image, (new_w, new_h))
    
    crop = image[start_y : start_y+pixel_h, start_x : start_x+pixel_w]
    
    cv2.imwrite(crop_img_name, crop)
    cv2.imshow('crop_img_name', crop)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return crop_img_path
    
    
     

"""
    
    bubble_detect : detect bubbles in a given image.
    
    Args:
        bubble_count: integer
        img_path: string
    Returns:
        bubble_count: integer
    Raises:
        None.
    
"""
def bubble_detect(bubble_count:int, img_path:str):
    img = cv2.imread(img_path)
    print(img_path)
    
    # converting image to grayscale
    img_gray  = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    # blurring the image for image processing
    img_blur = cv2.blur(img_gray, (25,5))
    
    # detects circles
    detected_circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, .1, 100, param1 = 27, param2 = 31, minRadius=0, maxRadius=300)
    
    if detected_circles is None:
        return 0
    # counts the amount of circles in the list
    len(detected_circles)
    
    # used for drawing circles
    np.uint16(np.around(detected_circles))
    
    # draws image. this section if/for loop is not necessary for automation and can be cmmmented out
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0 , :]:
            a,b,r = pt[0],pt[1],pt[2]
            cv2.circle(img, (a,b), r, (0,255,0), 2)
            cv2.circle(img, (a,b), 1, (0,0,255), 3)
            
    bubble_count = 0
    for c in detected_circles[0, :]:
        # draws the outer green circle to show what bubble is detected.
        # you can comment out both cv2.circle commands.
        cv2.circle(img, (c[0], c[1]), c[2], (0, 255, 0), 3)
        
        # draws the inner red dot in the center of the detected circle.
        cv2.circle(img, (c[0], c[1]), 1, (0, 0, 255), 5)
        bubble_count += 1
        
    return bubble_count


"""
    
    area_detect : detects the percentage of the unetched area of a square given.
    
    Args:
        img_path: string
    Returns:
        whole_number_percentage: integer
    Raises:
        None.
    
"""
def areaDetectNonColor(img_path:str):
    # Read in image location
    image = cv2.imread(img_path)

    # Converts image to gray scale and blurs it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    
    # Sharpens the blurred image
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
    
    # Setting color threshold and cleaning up noise in the picture
    thresh = cv2.threshold(blur, 148, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    black_threshold = 50

    # Counting black pixels and total pixels
    black_pixels = np.count_nonzero(close < black_threshold)
    total_pixels = close.size

    # Calculates percentage of black pixels then shows altered pictures
    percentage_black = (black_pixels / total_pixels) * 100
    whole_number_percentage = int(percentage_black)

    return whole_number_percentage


"""
    
    areaDetectColorBinary : 
    
    Args:
        img_path: string
    Returns:
        whole_number_percentage: integer
    Raises:
        None.
    
"""
def areaDetectColorBinary(img_path:str):

    # read in image location
    image = cv2.imread(img_path)

    # converts image to gray scale and blurs it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    
    # Sharpens the blurred image
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
    
    # Setting color threshold and cleaning up noise in the picture
    # 157 used for gray membranes
    # 148
    # 172 for no color membranes
    # 110

    ret3,otsu = cv2.threshold(sharpen,35,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # thresh = cv2.threshold(sharpen, 155, 255, cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    close = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, kernel, iterations=2)
    black_threshold = 50

    
    # Counting black pixels and total pixels
    black_pixels = np.count_nonzero(close < black_threshold)
    
    total_pixels = otsu.size

    # Calculates percentage of black pixels then shows altered pictures
    percentage_black = (black_pixels / total_pixels) * 100
    whole_number_percentage = int(percentage_black)
    cv2.imshow('close', close) # this shoes black and white pixels
    # cv2.imshow('gray', gray)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return whole_number_percentage


"""
    
    send_slack_message : sends a slack message to a certain slack channel.
    
    Args:
        webhook_url: string
        message: string
    Returns:
        None.
    Raises:
        None.
    
"""
def send_slack_message(webhook_url:str, message:str):
    #Defining JSON
    headers = {'Content-Type': 'application/json'}
    #dictionary payload with message
    payload = {'text': message}

    #POST request to webhook_url
    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

    #status_code = 200 means the message was sent successfully
    if response.status_code == 200:
        print('Message sent successfully to Slack!')
    else:
        print(f'Failed to send message to Slack. Error: {response.status_code}, {response.text}')


"""
    
    innermost_square : returns the most deeply nested square w/ minimum size (square of interest)
    
    Args:
        contours: list -> list of list of points that make up a contour (returned by findContours()) 
        hierarchy: list -> list of indices of contours passed in hierarchical order (returned by findContours()) 
        image: string -> image path of a given image
        min_size: integer -> minimum edge length of square to detect
    Returns:
        x1: integer -> x-coordinate of top left corner of square of interest
        y1: integer -> y-coordinate of top left corner of square of interest
        w1: integer -> width of square of interest
        h1: integer -> height of square of interest
        image: string -> image path of the original given image with a rectangle drawn on
    Raises:
        None.
    
"""
def innermost_square(contours, hierarchy, image:str, min_size:int):

    rects = [] # list for all rectangles detected
    
    # isolate all rectangles in contours
    for contour in range(len(contours)):
        (x,y,w,h) = cv2.boundingRect(contours[contour])
        rects.append((x,y,w,h))

    # make a list of all parent rectangles based on hierarchy, then sort from most to least deeply nested 
    # note: parents are sorted in hierarchical order but children are not sorted as particularly,
    # so here it is easier to sort and search by parents than by children
    parents_list = set([item[3] for items in hierarchy for item in items]) # TO DO: clean up
    parents_sorted_list = sorted(parents_list, reverse=True)

    # add parent candidates to list only if above minimum size 
    parent_candidates = []
    for i in parents_sorted_list:
        if max(rects[i][2],rects[i][3]) > min_size:
            parent_candidates.append(i)

    max_parent_candidate = max(parent_candidates) # most deeply nested parent

    # find children of minimum size and of most deeply nested parent
    child_list = []
    for (index, contour) in enumerate(hierarchy[0]):
        if (contour[3] == max_parent_candidate) and (min(rects[index][2],rects[index][3]) > min_size):
            child_list.append(index)

    # if there are child candidates, pick the most deeply nested child of the most deeply nested parent 
    # or pick the most deeply nested parent (could happen if its children do not meet min size)
    if len(child_list) > 0:
        max_child_candidate = max(child_list)
        deepest_sufficient_contour = max(max_parent_candidate, max_child_candidate)
    # if no child candidates, pick the most deeply nested parent 
    else:
        deepest_sufficient_contour = max_parent_candidate

    # get x,y of top left corner, width, and height of square of interest, draw rectangle
    (x1,y1,w1,h1) = rects[deepest_sufficient_contour]
    cv2.rectangle(image, (x1,y1), (x1+w1,y1+h1), (0,255,0), 2)

    return x1, y1, w1, h1, image


"""

    square_detect : detects whether there is a square in a given image

    Args:
        image: string -> path of image to be processed
    Returns:
        x: integer -> x-coordinate of top left corner of square of interest
        y: integer -> y-coordinate of top left corner of square of interest
        w: integer -> width of square of interest
        h: integer -> height of square of interest        
        detected: boolean -> true if a square is found, false otherwise (note: under construction)
        result: string -> copy of original image with detected square superimposed (also displayed on screen) (note: may change later)
    Raises:
        No errors. Assumes that all devices are operating correctly.
            
"""
def square_detect(img_path):
    image = cv2.imread(img_path)
    if image is None : 
        print("No image")
        print(img_path)
    image_copy = image.copy()
    detected = False
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to filter out noise
    g_blur = cv2.GaussianBlur(gray,(5,5),0)
    
    # Apply Otsu's thresholding (automatically calculates a threshold value and binarizes image)
    ret3,otsu = cv2.threshold(g_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    # Invert the image (swap black and white)
    # Square will be detected better as a dark shape with a light outline
    image_binary = cv2.bitwise_not(otsu)

    # find contours
    (contours,hierarchy) = cv2.findContours(image_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print('Contours: ' , len(contours))
    
    # identify innermost square of min size (membrane) and identify corners
    min_size = 10
    x, y, w, h, image_rect = innermost_square(contours, hierarchy, image_copy, min_size)
 
    cv2.circle(image_rect, (x, y), 3 ,255, -1) # draw a dot on upper left corner
    cv2.circle(image_rect, (x+w, y+h), 3 ,255, -1) # draw a dot on lower right corner
    cv2.circle(image_rect, (x, y+h), 3 ,255, -1) # draw a dot on lower left corner
    cv2.circle(image_rect, (x+w, y), 3 ,255, -1) # draw a dot on upper right corner
    detected = True # TO DO: fix

    #result = cv2.imshow('result',image_rect)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    return x, y, w, h, detected


"""

    probe adjustment : detecs the probes and adjusts their placement

    Args:
        img_path: string -> path of a given image
    Returns:
        detected: boolean -> true if a square is found, false otherwise
        rightProbe: array -> probe coordinates
        leftProbe: array -> probe coordinates
    Raises:
        No errors. Assumes that all devices are operating correctly.
            
"""
def probe_detection(img_path):
    # initialize variables, read image
    detected = False
    image = cv2.imread(img_path)
    alpha = 2.5 
    beta = 30
    
    img = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    #Converts picture into grayscale and blurs it
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray,(5,5),0) 

    #Apply otsu threshold
    ret3,otsu = cv2.threshold(blur,35,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image_binary = cv2.bitwise_not(otsu)

    (contours,_) = cv2.findContours(image_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    count = 0
    
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt) #Calculates area of objects to disregard stray small shapes it finds
        
        if len(approx) == 3 and area > 1000:
            
            # Extract vertice of the triangle
            point1 = tuple(approx[0][0])
            point2 = tuple(approx[1][0])
            point3 = tuple(approx[2][0])

            verticesList = [point1,point2,point3]

            tipofProbe = None

            #need to find lowest x for right probe
            if count == 0: 
                # lowest_x_value = float('inf') 
                # for vertex in verticesList:
                #     x_value = vertex[0]  # Get x coordinate of the vertex
    
                #     # Compare x_value with highest_x_value found so far
                #     if x_value < lowest_x_value:
                #         lowest_x_value = x_value
                #         tipofProbe = vertex
                # rightProbe = tipofProbe
                lowest_y_value = float('inf')
                for vertex in verticesList:
                    y_value = vertex[1]
                    if y_value < lowest_y_value:
                        lowest_y_value = y_value
                        tipofProbe = vertex
                rightProbe = tipofProbe
            # need to find highest x for left probe
            else:
                 highest_x_value = -float('inf') 
                 for vertex in verticesList:
                    x_value = vertex[0]  # Get x coordinate of the vertex
    
                    # Compare x_value with highest_x_value found so far
                    if x_value > highest_x_value:
                        highest_x_value = x_value
                        tipofProbe = vertex
                 leftProbe = tipofProbe
            
            img = cv2.drawContours(image, [cnt], -1, (0,255,255), 2)

            cv2.circle(img, tipofProbe, 5, (0, 255, 0), -1)  # Green dot at point
            # cv2.circle(img, point1, 5, (255, 0, 0), -1)  # red dot at point
            # cv2.circle(img, point2, 5, (0, 255, 0), -1)  # Green dot at point
            # cv2.circle(img, point3, 5, (0, 0, 255), -1)  # blue dot at point
            
            M = cv2.moments(cnt)
            count += 1

    cv2.imshow('final',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    if count == 2:
        detected = True

    return detected,rightProbe,leftProbe



def coordsDiff(img_path):
    detected,rightProbe,leftProbe = probe_detection(img_path)
    square,bR,uL = square_detect(img_path)

    print("Upper Left Corner: ", uL)
    print("Bottom Right Corner: ",bR,"\n")

    print("Right Probe:",rightProbe)
    print("Left Probe:", leftProbe, "\n")
    
    leftX = abs(leftProbe[0]-uL[0])
    leftY = abs(leftProbe[1]-uL[1])
    rightX = abs(rightProbe[0]-bR[0])
    rightY = abs(rightProbe[1]-bR[1])

    print(f'Upper Left Difference: ({leftX},{leftY})')
    print(f'Bottom Right Difference: ({rightX},{rightY})')
    
    return leftX,leftY,rightX,rightY



def move_probes(x, y):
    dist = 250/2
    cap4_des = [x+dist+30, y-dist-30]
    cap1_des = [x-dist-30, y+dist+30]
    
    return cap4_des, cap1_des


"""
    calculate_corner_coords : calculate theoretical GDS coordinates for 3 corners of chip
        (does not take outer edges of chip into account)

    Args:
        num_mem: number of membranes in one row of chip
        street: distance in microns of street width (region between membranes)
        mem_size: membrane length in microns
    Returns:
        corners: list of tuples with 3 corners' x, y coordinates 

"""
def calculate_corner_coords(num_mem, street, mem_size): 
    chip_length = (mem_size * num_mem) + (street * (num_mem - 1))
    
    upper_left_corner = (0, chip_length)
    lower_left_corner = (0, 0)
    upper_right_corner = (chip_length, chip_length)
    lower_right_corner = (chip_length, 0)

    corners = [lower_left_corner, upper_left_corner, upper_right_corner]

    return corners


"""
    get_mem_coords : calculates theoretical GDS coordinates of membrane centers 

    Args:
        num_mem: number of membranes in one row of chip
        street: distance in microns of street width (region between membranes)
        mem_size: membrane length in microns        
    Returns:
        coord_list : list of tuples w/ x,y coordinates of membrane centers

"""
def get_mem_coords(num_mem, street, mem_size):
    period = mem_size + street # distance in microns between each membrane

    coord_list = []

    start_mem = ((mem_size / 2), (mem_size / 2)) # lowest and leftmost membrane
    
    prev_mem = start_mem
    y = prev_mem[1]

    # traverse chip in snake motion, calculate x,y coordinates for all membrane centers, append to coord_list
    for i in range(num_mem): # row
        for j in range(num_mem): # column
            if (i == 0 and j == 0): # first membrane of whole chip
                coord_list.append(start_mem)
                continue
            elif (j == 0): # first membrane of each row
                x = prev_mem[0] # x coord unchanged from membrane directly below it
            elif (i % 2 == 0): # even row
                x = prev_mem[0] + period # go right 
            else: # odd row 
                x = prev_mem[0] - period # go left
            
            curr_mem = (x, y)
            prev_mem = curr_mem
            coord_list.append(curr_mem)

        y = prev_mem[1] + period # increase y coord for each new row
        
    return coord_list


"""
    get_affine_transform : create a matrix for an Affine transform
        to convert between GDS and stage/device coordinates

    Args:
        src_points: 3x2 numpy array of source (GDS) coordinates (3 points, each with x and y coords)
        dst_points: 3x2 numpy array of device coordinates (3 points, each with x and y coords)
    Returns:
        T: 2x3 numpy array, represents Affine transformation matrix
    Raises:
        AssertionError if input shape is incorrect

"""
def get_affine_transform(src_points, dst_points):

    # Make sure the input shape is correct
    assert src_points.shape == (3, 2) and dst_points.shape == (3, 2)

    # Create matrix A
    A = np.array([
        [src_points[0, 0], src_points[0, 1], 1, 0, 0, 0],
        [0, 0, 0, src_points[0, 0], src_points[0, 1], 1],
        [src_points[1, 0], src_points[1, 1], 1, 0, 0, 0],
        [0, 0, 0, src_points[1, 0], src_points[1, 1], 1],
        [src_points[2, 0], src_points[2, 1], 1, 0, 0, 0],
        [0, 0, 0, src_points[2, 0], src_points[2, 1], 1],
    ])

    # Create matrix B
    B = dst_points.flatten()
    
    # Solve the linear system A * x = B
    x = np.linalg.solve(A, B)

    # Reshape
    T = np.array([
        [x[0], x[1], x[2]],
        [x[3], x[4], x[5]]
    ])

    return T


"""
    apply_affine_transform : accepts GDS coordinates and returns equivalent device coordinates

    Args:
        T: Affine transform matrix (2x3 numpy array)
        src_point: tuple with 2 elements -> x,y coordinates
    Returns:
        dst_point: numpy array with x,y device coordinates

"""
def apply_affine_transform(T, src_point):

    gds = np.array([src_point[0], src_point[1], 1])
    gds = gds.transpose()
    dst_point = np.matmul(T, gds)
    dst_point = dst_point.transpose()

    return dst_point


"""
    apply_affine_all_mems : convert GDS coords to device coords for all membranes on chip

    Args:
        T: Affine transform matrix (2x3 numpy array)
        src_points_list: list of tuples w/ x,y coordinates of membrane centers
        num_mem: number of membranes in one row of chip
    Returns:
        dst_points: (total_mem)x2 numpy array w/ x,y device coordinates 
        
"""
def apply_affine_all_mems(T, src_points_list, num_mem):
    total_mem = num_mem * num_mem # for uniform square chip
    dst_points = np.zeros((total_mem, 2)) # allocate numpy array of size total_mem-by-2, fill w/ zeros

    # convert each source point to destination point 
    for (index, point) in enumerate(src_points_list):
        dst_point = apply_affine_transform(T, point)
        dst_points[index] = dst_point
        
    return dst_points

"""
    crop_from_prediction: Crops a square region from an image centered at a predicted coordinate with a defined box size

    Args:
        image_path,
        center_x,
        center_y,
        box_size=300
    Returns:
        crop
        
"""

def crop_from_prediction(image_path, center_x, center_y, box_size=300):
    # load the image from the specified path
    image = cv2.imread(image_path)
    
    # calculate half the box size for cropping
    half = box_size // 2
    
    # get image dimensions
    h, w, _ = image.shape
    
    # calculate bounding box coordinates
    x1 = max(center_x - half, 0)
    x2 = min(center_x + half, w)
    y1 = max(center_y - half, 0)
    y2 = min(center_y + half, h)
    
    # crop the image based on the calculated coordinates
    crop = image[y1:y2, x1:x2]
    return crop

"""
    compute_affine_pixel_stage_transform: Computes the affine transformation matrix that maps stage coordinates to image pixel coordinates

    Args:
        stage_points
        image_points
    Returns:
        affine_matrix
        
"""
def compute_affine_pixel_stage_transform(stage_points, image_points):
    """
    stage_points: list of 3 (x, y) tuples in stage coords
    image_points: list of 3 (x, y) tuples in image pixel coords
    """
    # convert list of points to NumPy arrays
    src = np.array(stage_points, dtype=np.float32)
    dst = np.array(image_points, dtype=np.float32)

    # compute the affine transfomration matrix mapping stage coords to image coords
    affine_matrix = cv2.getAffineTransform(src, dst)

    return affine_matrix

"""
    predict_crop_pixel_from_affine: Applies an affine transformation to predict image pixel coordinates from a stage coordinate

    Args:
        stage_xy
        affine_matrix
    Returns:
        dst_points: 
        
"""
def predict_crop_pixel_from_affine(stage_xy, affine_matrix):
    # convert stage coordinate to homogeneous format
    src_pt = np.array([stage_xy[0], stage_xy[1], 1.0])
    
    # apply affine transformation to get pixel coordinates
    dst_pt = np.matmul(affine_matrix, src_pt)
    
    # return integer pixel coordinates
    return int(dst_pt[0]), int(dst_pt[1])

"""
    calibration_helper_affine: Collects user-selected image points and known stage coordinates to generate an affine transform for pixel-to-stage mapping

    Args:
        signatone
        dev_coor
    Returns:
       affine_matrix
        
"""
def calibration_helper_affine(signatone, dev_coor):
    # store stage coordinates
    stage_points = []
    
    # store corresponding image coordinates
    image_points = []
    
    # counter for saved images
    img_count = 0
    
    # get current z positions for CAP4 and CAP1
    signatone.set_device('CAP4')
    cap4_coor=signatone.get_cap()
    cap4_coor_list=cap4_coor.split(",")
         
    signatone.set_device('CAP1')
    cap1_coor=signatone.get_cap()
    cap1_coor_list=cap1_coor.split(",")
    
    # move thorugh three known stage points 
    for i, membrane_idx in enumerate([0, 1, len(dev_coor) // 9]):
        if i!=0:
            # raise probes before moving to new membrane
            signatone.move_probes_z(700)
            signatone.set_device('WAFER')
            signatone.move_abs(dev_coor[membrane_idx][0], dev_coor[membrane_idx][1])
            
            # move probes to prior z position + small offset
            signatone.set_device("CAP1")
            signatone.move_z(int(float(cap1_coor_list[2]))+10)
            signatone.set_device("CAP4")                
            signatone.move_z(int(float(cap4_coor_list[2]))+10)
        
        img_count += 1
 
        # take image and save it
        img_path = f"C:\\CM400\\photos\\FULL_membrane_{img_count}.bmp"
        _ = take_image(img_count)
        signatone.save_image(img_path)
        print(f"Saved FULL image: {img_path}")

        # setup click capture
        clicked_point = []

        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                print(f"Clicked at: X={x}, Y={y}")
                clicked_point.append((x, y))
                cv2.destroyAllWindows()

        # display image and capture click
        img = cv2.imread(img_path)
        cv2.imshow(f"FULL_membrane_{img_count}", img)
        cv2.setMouseCallback(f"FULL_membrane_{img_count}", click_event)

        print("\nClick on the membrane center in the image window.")
        cv2.waitKey(0)

        # ensure click was captured
        if not clicked_point:
            raise Exception("No click detected! Please click inside the image.")

        x, y = clicked_point[0]

        # append stage and image coordinates for calibration
        stage_points.append((dev_coor[membrane_idx][0], dev_coor[membrane_idx][1]))
        image_points.append((x, y))

    # compute affine matrix from the collected points
    affine_matrix = compute_affine_pixel_stage_transform(stage_points, image_points)

    print("\n--- Affine Calibration Matrix ---")
    print(affine_matrix)

    return affine_matrix


"""
    areaDetectColorRange: Calculates the percentage of an image area that falls within a specified HSV color range

    Args:
        img_path: str,
        lower_bound: tuple,
        upper_bound: tuple
    Returns:
       percent_match
        
"""
def areaDetectColorRange(img_path: str, lower_bound: tuple, upper_bound: tuple):
    # load image
    image = cv2.imread(img_path)
    
    # convert BGR image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # filter for a specific color range
    lower = np.array(lower_bound)
    upper = np.array(upper_bound)
    mask = cv2.inRange(hsv, lower, upper)
    
    # count how many pixels fall within the mask range
    match_pixels = np.count_nonzero(mask)
    total_pixels = mask.size
    
    # calculate the percentage of the image area that matches the target color
    percent_match = (match_pixels / total_pixels) * 100
    
    # show mask result to user
    cv2.imshow('Color Range Mask', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return int(percent_match)
    

"""
    get_z_heights: calculates z-coordinates for each membrane based on the probe heights
    Args:
        z_ll: int -> z-coordinate of lower-left corner of the probe
        z_ul: int -> z-coordinate of upper-left corner of the probe
        z_ur: int -> z-coordinate of upper-right corner of the probe
        dev_points: list of tuples -> (x, y) coordinates of the middle of each membrane
        dst_points: list of tuples -> (x, y) coordinates of the lower-left, upper-left, and upper-right corners of the grid
    Returns:
        z_heights: list of z-coordinates for each membrane

""" 
def get_z_heights( z_ll, z_ul, z_ur,dev_points, dst_points):

    z_values = np.array([z_ll, z_ul, z_ur])
    points_3d = np.column_stack((dst_points, z_values)) # combine (X,Y) coordonates with Z-coordinates
    z_heights = []
    v1 = points_3d[1] - points_3d[0]  # Vector from upper-left to lower-left
    v2 = points_3d[2] - points_3d[0]  # Vector from upper-right to upper-left
    # Calculate the normal vector to the plane defined by these three points
    normal = np.cross(v1, v2)
    A, B, C = normal # Coefficients of the plane equation 
    D = -np.dot(normal, points_3d[0]) 

    # Function to compute Z at any (x, y)
    def get_z(x, y):
        return -(A * x + B * y + D) / C
    
    for num in range(len(dev_points)):
        coor=get_z(dev_points[num][0], dev_points[num][1]) #calculate z-coordinates for each membrane center
        z_heights.append(coor)
    
    z_heights = np.array(z_heights)
    return z_heights


def detect_circles(img_path):
    # Read the image
    image = cv2.imread(img_path)
    if image is None:
        print("Image not found or path is incorrect.")
        return False
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(
        gray_blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=5,
        maxRadius=100
    )
    # Check if any circles were found
    if circles is not None and len(circles[0]) > 0:
        return True
    else:
        return False

"""
    run_water_pump: pumps water for 2 seconds to clear any bubbles

    Args:
       None
    Returns:
        None
        
"""
def run_water_pump():
    water_pump.pwm(183, 0.40)     # Set frequency and 40% power
    water_pump.set_enable(1)       # Start pump
    time.sleep(2)       # Pump for 2 seconds
    water_pump.set_enable(0)       # Stop pump
    time.sleep(2) # Wait for water suface to calm down