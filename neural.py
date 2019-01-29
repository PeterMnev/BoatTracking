import cv2
import numpy as np
import time
import sys
sys.path.insert(0, '/home/nvidia/Documents/darknet')
import darknet


def runDetection(frame, net, meta):
        
            
        
	im, image = darknet.array_to_image(frame)
	darknet.rgbgr_image(im)
	r = darknet.detect(net, meta, im)
	print (im)
	return r
		
