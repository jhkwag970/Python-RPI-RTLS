import pandas as pd
import numpy as np
import math, os, datetime, kbhit, time
from datetime import datetime
import time
import board
import adafruit_icm20x

analysisPath = "Python-RPI-RTLS/mag_csv/"

calX = -12.45
calY = 7.65
def toCSV(path, fileName, df):
    os.chdir(path)
    df.to_csv(fileName, index=False)
    os.chdir("../../")

def getHeading(magnetic):
    x = magnetic[0]+calX
    y = magnetic[1]+calY
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


def calibrationDataCollection():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    icm = adafruit_icm20x.ICM20948(i2c)
    
    lx = kbhit.lxTerm()
    lx.start()
    xList=[]
    yList=[]
    zList=[]
    while True:
        #print(icm.magnetic)

        if lx.kbhit(): 
            c = lx.getch()
            c_ord = ord(c)
            if c_ord == 32: # Spacebar
                print("\nStop")
                break
        
        x = icm.magnetic[0]-12.45
        y = icm.magnetic[1]+7.65
        z = icm.magnetic[2]
        print([x,y,z])

        xList.append(x)
        yList.append(y)
        zList.append(z)

        # print((max(x)+min(x))/2)
        # print((max(y)+min(y))/2)
        # print((max(z)+min(z))/2)
        # print()
        time.sleep(0.1)
    
    comp_df = pd.DataFrame({"x": xList, "y": yList, "z": zList})
    # comp_df["offset_x"] = (comp_df.x.max()+comp_df.x.min())/2
    # comp_df["offset_y"] = (comp_df.y.max()+comp_df.y.min())/2
    # comp_df["offset_z"] = (comp_df.z.max()+comp_df.z.min())/2
    # comp_df["cal_x"] = comp_df.x - comp_df.offset_x
    # comp_df["cal_y"] = comp_df.y - comp_df.offset_y
    # comp_df["cal_z"] = comp_df.z - comp_df.offset_z
    toCSV(analysisPath, "Calibration_270.csv", comp_df)


def Compass():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    icm = adafruit_icm20x.ICM20948(i2c)
    lx = kbhit.lxTerm()
    lx.start()
    headingList=[]
    filteredHeadingList=[]
    while True:
        heading = movingAverageFilter(icm)
        print(heading)
        headingList.append(heading[0])
        filteredHeadingList.append(heading[1])
        if lx.kbhit(): 
            c = lx.getch() 
            c_ord = ord(c)
            if c_ord == 32: # Spacebar
                print("\nStop")
                break
        time.sleep(0.5)
    df = pd.DataFrame({"compassHeading": headingList, "filteredHeading": filteredHeadingList})
    toCSV(analysisPath, "compass.csv",df)    

stableNum=30
#Moving Average Filter
def movingAverageFilter(icm):
    
    filteredHeading = -1
    for i in range(stableNum):
        compassHeading = getHeading(icm.magnetic)
        filteredHeading += compassHeading
    
    filteredHeading /= stableNum
    return [compassHeading, filteredHeading]    

#KalmanFilter
def kalmanFilter(icm):
    print("kalman")


#LowPassFilter
def LowPassCompass():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    icm = adafruit_icm20x.ICM20948(i2c)
    lx = kbhit.lxTerm()
    lx.start()
    compassHeading = getHeading(icm.magnetic)
    filteredHeading = compassHeading
    headingList=[]
    filteredHeadingList=[]
    sensitivity = 0.5
    while True:    
        compassHeading = getHeading(icm.magnetic)
        filteredHeading = filteredHeading * (1-sensitivity) + compassHeading * sensitivity
        headingList.append(compassHeading)
        filteredHeadingList.append(filteredHeading)
        print([compassHeading, filteredHeading])
        if lx.kbhit(): 
            c = lx.getch() 
            c_ord = ord(c)
            if c_ord == 32: # Spacebar
                print("\nStop")
                break
        time.sleep(0.5)

    df = pd.DataFrame({"compassHeading": headingList, "filteredHeading": filteredHeadingList})
    toCSV(analysisPath, "compass.csv",df) 
    

LowPassCompass()