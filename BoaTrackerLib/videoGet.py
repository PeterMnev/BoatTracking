from threading import Thread
import cv2
import Queue

class VideoGet:

    def __init__(self, src):
        self.stream = cv2.VideoCapture(src)
        self.frameQ = Queue.Queue()
        self.grabbed, self.frame = self.stream.read()
        self.frameQ.put(self.frame)
        self.stopped = False

    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                self.frameQ.put(self.frame)
                self.frameQ.join()


    def stop(self):
        self.stopped = True
