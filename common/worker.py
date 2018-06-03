import threading


class worker(threading.Thread):
    def __init__(self,id, name):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            print("thread%d %s: waiting for task" %(self.ident,self.name))
            # getStory(self.id)
            self.thread_stop = True

    def stop(self):
        self.thread_stop = True


def createThread(id,Tnum):
    threadList = []
    for i in range(1,Tnum):
        threadList.append(str(i))

    threads = []
    # 创建新线程
    for tName in threadList:
        thread = worker(id, tName)
        thread.start()
        threads.append(thread)
        id += 1
    # 等待所有线程完成
    # join()方法的位置是在for循环外的，也就是说必须等待for循环里的两个进程都结束后，才去执行主进程。
    #join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞。
    for t in threads:
        t.join()
    # sleep(0.5)