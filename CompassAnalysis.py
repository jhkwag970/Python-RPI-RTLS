import pandas as pd
import numpy as np
import math, os, datetime, kbhit, time
from datetime import datetime

path = "Python-RPI-RTLS/iphonMag_csv/"
analysisPath = "Python-RPI-RTLS/analysis_csv/"
accelPath = "Python-RPI-RTLS/accel_csv/"
csvIdx = 4
#path = "Python-RPI-RTLS/mpu9250_csv/"

def Compass(path, fileName):
    #print((math.atan2(1.486098,-41.7141)*180)/math.pi)
    mag = pd.read_csv(path+fileName)
    condition = [(mag.Bx > 0), (mag.Bx < 0), (mag.Bx == 0) & (mag.By < 0), (mag.Bx == 0) & (mag.By > 0)]
    choices = [360-np.arctan2(mag.Bx, mag.By)*180/math.pi,-np.arctan2(mag.Bx, mag.By)*180/math.pi,180.0, 0.0]
    mag["compass"] = np.select(condition, choices, default= np.nan)
    mag["mean"] = mag.compass.mean()
    mag["max"] = mag.compass.max()
    mag["min"] = mag.compass.min()
    mag["std"] = mag.compass.std()

    mag["offset"] = mag["mean"] - getAngle(fileName)


    toCSV(path, "angle_"+fileName, mag)
    
def toCSV(path, fileName, df):
    os.chdir(path)
    df.to_csv(fileName, index=False)
    os.chdir("../../")

def getAngle(file):
    intAngle = int(file.split(".")[0])
    return intAngle

def getOffsetAvg(fileList):
    offsetList=[]
    angleList=[]
    for file in fileList:
        if "angle" in file:
            offsetList.append(pd.read_csv(path + file)["offset"][0])
        else:
            angleList.append(str(getAngle(file))+" degree")

    offsetMean = np.mean(offsetList)
    df = pd.DataFrame({"angle": angleList, "offset": offsetList})
    df["mean"] = df.offset.mean()
    df["max"] = df.offset.max()
    df["min"] = df.offset.min()
    df["std"] = df.offset.std()

    toCSV(analysisPath, "Angle_Offset_Analysis.csv", df)

    return offsetMean