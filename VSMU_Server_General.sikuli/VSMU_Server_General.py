import time
from sikuli import *
from datetime import datetime
from c_Open_Vigil import Open_Vigil_A
from c_Open_VSMU import open_vsmu
# The textfield_iter function is no longer needed
from c_Validation_TextField import text_fields
from c_Open_Vigil import c_Maximize
from c_Close_and_Open_Procedure import close_and_open_procedure
from c_Apply_VSMU_Cameras import apply
from t_dropdown_test import testRegionForChange, dropdownmenu_result
from vsmu_class_dll import VsmuTab
from c_Checkbox_check import save_all_settings
from c_Reset_VSMU_State import reset_ui_to_saved_state



# ----------------------------------------------------------------------
# COORDINATE DEFINITIONS (Tuples: x, y, w, h)
# ----------------------------------------------------------------------
C_VSMU_TAB          = (538,117,85,25)
C_ALLOW_AUTO_DETECT = (448,300,35,33)
C_NETWORK_LOGGING   = (450,332,30,32)
C_REDUNDANT_SERVER  = (448,396,32,34)
C_USER_AUDIT        = (447,398,35,30)
C_WATCHDOG          = (601,301,33,29)
C_SHOW_ACK_ERRORS   = (604,332,31,32)
C_SCREEN_SAVER      = (602,365,34,32)
C_SCREEN_TEXTFIELD  = (713,366,42,29)


# ----------------------------------------------------------------------
# SIKULI REGION OBJECTS
# ----------------------------------------------------------------------          
for var_name, var_value in globals().copy().items():
    if var_name.startswith("C_") and isinstance(var_value, tuple):
        r_var_name = var_name.replace("C_", "R_", 1)
        globals()[r_var_name] = Region(*var_value)


        
# vsmu_tab Object Initializations
allow_auto_detect = VsmuTab(tab_header="server_general", category="allow_auto_detect", submenu="none", status=True)
network_logging = VsmuTab(tab_header="server_general", category="network_logging", submenu="none", status=True)
redundant_server = VsmuTab(tab_header="server_general", category="redundant_server", submenu="none", status=True)
user_audit = VsmuTab(tab_header="server_general", category="user_audit", submenu="user_performance_criteria", status=True)
watchdog = VsmuTab(tab_header="server_general", category="watchdog", submenu="test_watchdog", status=True)
show_acknowledgeable_errors = VsmuTab(tab_header="server_general", category="show_acknowledgeable_errors", submenu="none", status=True)
screen_saver = VsmuTab(tab_header="server_general", category="screen_saver", submenu="none", status=True)

# Settings Dictionary
CHECKBOX_SETTINGS = {
    "allow_auto_detect": (allow_auto_detect, R_ALLOW_AUTO_DETECT),
    "network_logging": (network_logging, R_NETWORK_LOGGING),
    "redundant_server": (redundant_server, R_REDUNDANT_SERVER),
    "user_audit": (user_audit, R_USER_AUDIT),
    "watchdog": (watchdog, R_WATCHDOG),
    "show_acknowledgeable_errors": (show_acknowledgeable_errors, R_SHOW_ACK_ERRORS),
    "screen_saver": (screen_saver, R_SCREEN_SAVER),
}
# Initial declaration - Text Comparison

regions_to_check = [
    (C_SCREEN_TEXTFIELD, "screen_saver", screen_saver)  
]
expected_data = ["5"]

def main():
    # --- Setup and Initial Save ---
    Open_Vigil_A()
    wait(10)
    open_vsmu()
    wait(2)
    click(R_VSMU_TAB) # Click server-tab
    # Saves all current settings - This OVERWRITES the file every time.
    save_all_settings(CHECKBOX_SETTINGS)
    # --- Initial Run (Toggling Settings) ---
    print "Toggling checkboxes to change status..."

    click(R_ALLOW_AUTO_DETECT)
    wait(0.4)
    click(R_NETWORK_LOGGING)
    wait(0.4)
    click(R_REDUNDANT_SERVER)
    wait(0.4)
    click(R_USER_AUDIT)
    wait(0.4)
    click(R_WATCHDOG)
    wait(0.4)
    click(R_SHOW_ACK_ERRORS)
    wait(0.4)    
    # --- MODIFIED: Text Field Logic ---
    for i, entry in enumerate(regions_to_check):
        field_coords, field_name, governing_object = entry
        
        # 1. EFFICIENT PARENT CHECK
        if governing_object and governing_object.hierarchy == "child":
            parent_region = find_region_for_object(governing_object.linked_parent)
            if parent_region and not parent_region.exists("1761172727910.png"):
                print "INFO: Parent '{}' is OFF. Clicking to enable for '{}' test.".format(governing_object.linked_parent.category, field_name)
                click(parent_region)
                wait(0.5)

        # 2. DIRECTLY CALL text_fields FOR THE CURRENT ITEM
        current_item_list = [entry]
        current_expected_dict = {field_name: expected_data[i]}
        text_fields(current_item_list, "initial", current_expected_dict)
    # Checkbox initial captures
    allow_to_detect = testRegionForChange(C_ALLOW_AUTO_DETECT, "initial", "allow to detect")
    network_logging = testRegionForChange(C_NETWORK_LOGGING, "initial", "network logging")
    redundant_server = testRegionForChange(C_REDUNDANT_SERVER, "initial", "Redundant server")
    user_audit = testRegionForChange(C_USER_AUDIT, "initial", "user audit")
    watchdog = testRegionForChange(C_WATCHDOG, "initial","watchdog")
    show_ack_errors = testRegionForChange(C_SHOW_ACK_ERRORS, "initial", "show ack errors")
    screen_saver = testRegionForChange(C_SCREEN_SAVER, "initial", "screen saver")

    # --- Reboot and Final Check ---
    close_and_open_procedure()
    #VSMU TAB
    click(R_VSMU_TAB)
    # Final validation loop
    for i, entry in enumerate(regions_to_check):
        field_name = entry[1]
        temp_dict = {field_name: expected_data[i]}
        text_fields([entry], "final", temp_dict)

    # dropdownmenu_result receives the coordinate tuple, not the Region object
    dropdownmenu_result(allow_to_detect, C_ALLOW_AUTO_DETECT)
    dropdownmenu_result(network_logging, C_NETWORK_LOGGING)
    dropdownmenu_result(redundant_server, C_REDUNDANT_SERVER)
    dropdownmenu_result(user_audit, C_USER_AUDIT)
    dropdownmenu_result(watchdog, C_WATCHDOG)
    dropdownmenu_result(show_ack_errors, C_SHOW_ACK_ERRORS)
    dropdownmenu_result(screen_saver, C_SCREEN_SAVER)
        
    # Reset UI to original state
    print "\n--- Resetting UI to Original State ---"
    reset_ui_to_saved_state(CHECKBOX_SETTINGS)
    print "--- Test Complete ---"

main()