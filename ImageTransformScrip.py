from __future__ import division
from __future__ import print_function
import numpy as np
import math

from geographiclib.geodesic import Geodesic


from dronekit import connect, VehicleMode
import time

#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
parser.add_argument('--connect', 
                   help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
vehicle = connect(connection_string, wait_ready=True)

#--connect udpin:192....

print (vehicle.heading)

yaw = 45 #DEGREES FROM NORTH!
pitch = 45 #Degrees from horizontal. (downwards positive, value should NEVER be negative. If it is negative, then your result will be incorect
# The distance will calculate to be negative of what it is and the gimbal will turn around, completely losing the boat NICE.

roll = 0
lat = 38.992062
lon = -76.933684

h = 230 #metres

pixelX = 1500
pixelY = 900

#yaw
angleX = 63.7
#pitch
angleY = 39

resultAngleX = ((pixelX-980)/1960 * angleX) + yaw #Azimuth
resultAngleY = (pixelY-540)/1960 * angleY + pitch 
distance = 0
radiansY = math.radians(resultAngleY)
if radiansY >= 0:
    distance = math.sin(radiansY)*h
else:
    distance = math.sin(radiansY)*h


newCoord = Geodesic.WGS84.Direct(lat,lon,resultAngleX, distance)

print (newCoord.get("lat2"))
print (newCoord.get("lon2"))

#Look at new coordinate! good job you did it.

