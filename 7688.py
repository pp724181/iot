import socket
import time
import requests
import os
import httplib, urllib

def post_to_thingspeak(payload):  
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    not_connected = 1
    while (not_connected):
        try:
            conn = httplib.HTTPConnection("api.thingspeak.com:80")
            conn.connect()
            not_connected = 0
        except (httplib.HTTPException, socket.error) as ex:
            print "Error: %s" % ex
            time.sleep(10)  # sleep 10 seconds

    conn.request("POST", "/update", payload, headers)
    response = conn.getresponse()
    print( response.status, response.reason, payload, time.strftime("%c"))
    data = response.read()
    conn.close()
    
def wifi():
    connect_state = 0
    while connect_state==0 :
        try:
            r = requests.get("https://tw.yahoo.com/")
            break
        except requests.ConnectionError, e:
            print "No wifi"
def connect() : 
    while True :
        
        error = 0
        
        os.system("fswebcam -i 0 -d v4l2:/dev/video0 -r 1280x720 --no-banner -p YUYV --jpeg 95 --save /tmp/test.jpg")       
        print 'Start send image'
        imgFile = open('/tmp/test.jpg','rb')
        
        while True :
            imgData = imgFile.readline(1024)
            if not imgData:
                break
            try : 
                sockobj.send(imgData)
            except :
                error = 1
                break
        try :
            sockobj.send("theend")
        except :
            print "Connect break!"
            error = 1
            sockobj.close()
            time.sleep(5)
            break
            
        imgFile.close()
        params = urllib.urlencode({'field1': data, 'key': thinkSpeakApiKey})
        post_to_thingspeak(params)
        if error == 0 :
            print 'Transmit End'
            time.sleep(0.1)
        else :
            print "Connect success"
            
print "wifi connecting....."

wifi()

print "wifi connecting success"

thinkSpeakApiKey = "JHXYQDR48WTQZUT0"

while True :
    #host = '192.168.8.6'
    host = '54.186.197.36' 
    port = 8080
    address = (host, port)
    sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True :
        try :
            sockobj.connect(address)
            break
        except :
            print "Connect to server fail........"
            print "Reconnect after 5 second"
            time.sleep(5)
    print "Connect to server success........"
    connect()
