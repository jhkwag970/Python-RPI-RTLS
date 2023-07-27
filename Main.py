from serial import Serial
from datetime import datetime
import os, time, warnings, kbhit, math
import pandas as pd
import numpy as np
warnings.filterwarnings("ignore")

import time
import board
import adafruit_icm20x

tmpCalX= -1.9303944992140032
tmpCalY= -1.5171074844610022

hCalX = 16.322921
hCalY = -7.212200
hCalZ = -22.263491

sCal1= [1.103134, -0.014659, 0.025388]
sCal2= [-0.014659, 1.040778, 0.014565]
sCal3= [0.025388, 0.014565,  0.979180]

def getCalibarion(x,y,z):
    x -= hCalX
    y -= hCalY
    A = np.array([sCal1, sCal2, sCal3])
    B = np.array([[x],[y],[z]])
    Cal = np.matmul(A, B)

    x = Cal[0][0] 
    y = Cal[1][0] 
    z = Cal[2][0]

    return x,y

def getHeading(magnetic):
    x = magnetic[0]
    y = magnetic[1]
    z = magnetic[2]

    x, y = getCalibarion(x,y,z)
    x -= tmpCalX
    y -= tmpCalY

    compassHeading = -1    
    if y == 0:
        if x >0:
            compassHeading = 90.0
        else:
            compassHeading = 270.0
    if x < 0:
        compassHeading = 360+math.atan2(x, y)*180/math.pi
    else:
        compassHeading = math.atan2(x, y)*180/math.pi
    return compassHeading

def beforeDataColection(icm):
    
    lx = kbhit.lxTerm()
    lx.start()
    xList=[]
    yList=[]
    zList=[]
    print("Calibration Start")
    while True:

        if lx.kbhit(): 
            c = lx.getch()
            c_ord = ord(c)
            if c_ord == 32: # Spacebar
                print("\nCalibration Stop")
                break
        
        x = icm.magnetic[0]
        y = icm.magnetic[1]
        z = icm.magnetic[2]

        x, y = getCalibarion(x,y,z)

        xList.append(x)
        yList.append(y)
        zList.append(z)    
    lx.reset()
    
    comp_df = pd.DataFrame({"x": xList, "y": yList, "z": zList})
    offsetX = (comp_df.x.max()+comp_df.x.min())/2
    offsetY = (comp_df.y.max()+comp_df.y.min())/2
    
    return offsetX, offsetY

port = "/dev/ttyACM0"
distIndex = 7
def getData():
    global tmpCalX, tmpCalY

    ser = Serial(port, 115200)
    i2c = board.I2C()
    icm = adafruit_icm20x.ICM20948(i2c)
    lx = kbhit.lxTerm()
    lx.start()

    dateList=[]
    distList = []
    timeCnt = 0
 
    compassHeading = getHeading(icm.magnetic)
    filteredHeading = compassHeading
    headingList=[]
    filteredHeadingList=[]
    sensitivity = 0.5

    res = ser.readline()
    dist= res.decode()[:len(res)-1].split(",")[distIndex]
    filteredDist = dist
    distList=[]
    filteredDistList=[]
    dSensitivity = 0.5



    tmpCalX, tmpCalY = beforeDataColection(icm)
    print(tmpCalX, tmpCalY)

    while True:
        compassHeading = getHeading(icm.magnetic)
        filteredHeading = filteredHeading * (1-sensitivity) + compassHeading * sensitivity
        headingList.append(compassHeading)
        filteredHeadingList.append(filteredHeading)

        res = ser.readline()
        dist= res.decode()[:len(res)-1].split(",")[distIndex]
        filteredDist = filteredDist * (1-dSensitivity) + dist * dSensitivity
        distList.append(dist)
        filteredDistList.append(filteredDist)
        
        date = datetime.now()

        print("[%s]  %.2f  %s" %(str(date), compassHeading, dist))

        distList.append(dist[:len(dist)-1])
        dateList.append(date)

        if stopLogging(lx):
            break
            
        if timeCnt > 0:
            print("Stop Logging Enabled")
            if stopLogging(lx):
                break

    lx.reset()
    toDistCSV(dateList, distList, filteredHeadingList)

def toDistCSV(dateList, distList, angleList):
    dwmDf = pd.DataFrame({'time': dateList, 'distance': distList, 'angle': angleList})
    now = datetime.now()
    fileName = str(now.strftime('%Y-%m-%d %Hd%M%S'))+".csv"
    
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

