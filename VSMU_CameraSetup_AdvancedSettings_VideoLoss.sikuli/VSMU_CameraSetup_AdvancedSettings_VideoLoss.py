import time
from sikuli import *
from datetime import datetime
from c_Open_Vigil import Open_Vigil_A
from c_Open_VSMU import open_vsmu
from c_Validation_TextField import *
from c_Open_Vigil import c_Maximize
from c_Close_and_Open_Procedure import close_and_open_procedure
from c_Apply_VSMU_Cameras import apply
from t_dropdown_test import testRegionForChange, testRegionForMatch

expected_image = "expected_image.png"

def dropdownmenu_result(result, region_used):
    print("Test 1: Perform manual actions now if needed. Click OK when ready for final capture.")
    print("Test 1: Taking final capture of Region 1 and comparing...")
    result_tc1 = testRegionForChange(region_used, phase="final")
    if result_tc1 is not None:
        print("Test 1 Final Result: Region 1 {0} initial state. Test {1}.".format(
            "MATCHED" if result_tc1 else "DID NOT MATCH",
            "PASSED" if result_tc1 else "WARNING:FAILED (expected no change)"))
    else:
        print("Test 1 Final Result: Comparison failed.")

def image_check(result, region_used):
    print("Test 2: Initializing check for Region 2...")
    print("Test 2: Ensure Region 2 is in the state you want to verify against '{0}'. Click OK to proceed.".format(expected_image))
    print("Test 2: Taking final capture of Region 2 and comparing to pattern...")
    result_tc2 = testRegionForMatch(region_used, expected_image, phase="final")
    if result_tc2 is not None:
        print("Test 2 Final Result: Region 2 {0} expected image. Test {1}.".format(
            "MATCHED" if result_tc2 else "DID NOT MATCH",
            "PASSED" if result_tc2 else "WARNING:FAILED"))
    else:
        print("Test 2 Final Result: Comparison failed.")


def image_capture_n_check(Input_region, phaseinput, typeoftest):
    global expected_image
    if typeoftest == "preset_test":
        if phaseinput == "initial":
            initial_capture_ok = testRegionForChange(Input_region, phaseinput)
            return initial_capture_ok
    else:
        if phaseinput == "initial":
            initial_capture_ok = testRegionForChange(Input_region, phaseinput)
            return initial_capture_ok
    return None

def main():
    Open_Vigil_A()
    wait(10)
    open_vsmu()
    wait(4) 
    #Initial declaration_1.0
    regions_to_check = [
        ((841,737,140,29), "post_motion_record")    # Define the regions for text entry.
    ]    
    expected_data = {
        "post_motion_record": "1"     # Define the expected data as a dictionary.
    }
    #Initial_run_1.0
    click(Region(977,626,84,26)))#bcd
    wait(2)
    click(Region(959,741,39,35))#slider
    wait(2)
    click(Region(996,743,37,34))#rbc checkbox
    wait(0.4)
    click(Region(734,839,30,26)) #video loss trigger
    wait(1)
    click(Region(1216,839,97,26))#trigger
    wait(0.4)
    type(Key.UP)
    wait(0.4)
    type(Key.ENTER)
    wait(2)
    click(Region(1260,710,33,34))#video loss email notification
    wait(3)
    if Region(616,237,196,115).exists("1757435994882.png",10):
        click(Region(770,393,189,18))
        type("test subject")
        wait(2)
        click(Region(781,425,234,59))
        type("samplesample")
        wait(1)
        click(Region(1126,723,67,31))
        wait(4)
    #text_fields(regions_to_check, "initial", expected_data)     # Use text_fields to set the initial value.    
    videoloss_bcd = image_capture_n_check((925,712,72,25), "initial", "dropdown")     
    videoloss_slider = image_capture_n_check((956,738,43,41), "initial", "dropdown")
    videoloss_rbc = image_capture_n_check((997,743,32,30)), "initial", "dropdown")  
    videoloss_trigger = image_capture_n_check((1215,842,74,22)), "initial", "dropdown")    
    #secondary dropdown swap
    #Reboot_1.0
    #insert close all after checking status of close network
    close_and_open_procedure()
    #Final_check_1.0
    #text_fields(regions_to_check, "final", expected_data)     # Use text_fields to validate the final value
    dropdownmenu_result(videoloss_bcd, (925,712,72,25))
    dropdownmenu_result(videoloss_slider, (956,738,43,41))
    dropdownmenu_result(videoloss_rbc, (997,743,32,30))
    dropdownmenu_result(videoloss_trigger, (1215,842,74,22))
    #insert move class here then continue the repeat
    
main()