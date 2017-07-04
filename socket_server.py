from socket import *
import h
import threading
import time
import cv2
import argparse
import os

global i 
i = 0
def websocketlink(sock,addr):
    print ('Accept new web socket from %s:%s...' % addr)
    item = []
    firstFrame = cv2.imread('/home/ec2-user/0616/firstframe.png')
    h.InitItem(item)
    while True:
        ##################################################
        # 
        print('Waiting Data')

        global i
        directory = "./picture/"
        directory = directory+time.strftime("%b")+time.strftime("%d") 
        if not os.path.exists(directory):
            os.makedirs(directory)
            #file1 = open(directory+'result.txt','w')
            #file1.close()
        imgFile = open(directory+'/' + str(i) + '.png','wb')  #
        print('Writing')
        while True:
            imgData = sock.recv(1024)  #
            if str(imgData).find("theend") != -1 :
                imgFile.write(imgData[:-6])
                print (imgData)
                break  #
            if not imgData:
                break  #
            imgFile.write(imgData)
        
        imgFile.close()
        #f = open('result.txt','r')
        #for x in range(0,8):
        #    item[x].motiontime = int(f.readline())
        #f.close()
        frame = cv2.imread(directory+'/'+str(i)+'.png')
        h.MotionDetection(item,frame,firstFrame)
        file1 = open(directory+'/result.txt','w')
        for x in range(0,8):
            file1.write(str(item[x].motiontime) + '\n')
        file1.close()

        if not imgData:
                break  #
        print('image save')
        i = i + 1
        ##################################################



def Socketserver():
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
    sockobj.bind(('172.31.25.232',8080))
    sockobj.listen(5)
    print ('Waiting for connection ......')
    while True:
        sock,addr=sockobj.accept()
        t=threading.Thread(target=websocketlink,args=(sock,addr))
        t.start()

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=1500, help="minimum area size")
args = vars(ap.parse_args())

Socketserver()
