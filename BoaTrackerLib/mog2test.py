 #my algorithm
import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
cap = cv2.VideoCapture('vid.avi')
box_size =5
kernel = np.ones((3,3),np.uint8)
while(1):
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame_gray = frame_gray.astype(float)
    mean_1 = cv2.blur(frame_gray,(box_size,box_size))
    mean_2 = cv2.blur(np.multiply(frame_gray,frame_gray),(box_size,box_size))
    std_image = np.multiply(mean_1,mean_1) - mean_2

    normalized_std_image = cv2.normalize(std_image,None,255,0,cv2.NORM_MINMAX,cv2.CV_8UC1)
    normalized_std_image = cv2.bitwise_not(normalized_std_image)
    #cv2.namedWindow('std_image',cv2.WINDOW_AUTOSIZE)
    #normalized_std_image = cv2.erode(normalized_std_image, kernel, iterations = 1)
    
    
    
    cv2.imshow('std_image',normalized_std_image)
    

    #color = 'b'
    #histr = cv2.calcHist([frame],[0],None,[256],[0,256])
    #plt.plot(histr,color = color)
    #plt.xlim([0,256])
    #plt.show()

    #720y 1280x
    ##    lower =(0, 0, 0) # lower bound for each channel
    ##    upper = (254, 100,100) # upper bound for each channel
    ##
    ##    # create the mask and use it to change the colors
    ##    mask = cv2.inRange(frame, lower, upper)
    ##    frame[mask != 0] = [0,0,0]

     
    cv2.imshow('frame',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()


#mog 2 modified
##import numpy as np
##import cv2 as cv
##cap = cv.VideoCapture('vid.avi')
##fgbg = cv.createBackgroundSubtractorMOG2(history = 200, varThreshold = 64, detectShadows = False)
##while(1):
##    ret, frame = cap.read()
##    fgmask = fgbg.apply(frame)
##    cv.imshow('frame',fgmask)
##    k = cv.waitKey(30) & 0xff
##    if k == 27:
##        break
##cap.release()
##cv.destroyAllWindows()




##import numpy as np
##import cv2 as cv
##cap = cv.VideoCapture('vid.avi')
##fgbg = cv.bgsegm.createBackgroundSubtractorMOG(100,5,0.6,0)
##while(1):
##    ret, frame = cap.read()
##    fgmask = fgbg.apply(frame)
##    cv.imshow('frame',fgmask)
##    k = cv.waitKey(30) & 0xff
##    if k == 27:
##        break
##cap.release()
##cv.destroyAllWindows()
