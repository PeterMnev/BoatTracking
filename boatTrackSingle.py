import cv2
import numpy as np
import time

start_time = time.time()

frame = im = cv2.imread('HTASub.png')
#subFrame = frame[max(0,center[0]-270):min(720,center[0]+270), max(0,center[1]-480):min(1280,center[1]+480)]
#subFrame = frame[max(0,center[0]-270):min(720,center[0]+270), max(0,center[1]-480):min(1280,center[1]+480)]
kernel = np.ones((5,5),np.uint8)

eroFrame = cv2.erode(frame,kernel,iterations = 1)
eroFrame = cv2.medianBlur(eroFrame,5)
greyFrame = cv2.cvtColor(eroFrame,cv2.COLOR_BGR2GRAY)
greyFrame = cv2.medianBlur(greyFrame,5)

#Adaptive Thresholding
v = np.median(greyFrame)
sigma = .07
lower = int(max(0,(1.0-sigma)*v))
upper = int(min(255, (1.0-sigma)*v))
#print (lower, upper)
#Canny detection
edged = cv2.Canny(greyFrame, lower/2, upper/2)
#ret,edged = cv2.threshold(greyFrame, 200,255, 0)
#Dilation improves detection, usually.
kernel = np.ones((3,3),np.uint8)

dilaFrame = cv2.dilate(edged,kernel,iterations = 1)
dilaFrame = cv2.morphologyEx(dilaFrame, cv2.MORPH_GRADIENT, kernel)
im2, contours, hierarchy = cv2.findContours(dilaFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

print("--- %s seconds ---" % (time.time() - start_time))    

length = 0
biggestContour = None

for cont in contours:
    if (len(cont) >= 5):
        e = cv2.fitEllipse(cont)
        a = e[1][0]
        b = e[1][1]
        
        if (b/a < 4):
            if cv2.arcLength(cont, False) > length:
                biggestContour = cont
                length = cv2.arcLength(cont,False)
        #cv2.ellipse(frame,e,(255,0,255),4) 
                
    
#cv2.drawContours(subFrame, biggestContour, -1, (0,255,0),3)
             

M = cv2.moments(biggestContour)
try:
    cv2.ellipse(frame,cv2.fitEllipse(biggestContour),(255,0,255),4)  
except:
    print ("null")

cv2.imwrite("boatProcked.jpeg", frame)


