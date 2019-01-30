import cv2
import numpy as np
import Queue
import sys
import threading
sys.path.insert(0, '/home/nvidia/Documents/darknet')
import darknet

class NeuralTracker:
        def __init__(self, frameQ, outQ):
                self.nframe = None
                #Initialize Net
                self.queue = frameQ
                self.out = outQ
        	self.net = darknet.load_net("/home/nvidia/Documents/darknet/cfg/yolov3.cfg", "/home/nvidia/Documents/darknet/yolov3.weights", 0)
	        self.meta = darknet.load_meta("/home/nvidia/Documents/darknet/cfg/coco.data")
        #Thread start
        def start(self):
                self.thread = threading.Thread(target=self.process, args=())
		self.thread.start()
		return self
        
        def process(self):
                while True:                     
                        self.nframe = self.queue.get(True)
                 
        	        im, image = darknet.array_to_image(self.nframe)
                        darknet.rgbgr_image(im)
                        r = darknet.detect(self.net, self.meta, im) 
                        self.out.put(r)
                        self.out.join()
                


