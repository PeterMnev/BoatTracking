# BoatTracking
Drone Boat Tracking Algorithm

Features:
* Implementation of YOLOv3 neural network in conjunction with OpenCV to detect and track boats.

* Multithreaded implementation prevents I/O bottlenecks from camera input and drone input

* Computes coordinates based on drone position and orientation, gimbal orientation, and location of boat on image (requires knowledge of camera parameters)

Todo:
* Add thread flowchart
* Implement drone data collection once drone is set up
* Create implementation guide
