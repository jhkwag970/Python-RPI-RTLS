from serial import Serial
from datetime import datetime
import os, time, warnings, kbhit, math
import pandas as pd
import numpy as np
warnings.filterwarnings("ignore")

import time
import board
import adafruit_icm20x

port = "/dev/ttyACM0"
distIndex = 7
def getData():
    ser = Serial(port, 115200)
    i2c = board.I2C()
    icm = adafruit_icm20x.ICM20948(i2c)
    lx = kbhit.lxTerm()
    lx.start()

    dateList=[]
    distList = []
    angleList=[]
    xList=[]
    yList=[]
    timeCnt = 0
    while True:
        res = ser.readline()
        dist= res.decode()[:len(res)-1].split(",")[distIndex]
        x = icm.magnetic[0]-12.45
        y = icm.magnetic[1]+7.65
        z = icm.magnetic[2]

        compassHeading = -1
        if y == 0:
            if x >0:
                compassHeading = 0.0
            else:
                compassHeading = 180.0
        if x < 0:
            compassHeading = 360+math.atan2(x, y)*180/math.pi
        else:
            compassHeading = math.atan2(x, y)*180/math.pi
        

        date = datetime.now()

        # if len(dist) == 0:
        #     print("Data Stop")
        #     timeCnt+=1
        #     time.sleep(0.5)
        #     continue
        # else:
        #     if(timeCnt > 0):
        #         print("Data Return")
        #     timecnt = 0

        print("[%s]  %.2f  %s" %(str(date), compassHeading, dist))

        distList.append(dist[:len(dist)-1])
        angleList.append(compassHeading)
        dateList.append(date)

        if stopLogging(lx):
            break
            
        if timeCnt > 0:
            print("Stop Logging Enabled")
            if stopLogging(lx):
                break

    lx.reset()
    toDistCSV(dateList, distList, angleList,)

def toDistCSV(dateList, distList, angleList):
    dwmDf = pd.DataFrame({'time': dateList, 'distance': distList, 'angle': angleList})
    now = datetime.now()
    fileName = str(now.strftime('%Y-%m-%d %H:%M:%S'))+".csv"
    
    os.chdir("final_csv/")
    dwmDf.to_csv(fileName, index=False)
    #os.chdir("../../")

def changeDir():
    os.chdir("/home/pi/Documents/Python-RPI-RTLS")

def stopLogging(lx): 
    if lx.kbhit():
        c = lx.getch()
        c_ord = ord(c)
        if c_ord == 32: # Spacebar
            print("\nData Collection Stop")
            return True

def runDataCollection():
    changeDir()
    getData()

runDataCollection()

