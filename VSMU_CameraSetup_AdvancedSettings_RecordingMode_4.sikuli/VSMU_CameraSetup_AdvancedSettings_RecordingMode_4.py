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
            initial_capture_ok = testRegionForChange(Input_region, phaseinput) #this can be changed to testregionformatch if needed
            return initial_capture_ok
    return None

def main():
    Open_Vigil_A()
    wait(10)
    open_vsmu()
    wait(2) 
    #Initial declaration_1.0
    regions_to_check = [
        ((841,737,140,29), "post_motion_record")    # Define the regions for text entry.
    ]    
    expected_data = {
        "post_motion_record": "1"     # Define the expected data as a dictionary.
    }
    #Initial_run_1.0
    text_fields(regions_to_check, "initial", expected_data)     # Use text_fields to set the initial value.    
    alarm_only = image_capture_n_check((854,715,155,19), "initial", "dropdown")     # Corrected call to image_capture_n_check, passing a tuple of coordinates.
    click(Region(734,807,32,26))#enable video alarm BY clicking checkbox video motion alarm function
    click(Region(1152,749,64,29))#close motion alarm window
    click(Region(1312,805,33,33)) #Heatmap checkbox enable
    click(Region(856,715,131,18)) #selection
    type(Key.DOWN)
    wait(0.4)
    type(Key.DOWN)
    wait(0.4)
    type(Key.ENTER)
    #Not required - motion alarm check
    wait(2)
    #Reboot_1.0
    #insert close all after checking status of close network
    close_and_open_procedure()
    #Final_check_1.0
    text_fields(regions_to_check, "final", expected_data)     # Use text_fields to validate the final value
    dropdownmenu_result(alarm_only, (854,715,155,19))
    #insert move class here then continue the repeat
    
main()