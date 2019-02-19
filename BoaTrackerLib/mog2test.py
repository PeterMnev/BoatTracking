import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
cap = cv2.VideoCapture('vid.avi')
while(1):
    ret, frame = cap.read()


    #color = 'b'
    #histr = cv2.calcHist([frame],[0],None,[256],[0,256])
    #plt.plot(histr,color = color)
    #plt.xlim([0,256])
    #plt.show()

    #720y 1280x
    lower =(0, 0, 0) # lower bound for each channel
    upper = (254, 100,100) # upper bound for each channel

    # create the mask and use it to change the colors
    mask = cv2.inRange(frame, lower, upper)
    frame[mask != 0] = [0,0,0]

    
    cv2.imshow('frame',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
