
import pandas as pd
import numpy as np
import math, os, datetime, kbhit, time
from datetime import datetime
import time
import board
import adafruit_icm20x

analysisPath = "Python-RPI-RTLS/analysis_csv/"
accelPath = "Python-RPI-RTLS/accel_csv/"

def toCSV(path, fileName, df):
    os.chdir(path)
    df.to_csv(fileName, index=False)
    os.chdir("../../")


v_x=[]
v_y=[]
p_x=[]
p_y=[]


def Accelerometer():
    global v_x, v_y, p_x, p_y
    i2c = board.I2C()  # uses board.SCL and board.SDA
    icm = adafruit_icm20x.ICM20948(i2c)
    lx = kbhit.lxTerm()
    lx.start()
    x=[]
    y=[]
    z=[]

    v_x.append(0)
    v_y.append(0)
    p_x.append(0)
    p_y.append(0)

    dateList=[]
    i=0
    
    while True:
        date =datetime.now().strftime('%S.%f')
        print(icm.acceleration)
        x.append(icm.acceleration[0])
        y.append(icm.acceleration[1])
        z.append(icm.acceleration[2])
        dateList.append(float(date))
        
        if i != 0:
            position(dateList, x, y)
        else: 
            i+=1
         
        if lx.kbhit(): 
            c = lx.getch() 
            c_ord = ord(c)
            if c_ord == 32: # Spacebar
                print("\nStop")
                break 
        time.sleep(0.1)
    df = pd.DataFrame({"time": dateList,"x": x, "y": y, "z":z, "v_x": v_x, "v_y": v_y, "p_x": p_x, "p_y": p_y})
    toCSV(accelPath, "accel.csv", df)


# Initialization for system model.
A = 1
H = 1
Q = 0
R = 4

x_0 = 0
y_0 = 0
P_0 = 6
K_0 = 1
def Accelerometer2():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    icm = adafruit_icm20x.ICM20948(i2c)
    lx = kbhit.lxTerm()
    lx.start()
    y_esti,x_esti, P, K = None, None, None, None
    x_measList = []
    y_measList = []
    x_estiList = []
    y_estiList = []
    i = 0
    while True:
        x_mea = icm.acceleration[0]+0.186786123
        y_mea = icm.acceleration[1]+0.178759483
        print([x_mea, y_mea])
        if i == 0:
            y_esti, x_esti, P, K = y_0, x_0, P_0, K_0
            i+=1
        else:
            x_esti, P, K = kalman_filter(x_mea, x_esti, P)
            y_esti, P, K = kalman_filter(y_mea, y_esti, P)

        x_measList.append(x_mea)
        y_measList.append(y_mea)
        x_estiList.append(x_esti)
        y_estiList.append(y_esti)

        if lx.kbhit(): 
            c = lx.getch() 
            c_ord = ord(c)
            if c_ord == 32: # Spacebar
                print("\nStop")
                break 
        time.sleep(0.1)
    
    df = pd.DataFrame({"x": x_measList, "y": y_measList, "x_est":x_estiList, "y_est": y_estiList})
    toCSV(accelPath, "accel.csv", df)


def kalman_filter(z_meas, x_esti, P):
    """Kalman Filter Algorithm for One Variable.
       Return Kalman Gain for Drawing.
    """
    # (1) Prediction.
    x_pred = A * x_esti
    P_pred = A * P * A + Q

    # (2) Kalman Gain.
    K = P_pred * H / (H * P_pred * H + R)

    # (3) Estimation.
    x_esti = x_pred + K * (z_meas - H * x_pred)

    # (4) Error Covariance.
    P = P_pred - K * H * P_pred

    return x_esti, P, K

def Accelerometer3():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    icm = adafruit_icm20x.ICM20948(i2c)
    lx = kbhit.lxTerm()
    sensititivty=0.1
    lx.start()
    y_esti,x_esti, P, K = None, None, None, None
    x_measList = []
    y_measList = []

    x_estiList = []
    y_estiList = []
    dateList=[]

    v_x.append(0)
    v_y.append(0)
    p_x.append(0)
    p_y.append(0)
    i = 0
    while True:
        date =datetime.now().strftime('%S.%f')
        x_mea = icm.acceleration[0]+0.059855042
        y_mea = icm.acceleration[1]+0.238223065

        # x_mea = icm.acceleration[0]+0.186786123
        # y_mea = icm.acceleration[1]+0.178759483
        dateList.append(float(date))
        print([x_mea, y_mea])
        if i == 0:
            x_esti=x_mea
            y_esti=y_mea
            i+=1
        else:
            x_esti = x_esti * (1-sensititivty) + x_mea * sensititivty
            y_esti = y_esti * (1-sensititivty) + y_mea * sensititivty
            i+=1
            

        x_measList.append(x_mea)
        y_measList.append(y_mea)
        x_estiList.append(x_esti)
        y_estiList.append(y_esti)

        if i >= 2:
            position(dateList, x_estiList, y_estiList)


        if lx.kbhit(): 
            c = lx.getch() 
            c_ord = ord(c)
            if c_ord == 32: # Spacebar
                print("\nStop")
                break 
        time.sleep(1)
    
    df = pd.DataFrame({"date": dateList,"x": x_measList, "y": y_measList, "x_est":x_estiList, "y_est": y_estiList, "v_x": v_x, "v_y": v_y, "p_x":p_x, "p_y":p_y})
    toCSV(accelPath, "accel.csv", df)


def position(dateList, x, y):
    global v_x, v_y, p_x, p_y 
    diff_time = dateList[-1] - dateList[-2]
    
    velocity_x = v_x[-1] + 0.5 *(x[-1] + x[-2]) * (diff_time)
    velocity_y = v_y[-1] + 0.5 *(y[-1] + y[-2]) * (diff_time)
    
    v_x.append(velocity_x)
    v_y.append(velocity_y)

    position_x = p_x[-1] + 0.5 * (v_x[-1] + v_x[-2]) * diff_time
    position_y = p_y[-1] + 0.5 * (v_y[-1] + v_y[-2]) * diff_time

    p_x.append(position_x)
    p_y.append(position_y)

Accelerometer3()



