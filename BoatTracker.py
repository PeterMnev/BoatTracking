#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
import math
import signal
import cv2
import numpy as np
from threading import Thread
from Queue import Queue

#from dronekit import connect, VehicleMode
from time import sleep
from geographiclib.geodesic import Geodesic

import argparse  
#should probably rename neural
import neural
import sys
sys.path.insert(0, '/home/nvidia/Documents/darknet')
import darknet


#parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
#parser.add_argument('--connect', 
#help="vehicle connection target string. If not specified, SITL automatically started and used.")
#args = parser.parse_args()
#connection_string = args.connect




#TODO
# !!!!!!! Figure out what I adjusted in the darknet setup (oops) !!!!!!!
#  Implement fix for the case when an object is assigned two types (causing crashes)

class Converter:
	
	def signal_handler(self):
	    sys.exit(0)
			
	

					
	def process(self, fd):
		split1 = fd.split('\n')
		for x in split1:
			split2 = x.split(', ')
			if (split2[0] == 'boat'): 
				self.calculate(split2)

        def updateState(self):

                #Update position relative to world
                self.altitude = vehicle.location.global_frame.alt
                self.lat = vehicle.location.global_frame.lat
                self.lon = vehicle.location.global_frame.lon

		#Gimbal Orientation

                #GPitch is -90 if pointing straight down, so multiply by -1
                self.GimbalPitch = vehicle.gimbal.pitch*-1
                #GYaw 0 is north! 90 is WEST
                self.GimbalYaw = vehicle.gimbal.yaw
                

                #Drone Orientation
                
		#Drone Angle of Yaw zero is north, 90 is EAST
                self.yaw = vehicle.heading
		#Drone Angle of Pitch - point up = positive
		self.pitch = vehicle.Attitude.pitch
                
                

                
	def calculate(self, pose):

		#Left = x1 - index 1, Top = y1-index 2. Right = x2 - index 3, Bottom = y2 - index4	
		#Origin is TOP LEFT CORNER
		#Calculating the center of box.
		#I need the resolution of the image to do this.
		
		pixelX = int(pose[1]) + (int(pose[3]) - int(pose[1]))/2
		pixelY = int(pose[2]) + (int(pose[4]) - int(pose[2]))/2

                
                #Assume 0 yaw is forwards  0 pitch is horizontal

                #Fixed FOV of the camera in the X direction - both will depend on zoom in future
		FOV_Yaw = 63.7
		

		#Fixed FOV of the camera in the Y direction
		FOV_Pitch = 39

                #Direction of the boat relative to the drone based on camera orientation,
		# drone orientation and the boat's coordinate on the image.
		ResultYaw = ((pixelX-980)/1960 * GimbalYaw) + self.yaw #From Azimuth
		ResultPitch = (pixelY-540)/1080 * GimbalPitch + self.pitch 


		distance = 0
		ResultPitchRadians = math.radians(ResultPitch)
		if ResultPitchRadians >= 0:
			distance = math.sin(ResultPitchRadians)*self.altitude
		else:
			distance = math.sin(ResultPitchRadians)*self.altitude


		newCoord = Geodesic.WGS84.Direct(self.lat,self.lon,ResultYaw, distance)

		print (newCoord.get("lat2"))
		print (newCoord.get("lon2"))
	
	def NeuralTrack(self, threadname, nq, cap):
		#net = darknet.load_net("/home/nvidia/Documents/darknet/cfg/yolov3.cfg", "/home/nvidia/Documents/darknet/yolov3.weights", 0)
		#meta = darknet.load_meta("/home/nvidia/Documents/darknet/cfg/coco.data")
		while (True):
			ret,frame = cap.read()
			#r = neural.runDetection(frame, net, meta)		
			print (frame)
			
	def __init__(self):
		#temp vals
		self.altitude = 100.0 #meters
		self.yaw = 45 #degrees
		self.lat = 38.992062
		self.lon = -76.933684
                self.GimbalPitch = 45
                self.GimbalYaw = 45
		self.pitch = 45
		#self.vehicle = connect(connection_string, wait_ready=True)		
		signal.signal(signal.SIGINT, self.signal_handler)
		self.capture = cv2.VideoCapture('testCases/vid.avi')
		
		self.RegCordQueue = Queue()
		self.NNCordQueue = Queue()
		
		NNThread = Thread(target = self.NeuralTrack, args = ("Thread-1", self.NNCordQueue, self.capture))
		NNThread.start()
		#interThread = Thread(target = self.Interpolate, args = ("Thread-2", self.RegCordQueue))
		
			

convert = Converter()

