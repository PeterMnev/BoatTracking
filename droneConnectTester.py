import argparse
import sys
import time
from dronekit import connect, VehicleMode
from time import sleep
from geographiclib.geodesic import Geodesic
#python droneConnectTester.py --connect 192.168.0.217:14450


parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
parser.add_argument('--connect', 
help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()
connection_string = args.connect

self.vehicle = connect(connection_string, wait_ready=True)

print (vehicle.Gimbal.roll)
    
