import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
 
plt.style.use('fivethirtyeight')
 
x_val = []
y_val = []
c_val = []
index = count()

def animate(i):
    if (next(index) == 0):
        x = 0
        y = 0
        c_val.append("red")
    else:
        x = random.uniform(100, -100)
        y = random.uniform(100, -100)
        c_val.append("green")

    x_val.append(x)
    y_val.append(y)
    plt.cla()
    plt.scatter(x_val, y_val, color=c_val)
    
 
# ani = FuncAnimation(plt.gcf(), animate, interval = 1000) 

# plt.tight_layout()
# plt.show()

#----Version 2---------------------------------------

idx = 0

while True:
    if idx == 0:
        x = 0
        y = 0
        c = "red"
    elif idx == 360:
        break
    else:
        x = random.uniform(100, -100)
        y = random.uniform(100, -100)
        c = "green"

    plt.scatter(x, y, color = c)
    plt.pause(1)
    idx+=1


plt.show()