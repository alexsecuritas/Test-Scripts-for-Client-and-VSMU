import time
from sikuli import *
from datetime import datetime
from c_Open_Vigil import Open_Vigil_A
from c_Open_VSMU import open_vsmu
from c_Validation_TextField import text_fields, textfield_iter
from c_Open_Vigil import c_Maximize
from c_Close_and_Open_Procedure import close_and_open_procedure
from c_Apply_VSMU_Cameras import apply
from t_dropdown_test import testRegionForChange, dropdownmenu_result
from vsmu_class_dll import vsmu_tab
from c_Checkbox_check import check_all_settings


#The aim is not to use each settings individual status and alter them based on that
#but to test whether or not changing any setting saves, regardless of its original state
#the reset boolean file will utilize the txt file for reference to reset the variables
#to their original state, it can also be used to change any setting on or off using
#checkbox_check and vsmu_class_dll
# ----------------------------------------------------------------------
# COORDINATE DEFINITIONS (Tuples: x, y, w, h)
# ----------------------------------------------------------------------
# Tab Coordinates

C_VSMU_TAB                  = (538,117,85,25)
C_STARTUP                   = (524,249,69,27)

# Checkbox Regions (from the original script)
C_SENTINEL_CLICK_IF_OFF     = (449,305,34,26) 

C_ALERT_IF_NO_FOOTAGE       = (450,332,30,32)
C_ALERT_IF_NO_FOOTAGE_TXT   = (652,339,38,26)
C_KIOSK_CLICK_IF_OFF        = (444,366,41,43)

C_HIDE_TITLE_BAR            = (478,409,26,26)
C_HIDE_MIN_MAX_BUTTONS      = (480,449,24,22)
C_SCHEDULED_REBOOT          = (448,505,51,44)
C_SCHEDULED_LAPSE           = (612,543,64,27)
C_ONLY_ON_DAY               = (459,573,26,25)
C_ONLY_ON_DAY_DATE          = (613,572,73,27)
C_ONLY_ON_DURING_HOUR       = (459,605,25,21)
C_ONLY_ON_DURING_HOUR_CR    = (624,605,103,27)
C_ONLY_ON_DURING_HOUR_CR_2  = (746,603,107,29)
C_LOGIN_LIMIT               = (898,307,25,27)
# ----------------------------------------------------------------------
# SIKULI REGION OBJECTS
# ----------------------------------------------------------------------          
for var_name, var_value in globals().copy().items():
    if var_name.startswith("C_") and isinstance(var_value, tuple):
        r_var_name = var_name.replace("C_", "R_", 1)
        globals()[r_var_name] = Region(*var_value)
        
#DROPDOWN MENU ARRAY
dropdown_items = [
    "ALERT_IF_NO_FOOTAGE",
    "SENTINEL_CLICK_IF_OFF",
    "KIOSK_CLICK_IF_OFF",
    "HIDE_TITLE_BAR",
    "HIDE_MIN_MAX_BUTTONS",
    "SCHEDULED_REBOOT",
    "ONLY_ON_DAY",
    "ONLY_ON_DAY_DATE",
    "ONLY_ON_DURING_HOUR",
    "LOGIN_LIMIT"
]
# ----------------------------------------------------------------------
# VSMU_TAB OBJECTS (Defining for the actual checkboxes being clicked)
# ----------------------------------------------------------------------
sentinel_on_startup = vsmu_tab(
    tab_header="server_startup", category="sentinel_on_startup", subcategory="none", submenu="none", status=False
)
alert_if_no_footage = vsmu_tab(
    tab_header="server_startup", category="alert_if_no_footage", subcategory="none", submenu="none", hierarchy="child", status=False, linked=sentinel_on_startup, linked_status=sentinel_on_startup.status
)
kiosk_mode = vsmu_tab(
    tab_header="server_startup", category="kiosk_mode", subcategory="reboot_warning", submenu=Region(925,552,75,32), status=False
)
hide_title_bar = vsmu_tab(
    tab_header="server_startup", category="hide_title_bar", subcategory="none", submenu="none", hierarchy="child", status=False, linked=kiosk_mode,  linked_status=kiosk_mode.status
)
hide_min_max_buttons = vsmu_tab(
    tab_header="server_startup", category="hide_min_max_buttons", subcategory="none", submenu="none", hierarchy="child", status=False, linked=kiosk_mode,  linked_status=kiosk_mode.status
)
scheduled_reboot = vsmu_tab(
    tab_header="server_startup", category="scheduled_reboot", subcategory="none", submenu="none", hierarchy="parent", status=False
)
only_on_day = vsmu_tab(
    tab_header="server_startup", category="only_on_day", subcategory="none", submenu="none", hierarchy="child", status=False, linked=scheduled_reboot,  linked_status=scheduled_reboot.status
)
only_during_hour = vsmu_tab(
    tab_header="server_startup", category="only_during_hour", subcategory="none", submenu="none", hierarchy="child", status=False, linked=scheduled_reboot,  linked_status=scheduled_reboot.status
)
logon_limit = vsmu_tab(
    tab_header="server_startup", category="logon_limit", subcategory="none", submenu="none", hierarchy="parent", status=False
)
# Combine all objects and their click regions into a dictionary for status saving
# NOTE: Using the CLICK regions as the regions to check status on.
CHECKBOX_SETTINGS = {
    "sentinel_on_startup": (sentinel_on_startup, R_SENTINEL_CLICK_IF_OFF),
    "alert_if_no_footage": (alert_if_no_footage, R_ALERT_IF_NO_FOOTAGE),
    "kiosk_mode": (kiosk_mode, R_KIOSK_CLICK_IF_OFF),
    "hide_title_bar": (hide_title_bar, R_HIDE_TITLE_BAR),
    "hide_min_max_buttons": (hide_min_max_buttons, R_HIDE_MIN_MAX_BUTTONS),
    "scheduled_reboot": (scheduled_reboot, R_SCHEDULED_REBOOT),
    "logon_limit": (logon_limit, R_LOGIN_LIMIT),
}

# Initial declaration - Text Fields
regions_to_check = [
    # (Coordinates_Tuple, "Name_String", Associated_Region_For_Click/Check)
    (C_ALERT_IF_NO_FOOTAGE_TXT, "alert_if_no_footage", C_ALERT_IF_NO_FOOTAGE),
    (C_SCHEDULED_LAPSE, "scheduled_reboot_lapse", C_SCHEDULED_REBOOT),
]

# Array of expected values (must match the order of regions_to_check)
expected_data = [
    "24",
    "90",
]
# ----------------------------------------------------------------------

def main():
    # --- Setup ---
    Open_Vigil_A()
    wait(10)
    open_vsmu()
    wait(2)
    click(R_VSMU_TAB) # Click server tab (assumes startup is default)
    wait(2)
    click(R_STARTUP)    
    # Saves all current checkbox settings (Sentinel, Network Logging, Kiosk)
    save_all_settings(CHECKBOX_SETTINGS)
    
    # --- Initial Run (Toggling Settings) ---
    print "Toggling checkboxes to change status..."
    # Sentinel Checkbox Logic (Must preserve the IF/ELSE structure)
    if R_SENTINEL_CLICK_IF_OFF.exists("1757607137110.png",4):
        print "Sentinel already ON, continuing."
        # No action needed if ON, status already saved by check_all_settings
    else:
        # Click the region to toggle it ON
        click(R_SENTINEL_CLICK_IF_OFF)
        print "Sentinel toggled ON."

    # Kiosk Checkbox Logic (Must preserve the IF/ELSE structure)
    if R_KIOSK_CLICK_IF_OFF.exists("1757607232251.png",4):
        print "Kiosk already ON, continuing."
    else:
        # kiosk = True # This variable is not used in the final check, removing
        click(R_KIOSK_CLICK_IF_OFF)
        print "Kiosk toggled ON."
        wait(2)
        click(kiosk_mode.submenu)
        
    if R_SCHEDULED_REBOOT.exists("1757607232251.png",4):
        print "Scheduled reboot is already ON, continuing."
    else:
        click(R_SCHEDULED_REBOOT)
        print "Scheduled reboot is toggled ON."
        
    wait(0.4)
    click(R_HIDE_TITLE_BAR)
    wait(0.4)
    click(R_HIDE_MIN_MAX_BUTTONS)
    wait(2)
    click(R_LOGIN_LIMIT)
    wait(0.4)
    click(R_ONLY_ON_DAY)
    # Text Field Initial Value Set
    for i, entry in enumerate(regions_to_check):
        value_to_pass = expected_data[i]
        textfield_iter(entry, value_to_pass)
    
    # Initial capture of the toggled state (using direct call to testRegionForChange)
    # Mapping the old capture variables to the correct new C_ coordinates:
    for item_name in dropdown_items:
        c_var_name = "C_" + item_name
        result_var_name = item_name.lower()
        c_variable = globals()[c_var_name]
        globals()[result_var_name] = testRegionForChange(c_variable, "initial")

    # --- Reboot and Final Check ---
    #close_and_open_procedure()
    apply()
    wait(2)
    open_vsmu()
    # Re-navigate to the Server/Startup Tab
    click(R_VSMU_TAB)
    wait(2)
    click(R_STARTUP)
    # Final check: validation against initial capture (Text Fields)
    for i, entry in enumerate(regions_to_check):
        field_name = entry[1]
        field_value = expected_data[i]
        
        # Repack the single item into a dictionary for the text_fields function
        temp_dict = {field_name: field_value}
        text_fields([entry], "final", temp_dict)

    # Final validation for checkboxes (using C_ coordinate tuples)
    # Mapping the old dropdown_result calls to the correct new C_ coordinates:
    for item_name in dropdown_items:
        c_var_name = "C_" + item_name
        result_var_name = item_name.lower() + "_result"
        c_variable = globals()[c_var_name]
        globals()[result_var_name] = dropdownmenu_result(result_var_name, c_variable)

main()