import cv2
import numpy as np
import time





#GIVEN: Boat center, bounding box, webcam video feed

#GOAL: Compute next center. Increase bounding box with time. Send coordinates of said center, look at new center.append

#SECONDARY GOAL: Create "standard deviation" i.e. difference between centers of boat and center of image. as that standard deviation grows,
#request a new neural net update

#"Constant moving average"

    

cap = cv2.VideoCapture('vid.avi')

#center of image param
center = [360,640]

#Ideally these parameters would be dynamically adjusted based on the neural net initial grab, and then based on the bounding box size.
#Width and height params
x = 270
y = 480


while(True):
    
    ret, frame = cap.read()
    height, width, channels = frame.shape
    subFrame = frame[max(0,center[0]-270):min(720,center[0]+270), max(0,center[1]-480):min(1280,center[1]+480)]
    #subFrame = frame[max(0,center[0]-270):min(720,center[0]+270), max(0,center[1]-480):min(1280,center[1]+480)]
    kernel = np.ones((5,5),np.uint8)

    eroFrame = cv2.erode(subFrame,kernel,iterations = 1)
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

    
    length = 0
    biggestContour = None
    for cont in contours:
        if (len(cont) > 6):
            e = cv2.fitEllipse(cont)
            a = e[1][0]
            b = e[1][1]
            
            if (b/a < 5):
                if cv2.arcLength(cont, False) > length:
                    biggestContour = cont
                    length = cv2.arcLength(cont,False)
        
    #cv2.drawContours(subFrame, biggestContour, -1, (0,255,0),3)
                 

    M = cv2.moments(biggestContour)
    try:
        cv2.ellipse(subFrame,cv2.fitEllipse(biggestContour),(255,0,255),4)  
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        center[1] = (center[1]+cX)/2
        center[0] = (center[0]+cY)/2
    except:
        print ("null")
    if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cv2.rectangle(subFrame, (0,0),(960,480),(0,255,255),thickness=4)
    cv2.imshow('frame',frame)

        
cap.release()
cv2.destroyAllWindows()
