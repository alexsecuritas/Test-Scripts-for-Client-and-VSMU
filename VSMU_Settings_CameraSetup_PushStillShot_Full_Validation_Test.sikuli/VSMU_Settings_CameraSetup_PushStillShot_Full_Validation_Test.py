import time
from sikuli import *
from c_Open_Vigil import Open_Vigil_A
from c_Open_VSMU import open_vsmu
from datetime import datetime

now = datetime.now()
print("Current Time = " + now.strftime("%H:%M:%S"))

def Open_Vigil_B():
    try:
        startTime = time.time()
        while (time.time() - startTime) < 20:
            if exists("1745449182299.png") or exists("1745449190161.png"):
                print("Vigil Client Opened, Visual Check Confirm")
                break
            print("No Visual Check Confirmation for Vigil Client, Opening Vigil")
            Open_Vigil_A()
    except Exception:
        print("c_Open_Vigil failed")

Open_Vigil_B()

open_vsmu()

def settings():
    wait(2)
    if Region(1091,455,123,74).exists("1748828936849.png", 4):
        print("Push to still shot is already enabled")
    else:
        print("Enabling Push to still shot")
        click(Region(1096,487,35,30))
    click(Region(1397,486,74,33))
    
    if Region(734,320,284,148).exists("1748829079345.png",5):
        print("Push to still shot window is visible")
    else:
        print("Warning: window cannot be found, attempting again")
        click(Region(1397,486,74,33))
settings()
# Define Regions
type_regionData = Region(866,432,200,22)
path_regionData = Region(864,452,182,26)
username_regionData = Region(863,480,129,24)
password_regionData = Region(863,505,139,25)
ftp_timeout_regionData = Region(863,532,131,24)
update_frequency_regionData = Region(864,557,110,27)
overlay_text_checkbox = Region(853,577,44,42)
timestamp_checkbox = Region(847,609,57,45)

#Dropdown change
click(type_regionData) #type
wait(0.5)
for _ in range(2):
    type(Key.UP)
    wait(0.3)
type(Key.ENTER)
wait(1)
if Region(860,584,31,29).exists("1748961159893"):
    click(overlay_text_checkbox) #remove checkbox
    print("un-checking overlay box")
    wait(0.4)
if Region(860,618,32,25).exists("1748961159893"):
    click(timestamp_checkbox)
    print("un-checking timestamp box")
    
    
regions_to_capture = [
    (path_regionData, "path_regionData"),
    (username_regionData, "username_regionData"),
    (ftp_timeout_regionData, "ftp_timeout_regionData"),
    (update_frequency_regionData, "update_frequency_regionData")
]

# Update fields
wait(1)
for region, label in regions_to_capture:
    try:
        click(region)
        wait(0.3)
        type("a", Key.CTRL)
        wait(0.2)
        type("1")
        print("Field '%s' updated." % label)
    except Exception as e:
        print("Error updating '%s': %s" % (label, str(e)))

type_img = capture(type_regionData)
password_img = capture(password_regionData)
overlay_checkbox_img = capture(overlay_text_checkbox)
timestamp_checkbox_img = capture(timestamp_checkbox)

print("Type data stored")
click(password_regionData)
type("a", Key.CTRL)
type(Key.DELETE)
# Close settings
click(Region(1042,656,63,26))
wait(5)

from c_Close_Network_Camera_Settings import closenetwork
from c_Apply_VSMU_Cameras import apply
from c_Close_Vigil import closevig

closenetwork()
apply()
closevig()
wait(4)
Open_Vigil_A()
open_vsmu()
settings()
# Validate dropdown image
def dropdowncheck(locationR, imgR):
    start = time.time()
    count = 0
    while (time.time() - start) < 20:
        if locationR.exists(imgR):
            print("Successful: %s settings has not changed" % imgR)
            break
        elif count == 0:
            print("Warning: Settings has changed")
            count += 1

dropdowncheck(type_regionData, type_img)
dropdowncheck(password_regionData, password_img)
dropdowncheck(overlay_text_checkbox, overlay_checkbox_img)
dropdowncheck(timestamp_checkbox, timestamp_checkbox_img)

# Validate checkboxes
if Region(860,584,31,29).exists("1748961159893.png"):
    print("Warning: Overlay checkbox is still checked")
else:
    print("Success: Overlay box is unchecked")

if Region(860,618,32,25).exists("1748961159893.png"):
    print("Warning: Timestamp checkbox is still checked")
else:
    print("Success: Timestamp box is unchecked")

# Validate text fields
wait(1)
expected = "1"
for region, label in regions_to_capture:
    try:
        click(region)
        wait(0.3)
        type("a", Key.CTRL)
        wait(0.3)
        type("c", Key.CTRL)
        wait(0.5)
        current = unicode(App.getClipboard(), "utf-8").strip()
        if current != expected:
            print("%s: Mismatch - Found: '%s', Expected: '%s'" % (label, current, expected))
        else:
            print("%s: Match - Value is '%s'" % (label, current))
    except Exception as e:
        print("Error validating '%s': %s" % (label, str(e)))