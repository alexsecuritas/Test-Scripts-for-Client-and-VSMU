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
    click(Region(538,117,85,25))#change to server
    #Initial declaration_1.0
    regions_to_check = [
        (Region(711,365,41,33), "screen_saver")    # Define the regions for text entry.
    ]    
    expected_data = {
        "screen_saver": "3"     # Define the expected data as a dictionary.
    }
    #Initial_run_1.0
    click(Region(448,300,35,33))#allow to detect
    wait(0.4)
    wait(2)
    text_fields(regions_to_check, "initial", expected_data)     # Use text_fields to set the initial value.    
    allow_to_detect = image_capture_n_check((448,300,35,33), "initial", "allow to detect")
    network_logging = image_capture_n_check((447,334,36,29), "initial", "network logging")
    redundant_server = image_capture_n_check((448,396,32,34), "initial", "Redundant server")
    user_audit = image_capture_n_check((447,398,35,30), "initial", "user audit")
    watchdog = image_capture_n_check((601,301,33,29), "initial","watchdog")
    show_ack_errors = image_capture_n_check((604,332,31,32), "initial", "show ack errors")
    screen_saver = image_capture_n_check((602,365,34,32), "initial", "screen saver")
    #Reboot_1.0
    #insert close all after checking status of close network
    close_and_open_procedure()
    #Final_check_1.0
    text_fields(regions_to_check, "final", expected_data)     # Use text_fields to validate the final value
    dropdownmenu_result(allow_to_detect, (448,300,35,33))
    dropdownmenu_result(network_logging, (447,334,36,29))
    dropdownmenu_result(redundant_server, (448,396,32,34))
    dropdownmenu_result(user_audit, (447,398,35,30))
    dropdownmenu_result(watchdog, (601,301,33,29))
    dropdownmenu_result(show_ack_errors, (604,332,31,32))
    dropdownmenu_result(screen_saver, (602,365,34,32))
    #insert move class here then continue the repeat
    
main()