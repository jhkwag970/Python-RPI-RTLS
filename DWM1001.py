from serial import Serial
from datetime import datetime
import os, time, warnings
import pandas as pd
import kbhit, math
warnings.filterwarnings("ignore")

port = "/dev/ttyACM0"
def getDistance():
    distList=[]
    timeList=[]
    lx = kbhit.lxTerm()
    lx.start()

    ser = Serial(port, 115200)
    distIndex = 7
    dateIndex = 0
    timeCnt = 0
    print("DWM1001 Start\n")
    while True:
        res = ser.readline()
        dist= res.decode()[:len(res)-1].split(",")[distIndex]

        if len(dist) == 0:
            print("Data Stop")
            timeCnt+=1
            time.sleep(0.5)
            continue
        else:
            if(timeCnt > 0):
                print("Data Return")
            timecnt = 0

        date = datetime.now()

        distList.append(dist[:len(dist)-1])
        timeList.append(date)
        print("[",date,"] ",dist) 

        if stopLogging(lx):
            break

        if timeCnt == 10:
            print("Stop Loggin Enabled")
            if stopLogging(lx):
                break
        
    lx.reset()
    toDistCSV(timeList, distList)

def stopLogging(lx):
    if lx.kbhit():
        c = lx.getch()
        c_ord = ord(c)
        if c_ord == 32: # Spacebar
            print("\nDWM1001 Stop")
            return True

def toDistCSV(timeList, distList):
    dwmDf = pd.DataFrame({'time': timeList, 'distance': distList})
    now = datetime.now()
    fileName = str(now.strftime('%Y-%m-%d %H:%M:%S'))+".csv"
    
    os.chdir("dwm1001_csv/")
    dwmDf.to_csv(fileName, index=False)
    #os.chdir("../../")

def changeDir():
    os.chdir("/home/pi/Documents/Python-RPI-RTLS")

changeDir()    
getDistance()



 