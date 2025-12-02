import time
from sikuli import *
from c_Open_Vigil import Open_Vigil_A
from datetime import datetime
from c_Server_Search import server_search

# --- Configuration and Regions ---
print "Current Time =" + datetime.now().strftime("%H:%M:%S")
timeout = 20
runc = 0
count = 0
vidtype = 0
No_footage = False

# Regions for playback
playback_submenu_Rc = Region(913,463,267,162)
quick_search = Region(1080,681,149,15)
search = Region(1289,682,102,18)
one_minute = Region(1294,705,101,17)
five_min = Region(1291,727,81,18)
ten_min = Region(1293,749,86,17)
instant_replay = Region(1290,770,95,17)

# After quick search is selected
camera_menu = Region(947,469,156,106)
rcsavestillimageormotionvideo = Region(1046,528,202,13)
Still_Image = Region(1301,529,186,15)
Bitmap = Region(1543,529,133,18)
JPG = Region(1527,553,148,18)
AVI_Video = Region(1304,554,93,20)
AVI_Video_Rapid_Stream = Region(1297,578,172,17)
Authentic_Video = Region(1297,601,141,16)
Authentic_Video_Rapid_Stream = Region(1298,623,190,16)
audio_as_WAV_file = Region(1301,645,169,16)

# Map export types to their region objects and friendly names
EXPORT_OPTIONS = [
    ("AVI", AVI_Video, 0),
    ("AVI_Video_Rapid_Stream", AVI_Video_Rapid_Stream, 1),
    ("Authentic_Video", Authentic_Video, 2),
    ("Authentic_Video_Rapid_Stream", Authentic_Video_Rapid_Stream, 3),
    ("Still_Image_JPG", JPG, 4),
    ("Still_Image_Bitmap", Bitmap, 5),
]
# --- Functions ---
def connect_to_server():
    global count, vidtype
    wait(1)
    doubleClick(Region(44,166,59,16))
    print "Server has been connected"
    wait(2)

def export_footage_end():
    global count, vidtype
    
    # Wait for the export button to be found
    start_time = time.time()
    export_btn_found = False
    while time.time() - start_time < 30:
        if Region(673,309,270,136).exists("1738787754499.png"):
            print "Attempting to export"
            print "Current Time = " + datetime.now().strftime("%H:%M:%S")
            try:
                click("1756990868895.png", 10)
            except:
                print "WARNING: issue with clicking the ok button when exporting - common, this occurs because the window is in a different depending on export type or vigil version times"
                print "There are alternate files that take into account the positioning, but that positioning changes depending on update as well"
            export_btn_found = True
            break
    
    if not export_btn_found:
        print "WARNING: Export button not found within timeout. Force clicking region"
        print "Current Time = " + datetime.now().strftime("%H:%M:%S")
        click(Region(994,667,77,15))

    # Wait for file overwrite prompt
    start_time = time.time()
    while time.time() - start_time < 30:
        if exists("1736962291786.png"):
            # If prompt exists, handle it
            click(Region(967,543,70,20))
            wait(0.2)
            click(Region(929,544,62,17))  # Confirms duplicate file exists
            wait(0.2)
            click(Region(815,588,243,15))
            break
        else:
            # If no overwrite prompt, proceed.
            print "No overwrite prompt found, continuing."
            break
            
    # Use the a list to select the video type region
    # This logic has been slightly altered to fit the loop in the main section.
    # The `vidtype` global variable is still used to track the current type.
    
    # Find the correct region from EXPORT_OPTIONS using the global vidtype
    region_to_click = None
    for name, region, vid_num in EXPORT_OPTIONS:
        if vid_num == vidtype:
            region_to_click = region
            break

    if region_to_click:
        click(region_to_click)
    else:
        print "WARNING: Unknown video type number: " + str(vidtype)
        return

    # Handle renaming the file
    if Region(711,334,150,52).exists("1754884377512.png") or exists("1754884398471.png"):
        current_vid_name = None
        for name, region, vid_num in EXPORT_OPTIONS:
            if vid_num == vidtype:
                current_vid_name = name
                break  

        if current_vid_name:
            click(Region(877,535,92,36))
            type(current_vid_name)
            print "Typing video type: " + current_vid_name
        wait(2)

        click(Region(868,430,213,15))#name
        type("Test")
        click(Region(868,481,236,14))#password
        type("Vigil123") #add a password cycle here
        click(Region(1012,693,96,35))#confirm
        if Region(765,476,66,106).exists("1754888475876.png"):
            print("The user supplied dodes not have permissions to export footage.")
            click(Region(917,559,83,28))#confirm new pop up
            click(Region(868,481,236,14))#password
            type("vigil123")

            click(Region(1012,693,96,35))#confirm
        
        wait(7)
        type("a", KeyModifier.CTRL)
        print "Renaming file"
        type(Key.DELETE)
        count += 1
        type("videofile_" + str(count))
        print "Confirming new file"
        click(Region(996,667,74,16))
        
        # Check for overwrite prompt again
        try:
            start_time = time.time()
            while time.time() - start_time < 3:
                if exists("1736962291786.png"):
                    click(Region(877,538,81,29))
                    print "Previous file with same name overwritten"
                    break
        except:
            print "WARNING: No files overwritten"
            
    # Final export status check
    ix = 0
    start_time = time.time()
    while time.time() - start_time < 2000:
        if exists("1738888299836.png"):
            if ix < 1:
                print "Process started at ", datetime.now().strftime("%H:%M:%S")
                ix += 1
        if exists("1738778620986.png"):
            click(Region(1005,557,81,22))
            print "Export successfully finished, confirm closed", datetime.now().strftime("%H:%M:%S")
            return
        time.sleep(1)
    
    print "WARNING: Export failed"


def export_video(typeofvid, vidtypenumber):
    global vidtype
    rightClick(camera_menu)
    wait(0.5)
    hover(rcsavestillimageormotionvideo)
    print "Selecting video type export"
    wait(0.5)
    vidtype = vidtypenumber
    if vidtype == 4 or vidtype == 5:
        hover(Still_Image)
    click(typeofvid)
    export_footage_end()

# --- Main execution ---
Open_Vigil_A()
wait(8)
connect_to_server()
server_search(True)
wait(3)
# Use a loop to iterate through the export options
for name, region, vid_num in EXPORT_OPTIONS:
    print "Exporting {0}".format(name)
    export_video(region, vid_num)
