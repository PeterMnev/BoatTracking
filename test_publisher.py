#!/usr/bin/env python

#  --- Changelog ---
# Goal:     Combine many other packages
# Status:   07/11: Started with script

import rospy
import signal
import random
import sys
import math
import numpy as np
import time
from std_msgs.msg import Int32, String, Float64MultiArray, Bool, Float32




def signal_handler():
    sys.exit(0)


if __name__ == '__main__':
    # Enable killing the script with Ctrl+C.
    signal.signal(signal.SIGINT, signal_handler)

    rospy.init_node('test_publisher', anonymous=True)

    # Publishers
    test_publisher = rospy.Publisher("/test",     Float64MultiArray,               queue_size=1, latch=True)

    rate = rospy.Rate(10)

    f = 0.5 # Hz = rev/s
    s = f * (2*math.pi)

    while 1:
        t = time.time()
        vec = [t, math.atan2(math.sin(t*s)+0.01, math.cos(t*s))+math.pi]
        msg = Float64MultiArray()
        msg.data = vec
        test_publisher.publish(msg)
        rospy.loginfo(msg.data)
        rate.sleep()
