#!/usr/bin/env python
from __future__ import division
import rospy
import math
from std_msgs.msg import String, Empty, Int32, Float32
from geometry_msgs.msg import Twist, Pose, PoseStamped, PointStamped, Point
import signal
from time import sleep

#TODO (AKA things that were omitted because they would be annoying in testing)

# 1) Call the command that starts the recognition from a script / bash script
# 2) Organize file locations. seriously.
# 3) ROS Messages
# 4) Figure out what I adjusted in the darknet setup (oops)
# 5) Implement fix for the case when an object is assigned two types (causing crashes)



def signal_handler():
    sys.exit(0)
		
def altitude(data):
	altitude = data.data
	print altitude

	
def angles(data):
	print data
	yaw = data[0]
	pitch = data[1]

def reader():
	pub = rospy.Publisher('target_pose', Float32, queue_size = 1)
	rospy.Subscriber("altitude", Float32, altitude)
	rospy.Subscriber("camera_angles", Float32, angles)
	while True:
		f = open("/home/lenny/darknet/output.txt", "r")
		if (f.mode == 'r'):
			contents = f.read()
			process(contents)
			sleep(0.5)
				
def process(fd):
	split1 = fd.split('\n')
	for x in split1:
		split2 = x.split(', ')
		if (split2[0] == 'boat'): 
			calculate(split2)


def calculate(pose):
	#Left = x1 - index 1, Top = y1-index 2. Right = x2 - index 3, Bottom = y2 - index4	
	#Origin is TOP LEFT CORNER
	#Calculating the center of box.
	#I need the resolution of the image to do this.
	pixelX = int(pose[1]) + (int(pose[3]) - int(pose[1]))/2
	pixelY = int(pose[2]) + (int(pose[4]) - int(pose[2]))/2

	#What lies below is tentative depending on the limits on the values provided
	#Assume 0 yaw is forwards  0 pitch is horizontal
	
	angleX = 63.7
	angleY = 39

	resultAngleX = ((pixelX-980)/1960 * angleX) + yaw #Azimuth
	resultAngleY = (pixelY-540)/1080 * angleY + pitch 
	distance = 0
	radiansY = math.radians(resultAngleY)
	if radiansY >= 0:
		distance = math.sin(radiansY)*h
	else:
		distance = math.sin(radiansY)*h


	newCoord = Geodesic.WGS84.Direct(lat,lon,resultAngleX, distance)

	print newCoord.get("lat2")
	print newCoord.get("lon2")




if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	rospy.init_node('box2cord', anonymous=True)
	altitude = 10 #meters
	yaw = 0 #degrees
	pitch = 0
	reader()
