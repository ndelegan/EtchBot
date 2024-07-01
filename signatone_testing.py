import signatone_driver as Signatone
import cv2

signatone = Signatone.Signatone()
position = 0,0,0
set_device = signatone.set_device("CAP1")
get_capposition = signatone.get_cap()
print(get_capposition)
img = cv2.imread('C:\\CM400\\photos\\imgCapture1.bmp')
print(img.shape)
detected = False
    
# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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
        cv2.rectangle(img, (x,y), (x+w,y+h),(0,255,0), 2)
        cv2.circle(img, (x, y), 3 ,255, -1) # put a dot on upper left corner
        cv2.circle(img, (x+w, y+h), 3 ,255, -1) # put a dot on lower right corner
        detected = True

result = cv2.imshow('result',img)
cv2.waitKey(0)
cv2.destroyAllWindows()