from serial import Serial
from datetime import datetime
import os, time, warnings
import pandas as pd
import kbhit
warnings.filterwarnings("ignore")


port = "/dev/ttyACM0"

# os.system("../")
# os.system("minicom -D "+port)


def getDistance():
    distList=[]
    timeList=[]
    lx = kbhit.lxTerm()
    lx.start()

    ser = Serial(port, 115200)
    distIndex = 7
    print("DWM1001 Start")
    while True:
        res = ser.readline()
        dist= res.decode()[:len(res)-1].split(",")[distIndex]
        time = datetime.now()

        distList.append(dist[:len(dist)-1])
        timeList.append(time)
        print("[",time,"] ",dist)
        if lx.kbhit():
            c = lx.getch()
            c_ord = ord(c)
            print(c)
            if c_ord == 32: # ESC
                break
    lx.reset()
    print(distList)
    print(timeList)
    
getDistance()