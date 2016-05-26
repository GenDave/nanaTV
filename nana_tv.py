## Nana tv v 2.0
#
# Button config
# 1 Pride and predudice
# 2 Bride and predudice
# 3 Andre Rieu
# 4 random

import os
import random
import subprocess
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)
GPIO.setup(17,GPIO.IN)
GPIO.setup(27,GPIO.IN)
GPIO.setup(22,GPIO.IN)

# 10 second start to exit nanatv
print("starting nanaTV in 10 seconds")
time.sleep(10)
print("starting nanaRV")

# Generate file list
extensionList = [".avi"] # list of allowed media file extensions.
mediaDir = '/home/pi/media/'
fileList = []
for root, dirnames, filenames in os.walk(mediaDir):
  for filename in filenames:
    if any([filename.endswith(ext) for ext in extensionList]):
      fileList.append(os.path.join(root, filename))

andreDir = '/home/pi/media/andre/'
andreList = []
for root, dirnames, filenames in os.walk(andreDir):
  for filename in filenames:
    if any([filename.endswith(ext) for ext in extensionList]):
      andreList.append(os.path.join(root, filename))

PrideFilm = '/home/pi/media/Pride_and_Prejudice.avi'
BrideFilm = '/home/pi/media/Bride_and_Prejudice.avi'

def getpin():
    # get gpio pin and return
    if (GPIO.input(4)):
        pinno = 1
    elif (GPIO.input(17)):
        pinno = 2
    elif (GPIO.input(27)):
        pinno = 3
    elif (GPIO.input(22)):
        pinno = 4
    else:
        pinno = 0
    return pinno
    
def playdata(fileList,playtype):
    selectedFile = random.choice(fileList)
    p = subprocess.Popen(["omxplayer","-b","-o" "hdmi",selectedFile])
    while p.poll() is None:
        pinno = getpin()
        if pinno != 0: 
            p.terminate()
            playtype = pinno
            break
        time.sleep(0.5)
    return playtype
    

playtype = 1
while True:
    if playtype == 1:
        playdata(fileList,1)
    elif playtype == 2:        
        playdata(andreDir,2)
    elif playtype == 3: 
        playdata(PrideFilm,1)
    elif playtype == 4:            
        playdata(BrideFilm,1)     
    else:
        break
    