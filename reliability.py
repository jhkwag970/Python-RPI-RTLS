from datetime import datetime
import pandas as pd


timeIndex=24
path="Python-RPI-RTLS/final_csv/"
format = '%Y-%m-%d %H:%M:%S.%f' 
def rel_test(csv):
    csv_1 = pd.read_csv(path+csv)
    max = csv_1["time"].max()
    min = csv_1["time"].min()
    num_max = datetime.strptime(max,format)
    num_min = datetime.strptime(min,format)
    diff = str(num_max-num_min)

    min = int(diff.split(":")[1]) * 120
    sec = float(diff.split(":")[2]) *2
    
    total = min + sec
    reliabiltiy = csv_1["time"].size / total
    # print(diff)
    # print(total)
    # print(csv_1["Date"].size)
    print(reliabiltiy)

rel_test("2023-07-06 21:31:06.csv")
rel_test("2023-07-06 21:40:24.csv")
rel_test("2023-07-06 22:25:57.csv")