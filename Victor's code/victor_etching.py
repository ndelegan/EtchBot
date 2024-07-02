#turn this code into a draw_rectangle function



import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import re


#user inputs
cushionRight = 10
cushionLeft = 10
cushionTop = 0
cushionBottom = 0

added_cushionRight =0
added_cushionLeft = 0
added_cushionTop = 0
added_cushionBottom = 0


#inputs
xmin = 0
xmax = 1600
ymin = 0
ymax = 1000




plt.rcParams['figure.dpi'] = 500
plt.rcParams['savefig.dpi'] = 500
plt.rcParams.update({'figure.autolayout': True})


def process_first(image):
    roi_contour_within = None
    
    # Define a threshold to identify near-black colors
    lower_black = np.array([0, 0, 0], dtype="uint8")
    upper_black = np.array([100, 100, 100], dtype="uint8")
    
    image = cv.imread(image)
    bb = cv.bilateralFilter(image, 50, 50, 50)
    bb = image
    gray = cv.cvtColor(bb, cv.COLOR_BGR2GRAY)
    # Create a mask to only select the near-black colors
    mask = cv.inRange(image, lower_black, upper_black)

    # Find contours in the mask
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Sort contours based on the area and assume the largest ones are the electrodes
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    # Center of the image
    image_center = np.array([image.shape[1]//2, image.shape[0]//2])

    # Find contours that can be approximated as triangles
    triangle_contours = []
    for cnt in contours:
        epsilon = 0.05 * cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, epsilon, True)
        if len(approx) == 3:
            triangle_contours.append(cnt)
    # Using the points of each triangle that are closest to the center of the image
    closest_points = []
    for cnt in triangle_contours:
        distances = [np.linalg.norm(image_center - pt[0]) for pt in cnt]
        closest_point_index = np.argmin(distances)
        closest_points.append(tuple(cnt[closest_point_index][0]))

    # If we have at least two points, define and expand a rectangle
    if len(closest_points) >= 2:
        if closest_points[0][0] < closest_points[1][0]:
            upper_left = closest_points[0]
            bottom_right = closest_points[1]
        if closest_points[1][0] < closest_points[0][0]:
            upper_left = closest_points[1]
            bottom_right = closest_points[0]
        
        # Expand the rectangle by 100 pixels in both x and y
        upper_left = (max(upper_left[0] - cushionLeft, 0), max(upper_left[1] - cushionTop, 0))
        bottom_right = (min(bottom_right[0] + cushionRight, gray.shape[1]), min(bottom_right[1] + cushionBottom, gray.shape[0]))

        # Draw the expanded rectangle
        first_image_processed = cv.rectangle(image, upper_left, bottom_right, (255, 255, 0), 2)

        # Crop the region for ROI detection
        roi_region = gray[upper_left[1]:bottom_right[1], upper_left[0]:bottom_right[0]]

        # Apply Gaussian blur to the ROI region
#         roi_blurred = cv.GaussianBlur(roi_region, (21, 31), 0)

        # Apply adaptive mean thresholding to the gray ROI region
    
        roi_thresh = cv.adaptiveThreshold(roi_region, 255, cv.ADAPTIVE_THRESH_MEAN_C, 
                                          cv.THRESH_BINARY_INV, 15, 2)

        # Find contours in the thresholded ROI region
        roi_contours, _ = cv.findContours(roi_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Assuming ROI is the largest contour in the region
        if roi_contours:
            roi_contour = max(roi_contours, key=cv.contourArea)
            
            
            epsilon = 0.05 * cv.arcLength(roi_contour, True)
            roi_contour = cv.approxPolyDP(roi_contour, epsilon, True)

            
            # Offset contour coordinates based on crop

            roi_contour = roi_contour + np.array([upper_left[0], upper_left[1]])
            cv.drawContours(first_image_processed, [roi_contour], -1, (0, 255, 0), 2)
            
            # Find vertices for smaller rectangle
            leftmost_point = tuple(roi_contour[roi_contour[:, :, 0].argmin()][0])
            highest_point = tuple(roi_contour[roi_contour[:, :, 1].argmin()][0])
            rightmost_point = tuple(roi_contour[roi_contour[:,:,0].argmax()][0])
            lowest_point = tuple(roi_contour[roi_contour[:,:,1].argmax()][0])
            
            # Define a point based on the left-most and highest points

            box_upper_left = (leftmost_point[0]-added_cushionLeft, highest_point[1]-added_cushionTop)
            box_bottom_right = (rightmost_point[0]+added_cushionRight, lowest_point[1]+added_cushionBottom)


#             cv.drawContours(image, [roi_contour], -1, (0, 255, 0), 2)
    if len(closest_points) < 2:
        print("Error finding electrodes")
        

        
    
    return first_image_processed, roi_region, upper_left, bottom_right, box_upper_left, box_bottom_right, leftmost_point, highest_point, closest_points
    

points_outside_contour = []
points_outside_contour = np.array(points_outside_contour)
def process_image(image, upper_left, bottom_right, box_upper_left, box_bottom_right, recent_roi_areas, leftmost_point, highest_point, points_outside_contour, previous_contour, skip, index):

    #     print("last contour area is " + str(last_contour_area))
    image = cv.imread(image)
#     image = image[ymin:ymax, xmin:xmax]
    
    imageCopy = image.copy()
    
    # Draw ROI rectangle
    cv.rectangle(image, upper_left, bottom_right, (255, 255, 0), 2)

    # Crop the region for ROI detection using the rectangle coordinates
    roi_region = image[upper_left[1]:bottom_right[1], upper_left[0]:bottom_right[0]]
#     roi_blurred = cv.GaussianBlur(roi_region, (21, 21), 0)
    

    
    height, width, channel = roi_region.shape
    for x in range(width):
        for y in range(height):
            
            # Get RGBA values of the current pixel
            blue = roi_region[y, x, 0]
            green = roi_region[y, x, 1]
            red = roi_region[y, x, 2]
            
                                
            blue = blue.astype(float)
            green = green.astype(float)
            red = red.astype(float)
            
#             for j in points_outside_contour:
#                 if (x, y) == j:
#                     roi_region[y, x, 0] = 255
#                     roi_region[y, x, 1] = 255
#                     roi_region[y, x, 2] = 255

            
            # Set the blue component to 100 if originally less than 121
            if blue < 105:
                roi_region[y, x, 0] = 0
                roi_region[y, x, 1] = 0
                roi_region[y, x, 2] = 0
                
            if blue > 250:
                roi_region[y, x, 0] = 0
                roi_region[y, x, 1] = 0
                roi_region[y, x, 2] = 0 
                
            
#            # bleaching out of bounds
            if x < leftbound:
                roi_region[y, x, 0] = 255
                roi_region[y, x, 1] = 255
                roi_region[y, x, 2] = 255
                
            if y < topbound:
                roi_region[y, x, 0] = 255
                roi_region[y, x, 1] = 255
                roi_region[y, x, 2] = 255

            total = blue + green + red
            
    if index > 1:
        # Extract x and y coordinates using NumPy
        points_outside_contour = np.array(points_outside_contour)
        x_coords = points_outside_contour[:, 0]
        y_coords = points_outside_contour[:, 1]

        # Create a mask to identify pixels outside the contour
        mask = np.zeros_like(roi_region, dtype=bool)
        mask[y_coords, x_coords, :] = True


        # Set values of pixels outside the contour to white (255, 255, 255)
        roi_region[mask] = 255

#                     # Convert back to uint8 if needed
#                     roi_region = roi_region.astype(np.uint8)



            # bleaching by color (bad for bubbles and not reliable)
#             if total < 320:
#                 roi_region[y, x, 0] = 255
#                 roi_region[y, x, 1] = 255
#                 roi_region[y, x, 2] = 255 
            
#             if total > 360:
#                 roi_region[y, x, 0] = 255
#                 roi_region[y, x, 1] = 255
#                 roi_region[y, x, 2] = 255 


    # Apply bilateral blurring to the image
    gray = roi_region
    gray = cv.bilateralFilter(gray, 20, 75, 75)
    gray = cv.GaussianBlur(gray, (41, 41), 0)
    gray = cv.cvtColor(gray, cv.COLOR_BGR2GRAY)

    
    
#     gray = cv.bilateralFilter(gray, 20, 100, 100)
    
    plt.imshow(cv.cvtColor(gray, cv.COLOR_BGR2RGB))
    plt.show()
    plt.axis('off')
    
    roi_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, 
                                          cv.THRESH_BINARY_INV, 11, 2)
    
    roi_contours, _ = cv.findContours(roi_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Assuming ROI is the largest contour in the region
    if roi_contours:
        roi_contour_prelim = max(roi_contours, key=cv.contourArea)

                    
        epsilon = 0.0001 * cv.arcLength(roi_contour_prelim, True)
        roi_contour_prelim = cv.approxPolyDP(roi_contour_prelim, epsilon, True)
        
        current_roi_area = cv.contourArea(roi_contour_prelim)
        all_areas.append(current_roi_area)

        # Compare ROI area with previous images
        if current_roi_area > np.mean(recent_roi_areas) * 1.1:
            print("Image has larger-than-expected area")
            skip = True

        if index > 1:
            if current_roi_area < np.mean(recent_roi_areas)*0.7:
                print("Image has smaller-than-expected area")
                skip = True

        if skip == True:
            last_contour_area = 0
            return imageCopy, previous_contour, points_outside_contour, skip


        roi_contour = roi_contour_prelim
        recent_roi_areas.append(current_roi_area)
        if len(recent_roi_areas) > 10:
            recent_roi_areas.pop(0)

        roi_contour_within = roi_contour

        roi_contour = roi_contour + np.array([upper_left[0], upper_left[1]])
        cv.drawContours(imageCopy, [roi_contour], -1, (0, 255, 0), 2)

        last_contour_area = current_roi_area

   

    # Identify points outside the contour
    
    
    
    
#     # Create a binary mask for the contour (inside will be True, outside will be False)
#     roi_region = 
#     mask_contour = np.zeros_like(roi_region, dtype=bool)
#     cv.drawContours(mask_contour, [roi_contour.astype(int)], 0, (1, 1, 1), thickness=cv.FILLED)

#     # Identify pixels outside the contour
#     rows_outside, cols_outside, _ = np.where(~mask_contour)
#     points_outside_contour = roi_region[rows_outside, cols_outside]

    
#     print(roi_contour_within)


    if index > 0:
        points_outside_contour = points_outside_contour.tolist()
        for y in range(height):
            for x in range(width):
                
                outside_last_contour = False
                distance_to_contour = cv.pointPolygonTest(roi_contour_within, (x, y), True)
                if distance_to_contour < -2:
                    outside_last_contour = True

                if outside_last_contour == True:
                    point_outside_contour = (x, y)
                    points_outside_contour.append(point_outside_contour)

    points_outside_contour = np.array(points_outside_contour)
        
    return imageCopy, roi_contour, points_outside_contour, skip


#user inputs
image_folder_path = input("Enter the path to the image folder: ")
first_image_index = int(input("Enter the index of the first image: "))
last_image_index = int(input("Enter the index of the last image: "))


image_files = [f for f in os.listdir(image_folder_path) if f.endswith('.jpg')]

# image_files = sorted(image_files, key=lambda x: int(x.split('.')[0]))

# Define a sorting function
def extract_number_from_filename(image_files):
    match = re.search(r'-(\d+)\.', image_files)
    return int(match.group(1)) if match else float('inf')
# Sort the filenames based on the numeric part
image_files = sorted(image_files, key=extract_number_from_filename)



#first image
first_image_path = os.path.join(image_folder_path, image_files[first_image_index-1])
print(first_image_path)
first_image_processed, roi_region, upper_left, bottom_right, box_upper_left, box_bottom_right, leftmost_point, highest_point, closest_points = process_first(first_image_path)





# List to store the areas of the ROI contours from the last 5 images
recent_roi_areas = []
all_areas = []
points_outside_contour = []
points_outside_contour = np.array(points_outside_contour)

# counter1 = 0
# counter2 = 0
leftbound = leftmost_point[0] - upper_left[0] + 5
topbound = highest_point[1] - upper_left[1] + 5


for i, file_name in enumerate(image_files[first_image_index - 1:last_image_index], start=first_image_index - 1):
    index = i
    image_path = os.path.join(image_folder_path, file_name)
    print(file_name)
    previous_contour=[]
    skip = False
    processed_image, roi_contour,points_outside_contour, skip = process_image(image_path, upper_left, bottom_right, box_upper_left, box_bottom_right, recent_roi_areas, leftmost_point, highest_point, points_outside_contour, previous_contour, skip, i)

#     if roi_countour:

#         if tuple(roi_contour[roi_contour[:, :, 0].argmin()][0])[0] > leftbound + 8:
#             counter1 += 1
#         if tuple(roi_contour[roi_contour[:, :, 1].argmin()][0])[1] > topbound + 8:
#             counter2 += 1

#         if counter1 == 5:
#             leftbound += 2
#             counter1 = 0

#         if counter2 == 5:
#             topbound += 2
#             counter2 = 0
    
    if skip == True:
        print(f"Skipped image {i} due to ROI area inconsistency.")
        continue

    # Print out the ROI area
    if skip == False:
        print(f"ROI area in image {i}: {cv.contourArea(roi_contour)}")

    # Draw the rectangle and contour on the image
#     triangle_contours=find_roi_rectangle(image_path)[2]
#     print(triangle_contours)
    closest_points = closest_points[0:2]
    for cp in closest_points:
            cv.circle(processed_image, cp,  20, (0, 255, 0), 5)
    cv.drawContours(processed_image, [roi_contour], -1, (255, 0, 0), 2)
#     cv.drawContours(processed_image, [triangle_contours], -1, (255, 0, 0), 2)
    cv.rectangle(processed_image, upper_left, bottom_right, (255, 0, 0), 2)

    # Display the image with ROI
    plt.figure(figsize=(4,3))
    plt.imshow(cv.cvtColor(processed_image, cv.COLOR_BGR2RGB))
    plt.title(f"Frame {i+1}", fontsize=15)
    plt.xticks([]), plt.yticks([])
    plt.show()
    
    previous_contour=roi_contour

    
    


# Load the image
# image_path = '/Users/victortyne/Box/Etch_Images/20211213_Xinghan/transfer2-9.jpg'
# image = cv.imread(image_path) =
# gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)


### this is for plotting the remaining area. Fitting the result to a line can give the etch rate


fig, ax = plt.subplots(figsize=(8,5))


all_areas = all_areas[0:106]
num = range(len(all_areas))
ax.scatter(num, all_areas, s=7)



ax.set_xlabel('Frame', fontsize=20)
ax.set_ylabel('Contour Area (pixels)', fontsize=20)
