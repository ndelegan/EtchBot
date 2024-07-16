"""

    Helper functions that are used in the etching process within the 'etching.py' file.
    
    Each function was written by different students from the UIC Chicago Tech Circle Team:
        Take Image Author(s): Andrea Munoz
        Bubble Detect Author(s): Fernanda Villalpando
        Area Detect Author(s): Lisette Ruano
        Send Slack Message Author(s): Andrea Munoz
        Square Detect Author(s): Claudia Jimenez, Aima Qutbuddin, Lisette Ruano
        Innermost Square Author(s): Kyle Cheek, Claudia Jimenez
        
    Collaborator(s): Argonne National Laboratory (Nazar Delegan, Clayton Devault), Kyle Cheek
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
    
    take_image : takes an image and saves it in a certain file path
    
    Args:
        counter : integer
        filename : string
    Returns:
        filename : string -> file path of image
    Raises:
        None.
    Citations: 
        None.
    
"""
def take_image(counter,filename):
    string = " C:\\CM400\\photos\\imgCapture"
    string2 = ".bmp"
    filename = f'{string}{counter}{string2}'
    mini_str = "imgCapture"
    specified_filename = f'{mini_str}{counter}{string2}'
    return filename

"""
    
    delete_image : deletes an image from a given file path
    
    Args:
        counter : integer
        filename : string
    Returns:
        None.
    Raises:
        None.
    Citations: 
        None.
    
"""
def delete_image(counter, filename):
    string = " C:\\CM400\\photos\\imgCapture"
    string2 = ".bmp"
    
    while counter >= 0:
        filename = f'{string}{counter}{string2}'
        os.remove(filename)
        counter-=1
        

"""
    
    bubble_detect : detect bubbles in a given image
    
    Args:
        bubble_count : integer
        image_name : string
    Returns:
        bubble_count : integer -> hw many bubbles were found
    Raises:
        None.
    Citations: 
        None.
    
"""
def bubble_detect(bubble_count, image_name):
    #Image Path Declaration
    image_path = "C:\\Users\\AdminUser\\Downloads" + image_name
    # image_path = os.path.join(path_root, 'Downloads', filename)
    img = cv2.imread(image_path)
    #converting image to grayscale
    img_gray  = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #Blurring the image for image processing
    img_blur = cv2.blur(img_gray, (25,5))
    #detects circles
    detected_circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, .1, 100, param1 = 27, param2 = 31, minRadius=0, maxRadius=300)
    #counts the amount of circles in the list
    len(detected_circles)
    detected_circles
    #used for drawing circles
    np.uint16(np.around(detected_circles))
    
    #draws image. this section if/for loop is not necessary for automation and can be cmmmented out
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0 , :]:
            a,b,r = pt[0],pt[1],pt[2]
            cv2.circle(img, (a,b), r, (0,255,0), 2)
            cv2.circle(img, (a,b), 1, (0,0,255), 3)
            
    bubble_count = 0
    for c in detected_circles[0, :]:
        #draws the outer green circle to show what bubble is detected.
        #you can comment out both cv2.circle commands.
        cv2.circle(img, (c[0], c[1]), c[2], (0, 255, 0), 3)
        #draws the inner red dot in the center of the detected circle.
        cv2.circle(img, (c[0], c[1]), 1, (0, 0, 255), 5)
        bubble_count += 1
    return bubble_count


"""
    
    area_detect : detects the percentage of the square given
    
    Args:
        None.
    Returns:
        whole_number_percentage : integer -> percentge of area not etched
    Raises:
        None.
    Citations: 
        None.
    
"""
def area_detect(imagePath):
   #Read in image location
    image = cv2.imread(imagePath)
    # img = np.zeros(image.shape, image.dtype)
    # alpha = 2.0
    # beta = 30
    # img = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    #Converts image to gray scale and blurs it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    
    #Sharpens the blurred image
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
    
    #Setting color threshold and cleaning up noise in the picture
    thresh = cv2.threshold(blur, 148, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    black_threshold = 50

    #Counting black pixels and total pixels
    black_pixels = np.count_nonzero(close < black_threshold)
    total_pixels = close.size

    #Calculates percentage of black pixels then shows altered pictures
    percentage_black = (black_pixels / total_pixels) * 100
    whole_number_percentage = int(percentage_black)

    return whole_number_percentage


"""
    
    send_slack_message : sends a slack message to a certain slack channel
    
    Args:
        webhook_url : string
        message : string
    Returns:
        None.
    Raises:
        None.
    Citations: 
        None.
    
"""
def send_slack_message(webhook_url, message):
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
        contours : list of list of points that make up a contour (returned by findContours()) 
        hierarchy : list of indices of contours passed in hierarchical order (returned by findContours()) 
        image : image object to draw rectangle on
        min_size : minimum edge length of square to detect
    Returns:
        x1 : x-coordinate of top left corner of square of interest
        y1 : y-coordinate of top left corner of square of interest
        w1 : width of square of interest
        h1 : height of square of interest
        image : image with rectangle drawn on
    Raises:
        None.
    
"""
def innermost_square(contours, hierarchy, image, min_size):

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

    square_detect : square detection of membrane of interest

    Args:
        image : string
    Returns:
        detected : boolean -> true if a square is found, false otherwise
        result : copy of original image with detected squares superimposed (also displayed on screen) # may change later
    Raises:
        No errors. Assumes that all devices are operating correctly.
            
"""
def square_detect(image): 
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
    (contours,_) = cv2.findContours(image_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    print('Contours: ' , len(contours))
    
    #draw and show detected squares
    arg1 = 10
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        if h > arg1 and w > arg1:
            cv2.rectangle(image_copy, (x,y), (x+w,y+h),(0,255,0), 2)
            cv2.circle(image_copy, (x, y), 3 ,255, -1) # put a dot on upper left corner
            cv2.circle(image_copy, (x+w, y+h), 3 ,255, -1) # put a dot on lower right corner
            detected = True

    result = cv2.imshow('result',image_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return detected, result


"""

    probe adjustment : detecs the probes and adjusts their placement

    Args:
        imagePath : string
    Returns:
        detected : boolean -> true if a square is found, false otherwise
        rightProbe : array -> probe coordinates
        leftProbe : array -> probe coordinates
    Raises:
        No errors. Assumes that all devices are operating correctly.
            
"""
def probe_adjustment(imagePath):
    detected = False
    
    image = cv2.imread(imagePath)
   
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
    
