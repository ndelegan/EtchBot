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
        Get Affine Transformation Author(s): Clayton DeVault
        Apply Affine Transformation Author(s): Claudia Jimenez
        
    Commenting/Code Structure was implemented by Lisset Rico.
        
    Collaborator(s): Argonne National Laboratory (Nazar Delegan, Clayton DeVault), Break Through Tech (Kyle Cheek)
    Date Created: 06/26/2024

"""

import time
import cv2
import requests
import json
import os
import random
import numpy as np


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
def crop_image(start_x, start_y, new_w, new_h, pixel_w, pixel_h, img_path, crop_img_name, crop_img_path):
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

    thresh = cv2.threshold(sharpen, 155, 255, cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    close = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, kernel, iterations=2)
    black_threshold = 50

    
    # Counting black pixels and total pixels
    black_pixels = np.count_nonzero(close < black_threshold)
    
    total_pixels = close.size

    # Calculates percentage of black pixels then shows altered pictures
    percentage_green = (black_pixels / total_pixels) * 100
    whole_number_percentage = int(percentage_green)
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
    TO DO: add more comments, clean up busy logic lines
    
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

    # result = cv2.imshow('result',image_rect)
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
def probe_adjustment(img_path):
    detected = False
    
    image = cv2.imread(img_path)
   
    #Converts picture into grayscale and blurs it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray,(5,5),0) 

    #Apply otsu threshold
    ret3,otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image_binary = cv2.bitwise_not(otsu)

    
    (contours,_) = cv2.findContours(image_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    count = 0
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt) #Calculates area of objects to disregard stray small shapes it finds
        
        if len(approx) == 3 and area > 400:
            
            # Extract vertice of the triangle
            if count == 0:
                rightProbe = tuple(approx[1][0])
            else:
                leftProbe = tuple(approx[1][0])
            
            img = cv2.drawContours(image, [cnt], -1, (0,255,255), 3)
            
            # cv2.circle(image, point, 5, (0, 255, 0), -1)  # Green dot at point
            
            M = cv2.moments(cnt)

            count+=1
            combined_string = str(count)
            
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])
                cv2.putText(img, combined_string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    if count == 2:
        detected = True

    return detected,rightProbe,leftProbe


"""
    calculate_corner_coords : calculate theoretical GDS coordinates for 3 corners of chip

    Args:
        num_mem : number of membranes in one row of chip
        outer_edge : distance in microns from outer edge of chip to membrane side
        street : distance in microns of street width (region between membranes)
        mem_size : membrane length in microns
    Returns:
        corners : list of tuples with 3 corners' x, y coordinates 

"""

def calculate_corner_coords(num_mem, outer_edge, street, mem_size): 
    chip_length = (mem_size * num_mem) + (street * (num_mem - 1)) + (outer_edge * 2)
    
    upper_left_corner = (0, chip_length)
    lower_left_corner = (0, 0)
    upper_right_corner = (chip_length, chip_length)
    lower_right_corner = (chip_length, 0)

    corners = [lower_left_corner, upper_left_corner, upper_right_corner]

    return corners

"""
    get_mem_coords : calculates theoretical GDS coordinates of membrane centers 

    Args:
        num_mem : number of membranes in one row of chip
        outer_edge : distance in microns from outer edge of chip to membrane side
        street : distance in microns of street width (region between membranes)
        mem_size : membrane length in microns        
    Returns:
        coord_list : list of tuples w/ x,y coordinates of membrane centers

"""

def get_mem_coords(num_mem, outer_edge, street, mem_size):
    period = mem_size + street # distance in microns between each membrane

    coord_list = []

    start_mem = (outer_edge + (mem_size / 2), outer_edge + (mem_size / 2)) # lowest and leftmost membrane
    
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
        src_points : 3x2 numpy array of source (GDS) coordinates (3 points, each with x and y coords)
        dst_points : 3x2 numpy array of device coordinates (3 points, each with x and y coords)
    Returns:
        T : 2x3 numpy array, represents Affine transformation matrix

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
        T : Affine transform matrix (2x3 numpy array)
        src_point : tuple with 2 elements -> x,y coordinates
    Returns:
        dst_point: numpy array with x,y device coordinates

"""

def apply_affine_transform(T, src_point):

    gds = np.array([src_point[0], src_point[1], 1])
    gds = gds.transpose()
    dst_point = np.matmul(T, gds)
    dst_point = dst_point.transpose()

    return dst_point
