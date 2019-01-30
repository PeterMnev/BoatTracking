import threading
import Queue
import time
import cv2
import neuTracker
import copy
import numpy as np

class Intermediator:
	
	def __init__(self, inputFeed):
                self.pframe = None
		self.input = inputFeed
		self.neuralQ = Queue.Queue()
		self.outQ = Queue.Queue()	
		self.nTracker = neuTracker.NeuralTracker(self.neuralQ, self.outQ)
		self.nTracker.start()
				
	def start(self):
		self.thread = threading.Thread(target=self.process, args=())
		self.thread.start()
		return self	
        def interpolate(self, modframe):
            #center of image param
            center = [360,640]

#Ideally these parameters would be dynamically adjusted based on the neural net initial grab, and then based on the bounding box size.
#Width and height params
            x = 270
            y = 480
            height, width, channels = modframe.shape
            subFrame = modframe[max(0,center[0]-270):min(720,center[0]+270), max(0,center[1]-480):min(1280,center[1]+480)]
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
            cv2.rectangle(subFrame, (0,0),(960,480),(0,255,255),thickness=4)  
            return modframe
            
            
	def process(self):
		begin_time = time.time()-.5
		while True:
		        frame = self.input.frameQ.get()
		        self.input.frameQ.task_done()
		        cur_time = time.time()
			if (cur_time - begin_time >= 3):
			        begin_time = cur_time
			        self.neuralQ.put(frame)

                        modframe = copy.copy(frame)
                        self.pframe = self.interpolate(modframe)
			#Do processing
			#(set of opencv commands here)
		        self.interCord = "None" #temporarily none.

			
			try:	
			        asd = self.outQ.get(False)
			        print(asd)
			        self.outQ.task_done()
			except:
			        continue			
							
		cv2.destroyAllWindows()
