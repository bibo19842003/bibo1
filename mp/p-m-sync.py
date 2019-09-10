#!/usr/bin/python3

'''
  download gerrit project
'''

from urllib import request
import sys
import os
import threading
import queue


class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print ("开启线程：" + self.name)
        process_data(self.name, self.q)
        print ("退出线程：" + self.name)

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print ("thread %s fetching %s" % (threadName, data))
            project_all_path = project_path + data + ".git"
            if not os.path.exists(project_all_path):
                print("init new project: " + data)
                os.system("git init --bare %s" % (project_all_path))
            os.chdir(project_all_path)
#            print("fetch project: " + data)
            os.system("git fetch -f %s refs/heads/*:refs/heads/*" % (gerrit_path + data))
        else:
            queueLock.release()


project_list = "/home/bibo/house/source-code-mirror/bibo-project.txt"
project_path = "/home/bibo/house/source-code-mirror/"
project_page = "https://gerrit.googlesource.com/?format=TEXT"
gerrit_path = "https://gerrit.googlesource.com/"
tn = 4

exitFlag = 0

# download project list
response = request.urlopen(project_page)

if response.getcode() != 200:
    print("download project list failed !!!")
    sys.exit(1)

page = response.read()
page = page.decode('utf-8')
print(page)

f1 = open(project_list, "w+")
f1.write(page)
f1.close()

with open(project_list,'r') as f2:
    projects = [line.rstrip('\n') for line in f2]

# 下载 project
threadList = range(1, tn + 1)
queueLock = threading.Lock()
workQueue = queue.Queue()
threads = []
threadID = 1

# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for p in projects:
    workQueue.put(p)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")

print("You are good !!!")



