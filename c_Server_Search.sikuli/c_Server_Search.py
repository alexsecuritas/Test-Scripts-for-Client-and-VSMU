import os
import time
from sikuli import * 
import shutil
from datetime import datetime
from c_Playback_Separate_Page_Check import playback
def server_search(Play_tog): #Starts searching for footage   
    target_folder = r"\\capaldi\Testing Documents\_Automation_Logs\Captures\Settings\Startup_Display\Separate_Pages_For_Live_And_Playback"
    click(Region(128,51,41,38))
    popup("Waiting for client to connect to server- ensuring all footage loads", 10)
    startTime = time.time()
    while (time.time() - startTime) < 10:
        if not exists("1744206105799.png"):
            click(Region(128,51,48,43)) #Re-tries search button  
        if exists("1744206105799.png"):
            print("Search footage is open")
            break
    wait(2)
    click(Region(479,497,93,20))#allcam
    click(Region(530,294,217,21))#lasthour
    for i in range(7):
        type(Key.DOWN)
    type(Key.ENTER)
        
    click(Region(473,186,63,23)) #search button
    #Checks for search server errors
    if Region(694,379,561,295).exists("1744822044071.png") or Region(678,366,565,272).exists("1744822029705.png"):
        shutil.move(Screen(0).capture(Screen(0).getBounds()).getFile(), os.path.join(target_folder, "footage_on_server" + str(datetime.now().strftime("%H.%M.%S")) + ".png"))
        click(Region(988,570,82,20))
        shutil.move(Screen(0).capture(Screen(0).getBounds()).getFile(), os.path.join(target_folder, "footage_on_server_1" + str(datetime.now().strftime("%H.%M.%S")) + ".png"))

    if Region(736,441,446,150).exists("1744820021272.png"):
        print("Warning: Common error, could not find footage through search, there might be no existing footage from server")
        shutil.move(Screen(0).capture(Screen(0).getBounds()).getFile(), os.path.join(target_folder, "nf" + str(datetime.now().strftime("%H.%M.%S")) + ".png"))
        click(Region(1089,556,86,21))
        shutil.move(Screen(0).capture(Screen(0).getBounds()).getFile(), os.path.join(target_folder, "nf" + str(datetime.now().strftime("%H.%M.%S")) + ".png"))
       
    wait(0.5)
    doubleClick(Region(765,268,72,25)) #selects playback
    wait(3)
    if Play_tog == True:
        playback(True)

    if Play_tog == False:
        playback(False)
        