"""

    Helper functions that are used in the etching process within the 'etching.py' file.
    
    Each function was written by different students from the UIC Chicago Tech Circle Team:
        Take Image Author(s): Andrea Munoz
        Bubble Detect Author(s): Fernanda Villalpando
        Area Detect Author(s): Lisette Ruano
        Send Slack Message Author(s): Andrea Munoz
        Square Detect Author(s): Claudia Jimenez, Aima Qutbuddin, Lisette Ruano
        
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
    
    take_image : 
    
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
def take_image(counter,filename):
    string = " C:\\CM400\\photos\\imgCapture"
    string2 = ".bmp"
    filename = f'{string}{counter}{string2}'
    mini_str = "imgCapture"
    specified_filename = f'{mini_str}{counter}{string2}'
    return specified_filename


"""
    
    bubble_detect : 
    
    Args:
        bubble_count : integer
        image_name : string
    Returns:
        None.
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
    
    area_detect : 
    
    Args:
        None.
    Returns:
        None.
    Raises:
        None.
    Citations: 
        None.
    
"""
def area_detect():
    pass


"""
    
    send_slack_message : 
    
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

    square_detect : square detection of membrane of interest

    Args:
        image : string
    Returns:
        detected : boolean -> true if a square is found, false otherwise
        result : copy of original image with detected squares superimposed (also displayed on screen) # may change later
    Raises:
        No errors. Assumes that all devices are operating correctly.
    Citations: 
        https://stackoverflow.com/questions/55169645/square-detection-in-image,
        https://www.tutorialspoint.com/how-to-detect-a-rectangle-and-square-in-an-image-using-opencv-python, 
        https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_thresholding/
            py_thresholding.html#otsus-binarization
            
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
            detected = True

    result = cv2.imshow('result',image_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return detected, result
