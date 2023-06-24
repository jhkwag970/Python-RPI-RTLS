from serial import Serial
from datetime import datetime


ser = Serial('/dev/ttyACM0', 115200)

distIndex = 7
nowtime = datetime.now()
while True:
    if ser.readable():
        res = ser.readline()
        dist= res.decode()[:len(res)-1].split(",")[distIndex]
        nowtime = datetime.now()
        print("[",nowtime,"] ",dist)