from serial import Serial
from datetime import datetime
import os, time, warnings
import pandas as pd
import kbhit
warnings.filterwarnings("ignore")

port = "/dev/ttyACM0"
def getDistance():
    distList=[]
    timeList=[]
    lx = kbhit.lxTerm()
    lx.start()

    ser = Serial(port, 115200)
    distIndex = 7
    print("DWM1001 Start\n")
    while True:
        res = ser.readline()
        dist= res.decode()[:len(res)-1].split(",")[distIndex]
        date = datetime.now()

        distList.append(dist[:len(dist)-1])
        timeList.append(date)
        print("[",date,"] ",dist)
        if lx.kbhit():
            c = lx.getch()
            c_ord = ord(c)
            if c_ord == 32: # ESC
                print("\nDWM1001 Stop")
                break
    lx.reset()
    toDistCSV(timeList, distList)

def toDistCSV(timeList, distList):
    dwmDf = pd.DataFrame({'time': timeList, 'distance': distList})
    now = datetime.now()
    fileName = str(now.strftime('%Y-%m-%d %H:%M:%S'))+".csv"
    
    os.chdir("Python-RPI-RTLS/csv/")
    dwmDf.to_csv(fileName, index=False)
    os.chdir("../../")
    
getDistance()