import pandas as pd
import numpy as np
import math, os, datetime

path = "Python-RPI-RTLS/iphonMag_csv/"
csvIdx = 4
#path = "Python-RPI-RTLS/mpu9250_csv/"

def Compass(path, fileName):
    #print((math.atan2(1.486098,-41.7141)*180)/math.pi)
    mag = pd.read_csv(path+fileName)
    mag["compass"] = np.where(np.arctan2(mag.Bx, mag.By)*180/math.pi < 0, 360+np.arctan2(mag.Bx, mag.By)*180/math.pi, np.arctan2(mag.Bx, mag.By)*180/math.pi)
    
    mag["mean"] = mag.compass.mean()
    mag["max"] = mag.compass.max()
    mag["min"] = mag.compass.min()
    mag["std"] = mag.compass.std()

    mag["offset"] = getAngle(file) - mag["mean"]


    toCSV(path, fileName, mag)
    
def toCSV(path, fileName, df):
    os.chdir(path)
    df.to_csv("angle_"+fileName, index=False)
    os.chdir("../../")

def getAngle(file):
    intAngle = int(file.split(".")[0])
    if(intAngle == 0):
        intAngle = 360
    return intAngle

fileList = os.listdir(path)

for file in fileList:
    if not "angle" in file:
        Compass(path, file)

offsetList=[]
for file in fileList:
    if "angle" in file:
        offsetList.append(pd.read_csv(path + file)["offset"][0])
print(offsetList)

offsetMean = np.mean(offsetList)
print(offsetMean)

