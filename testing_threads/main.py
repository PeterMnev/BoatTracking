import threading
import Queue
import time
import cv2
import videoGet

# https://docs.python.org/2/library/queue.html

#occasionally pass to ANOTHER thread from this thread, by updating a flag?
def work1(threadname, inputFeed):
        while(True):
                frameT = inputFeed.frameQ.get()

                inputFeed.frameQ.task_done()
                if cv2.waitKey(1) & 0xFF == ord('w'):
                        break
                try:
                        cv2.imshow('imageTHREAD',frameT)
                except:
                        break

        cv2.destroyAllWindows()
        






inputFeed = videoGet.VideoGet("vid.avi")
inputFeed.start()

thread1 = threading.Thread(target=work1, args=("Thread-1",inputFeed))

thread1.start()


start_time = time.time()
frame = inputFeed.frameQ.get(True,None)
inputFeed.frameQ.task_done()
while (True):
        cur_time = time.time()
        if (cur_time - start_time) >= 2:
                start_time = cur_time
                try:
                        frame = inputFeed.frameQ.get(True,1)
                except:
                        break
                inputFeed.frameQ.task_done()

        if cv2.waitKey(1) & 0xFF == ord('q'):
                inputFeed.stop()
                break


        try:
                cv2.imshow('image',frame)
        except:
                break
 
        
        
cv2.destroyAllWindows()

