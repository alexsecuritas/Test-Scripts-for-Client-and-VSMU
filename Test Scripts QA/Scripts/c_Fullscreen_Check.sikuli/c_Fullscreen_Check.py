import time
from sikuli import * 
from datetime import datetime
import os
def fullscreen_check():
    startTime = time.time()
    while (time.time() - startTime) < 20: 
        if (not Region(62,49,488,59).exists("1744752914300.png")) and Region(286,985,169,94).exists("1744754850803.png"):
            print("Fullscreen mode on, switching off")
            click(Region(347,1013,33,29))
            wait(5)
            break
        if Region(62,49,488,59).exists("1744752914300.png") and not Region(286,985,169,94).exists("1744754850803.png"):
            print("Fullscreen mode off, continuing test")
            break