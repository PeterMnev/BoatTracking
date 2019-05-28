import cv2
import numpy as np
import time


start_time = time.time()


#GIVEN: Boat center, bounding box, webcam video feed

#GOAL: Compute next center. Increase bounding box with time.



###Preparation of image
##im = cv2.imread('boatProcked.jpeg')
##imgr = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
##imgray = cv2.medianBlur(imgr,15)
##
###Regular detection
##ret,thresh = cv2.threshold(imgray, 127,255, 0)
##im2, contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
##
##
##cv2.drawContours(im, contours, -1, (0,255,0),3)
##
##print("--- %s seconds ---" % (time.time() - start_time))
##
##cv2.imwrite("BoatSmoothed.jpeg", imgray)
##cv2.imwrite("BoatContoursAlt.jpg",im)


cap = cv2.VideoCapture('vid.avi')

time.sleep(2)






while(True):
    ret, frame = cap.read()
    kernel = np.ones((5,5),np.uint8)
    frame = cv2.erode(frame,kernel,iterations = 1)

    greyFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    greyFrame = cv2.medianBlur(greyFrame,27)

    #Adaptive Thresholding
    v = np.median(greyFrame)
    sigma = .4
    lower = int(max(0,(1.0-sigma)*v))
    upper = int (min(255, (1.0-sigma)*v))

    #Canny detection
    edged = cv2.Canny(greyFrame, lower, upper)
    #ret,edged = cv2.threshold(greyFrame, 200,255, 0)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    

    area = 0
    biggestContour = []
    for cont in contours:
        if cv2.contourArea(cont) > area:
            biggestContour = cont
    cv2.drawContours(edged, biggestContour, -1, (0,255,0),3)
    cv2.imshow('frame',edged)
    if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
