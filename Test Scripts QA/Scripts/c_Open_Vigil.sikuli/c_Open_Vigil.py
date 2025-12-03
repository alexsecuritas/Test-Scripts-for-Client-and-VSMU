from sikuli import *
from time import sleep
import os
import subprocess
import sys
# --- Sikuli Functions ---
def c_Maximize():
    if exists("1726809870377.png"):
        rightClick("1726809870377.png")
        wait(0.4)
    if exists("1726810427408.png"):
        click("1726831585922.png")
        wait(0.4)
        
def c_Open_Vigil_B():
    config = {
        "appPath": r"C:\Program Files (x86)\Vigil\VIGIL Client\VIGIL Client.exe",
    }
    try:
        subprocess.Popen(config["appPath"])
        print("Vigil Client launched successfully.")
        wait(0.4)
    except FileNotFoundError:
        print("Error: Vigil Client executable not found at ", config["appPath"])
    except Exception as e:
        print("An unexpected error occurred while launching Vigil Client:", e)

def Open_Vigil_A():
    vigil_open_image = "vigil_open_image.png"
    try:
        if Region(220,4,485,141).exists(vigil_open_image, 2):
            print("Vigil Client Opened, Visual Check -> Successful")            
        else:
            print("No Visual Check Confirmation for Vigil Client, Opening Vigil")
        c_Open_Vigil_B()
    except Exception:
        print("c_Open_Vigil failed")
        
if __name__=="__main__":
    Open_Vigil_A()