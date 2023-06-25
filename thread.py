import time
from threading import Thread

def funcOne():
    i = 0
    while True:
        print("funcOne ",i)
        i+=1
        time.sleep(1)

def funcTwo():
    i = 0
    while True:
        print("funcTwo", i)
        i+=1
        time.sleep(1)

process1 = Thread(target=funcOne, args=())
process2 = Thread(target=funcTwo, args=())

process1.start()
process2.start()