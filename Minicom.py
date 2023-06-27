import os

port = "/dev/ttyACM0"
# os.system("cd ../")
# os.system("minicom -D "+port+" -S ../Documents/Python-RPI-RTLS/MinicomScript.txt")
#minicom -D /dev/ttyACM0 -o timestamp=extended -C output.txt

os.system("minicom -D /dev/ttyACM0 -O timestamp=extended")