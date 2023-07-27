import pandas as pd
import numpy as np
import math, os, datetime, kbhit, time
from datetime import datetime
import time
import board
import adafruit_icm20x

analysisPath = "Python-RPI-RTLS/mag_csv/"
#Trial 1: -12.45 7.65
#Trial 2: -17.9999 6.074999
#0.5204260257859987 -11.392350809461004
#0.7371782007859977 -11.346112334460999
#0.8691691257859961 -12.161573009461002
tmpCalX= -1.4932897742140003
tmpCalY= -4.161397634460999

hCalX = 16.322921
hCalY = -7.212200
hCalZ = -22.263491

sCal1= [1.103134, -0.014659, 0.025388]
sCal2= [-0.014659, 1.040778, 0.014565]
sCal3= [0.025388, 0.014565,  0.979180]
def toCSV(path, fileName, df):
    os.chdir(path)
    df.to_csv(fileName, index=False)
    os.chdir("../../")

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


def calibrationDataCollection():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    icm = adafruit_icm20x.ICM20948(i2c)
    
    lx = kbhit.lxTerm()
    lx.start()
    xList=[]
    yList=[]
    zList=[]
    print("Calibration Start")
    while True:
        #print(icm.magnetic)

        if lx.kbhit(): 
            c = lx.getch()
            c_ord = ord(c)
            if c_ord == 32: # Spacebar
                print("\nCalibration Stop")
                break
        
        x = icm.magnetic[0]
        y = icm.magnetic[1]
        z = icm.magnetic[2]
        #print([x,y,z])

        xList.append(x)
        yList.append(y)
        zList.append(z)

        # print((max(x)+min(x))/2)
        # print((max(y)+min(y))/2)
        # print((max(z)+min(z))/2)
        # print()
        
    
    comp_df = pd.DataFrame({"x": xList, "y": yList, "z": zList})
    comp_df["offset_x"] = (comp_df.x.max()+comp_df.x.min())/2
    comp_df["offset_y"] = (comp_df.y.max()+comp_df.y.min())/2
    comp_df["offset_z"] = (comp_df.z.max()+comp_df.z.min())/2
    comp_df["cal_x"] = comp_df.x - comp_df.offset_x
    comp_df["cal_y"] = comp_df.y - comp_df.offset_y
    comp_df["cal_z"] = comp_df.z - comp_df.offset_z
    toCSV(analysisPath, "CalibrationFlat.csv", comp_df)
    return comp_df.offset_x[0], comp_df.offset_x[1]


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

def beforeDataColection(icm):
    
    lx = kbhit.lxTerm()
    lx.start()
    xList=[]
    yList=[]
    zList=[]
    print("Calibration Start")
    while True:
        #print(icm.magnetic)

        if lx.kbhit(): 
            c = lx.getch()
            c_ord = ord(c)
            if c_ord == 32: # Spacebar
                print("\nCalibration Stop")
                break
        
        x = icm.magnetic[0]
        y = icm.magnetic[1]
        z = icm.magnetic[2]
        #print([x,y,z])

        x, y = getCalibarion(x,y,z)

        xList.append(x)
        yList.append(y)
        zList.append(z)
        
    
    comp_df = pd.DataFrame({"x": xList, "y": yList, "z": zList})
    offsetX = (comp_df.x.max()+comp_df.x.min())/2
    offsetY = (comp_df.y.max()+comp_df.y.min())/2
    print(offsetX, offsetY)
    return offsetX, offsetY

#LowPassFilter
def LowPassCompass():
    global tmpCalX, tmpCalY
    i2c = board.I2C()  # uses board.SCL and board.SDA
    icm = adafruit_icm20x.ICM20948(i2c)
    lx = kbhit.lxTerm()
    lx.start()
    compassHeading = getHeading(icm.magnetic)
    filteredHeading = compassHeading
    headingList=[]
    filteredHeadingList=[]
    sensitivity = 0.4

    #tmpCalX, tmpCalY = beforeDataColection(icm)

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
        time.sleep(0.1)
    df = pd.DataFrame({"compassHeading": headingList, "filteredHeading": filteredHeadingList})
    df["fMax"] = df.filteredHeading.max()
    df["fMin"] = df.filteredHeading.min()
    df["fMean"] = df.filteredHeading.mean()
    df["fStd"] = df.filteredHeading.std()

    df["cMax"] = df.compassHeading.max()
    df["cMin"] = df.compassHeading.min()
    df["cMean"] = df.compassHeading.mean()
    df["cStd"] = df.compassHeading.std()
    
    toCSV(analysisPath, "compass"+str(sensitivity)+".csv",df) 
    return df
    

#calibrationDataCollection()
df = LowPassCompass()

