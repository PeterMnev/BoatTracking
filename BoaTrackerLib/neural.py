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

def neuralTrack(self, threadname, nq, cap):
	net = darknet.load_net("/home/nvidia/Documents/darknet/cfg/yolov3.cfg", "/home/nvidia/Documents/darknet/yolov3.weights", 0)
	meta = darknet.load_meta("/home/nvidia/Documents/darknet/cfg/coco.data")
	while (True):
		ret,frame = cap.read()
		im, image = darknet.array_to_image(frame)
                darknet.rgbgr_image(im)
                r = darknet.detect(net, meta, im)              
                print (r)
                sleep(12)
