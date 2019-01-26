import threading
import Queue
import time

# https://docs.python.org/2/library/queue.html


def work1(threadname, q):
	while(True):


		q.put("an awesome amazing potato")
		q.join()




q = Queue.Queue()



thread1 = threading.Thread(target=work1, args=("Thread-1",q))

thread1.start()

while (True):
	print (q.get())
	
	print (q.qsize())
	
	q.task_done()
