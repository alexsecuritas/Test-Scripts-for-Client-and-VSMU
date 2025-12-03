import time
from sikuli import *
def closevig():
    click(Region(1873,0,44,20))
    startTime = time.time()
    while (time.time() - startTime) < 20:
        
        if exists("1739398814203.png"):
            print("Closing Vigil by selecting yes")
            click(Region(984,570,87,22))
            return 0
if __name__ == "__main__":
    closevig()