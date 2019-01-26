import threading
import Queue
import time
import cv2
import videoGet

# https://docs.python.org/2/library/queue.html


def work1(threadname, inputF):
        while(True):
                frameT = inputF.frame
                if cv2.waitKey(150) & 0xFF == ord('w'):
                        break
                cv2.imshow('imageTHREAD',frameT)

        cv2.destroyAllWindows()
        






inputFeed = videoGet.VideoGet(0)
inputFeed.start()

thread1 = threading.Thread(target=work1, args=("Thread-1",inputFeed))

thread1.start()

while (True):
        frame = inputFeed.frame
        if cv2.waitKey(15) & 0xFF == ord('q'):
                inputFeed.stop()
                break
        time.sleep(1)
        cv2.imshow('image',frame)
        
        
cv2.destroyAllWindows()

