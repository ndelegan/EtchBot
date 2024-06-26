import time
import cv2
import requests
import json
import os
import random
import numpy as np


# Function to execute image function for signatone
def take_image(counter,filename):
    string = " C:\\CM400\\photos\\imgCapture"
    string2 = ".bmp"
    filename = f'{string}{counter}{string2}'
    mini_str = "imgCapture"
    specified_filename = f'{mini_str}{counter}{string2}'
    return specified_filename


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


def area_detect():
    pass


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