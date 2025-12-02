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

# ----------------------------------------------------------------------
# COORDINATE DEFINITIONS (Tuples: x, y, w, h)
# ----------------------------------------------------------------------
# Tab Coordinates
C_VSMU_TAB                  = (538,117,85,25)
C_SECURITY_TAB              = (1132,246,69,27) # The Security Sub-Tab

# Checkbox Regions (Click/Comparison)
C_ALLOW_TO_DETECT_CLICK     = (457,332,32,29)
C_NETWORK_LOGGING_CLICK     = (457,365,30,26)

# Image Comparison Regions (Usually the same as click regions)
C_ALLOW_TO_DETECT_CHECK     = (457,332,32,29)
C_NETWORK_LOGGING_CHECK     = (457,365,30,26)

# Text Field Coordinates
C_PASSWORD_TEXTFIELD        = (706,330,33,34)
C_RETENTION_TEXTFIELD       = (705,366,36,25)

# ----------------------------------------------------------------------
# SIKULI REGION OBJECTS (Created by unpacking C_ tuples)
# ----------------------------------------------------------------------
R_VSMU_TAB                  = Region(*C_VSMU_TAB)
R_SECURITY_TAB              = Region(*C_SECURITY_TAB)
R_ALLOW_TO_DETECT_CLICK     = Region(*C_ALLOW_TO_DETECT_CLICK)
R_NETWORK_LOGGING_CLICK     = Region(*C_NETWORK_LOGGING_CLICK)

# ----------------------------------------------------------------------
# VSMU_TAB OBJECTS 
# ----------------------------------------------------------------------
allow_to_detect = vsmu_tab(
    tab_header="server_security", category="allow_to_detect", subcategory="none", submenu="none", status=True
)
network_logging = vsmu_tab(
    tab_header="server_security", category="network_logging", subcategory="none", submenu="none", status=True
)

# Combine all objects and their click regions into a dictionary for status saving
CHECKBOX_SETTINGS = {
    "allow_to_detect": (allow_to_detect, R_ALLOW_TO_DETECT_CLICK),
    "network_logging": (network_logging, R_NETWORK_LOGGING_CLICK),
}

# Initial declaration - Text Fields
regions_to_check = [
    # (Coordinates_Tuple, "Name_String", Associated_Region_For_Click/Check)
    (C_PASSWORD_TEXTFIELD,  "password",  C_PASSWORD_TEXTFIELD),
    (C_RETENTION_TEXTFIELD, "retention", C_RETENTION_TEXTFIELD),
]

# Array of expected values (must match the order of regions_to_check)
expected_data = [
    "10",
    "10",
]
# ----------------------------------------------------------------------

def main():
    # --- Setup ---
    Open_Vigil_A()
    wait(10)
    open_vsmu()
    wait(2)
    click(R_VSMU_TAB)        # Click server tab
    click(R_SECURITY_TAB)    # Click security sub-tab
    
    # Saves all current checkbox settings
    check_all_settings(CHECKBOX_SETTINGS)
    
    # --- Initial Run (Toggling and Setting Text Fields) ---
    print "Toggling checkboxes to change status..."

    # Checkbox Toggles (using R_ regions for clicking)
    click(R_ALLOW_TO_DETECT_CLICK)
    wait(0.4)
    click(R_NETWORK_LOGGING_CLICK)
    wait(2)
    
    # Text Field Initial Value Set (Using corrected iterator logic)
    for i, entry in enumerate(regions_to_check):
        value_to_pass = expected_data[i]
        textfield_iter(entry, value_to_pass)
    
    # Initial capture of the toggled state (using direct call to testRegionForChange)
    allow_to_detect_result = testRegionForChange(C_ALLOW_TO_DETECT_CHECK, "initial")
    network_logging_result = testRegionForChange(C_NETWORK_LOGGING_CHECK, "initial")

    # --- Reboot and Final Check ---
    close_and_open_procedure()
    
    # Re-navigate to the Security Tab
    click(R_VSMU_TAB)
    wait(2)
    click(R_SECURITY_TAB)
    
    # Final check: validation against initial capture
    # This loop runs for final validation of text fields
    for i, entry in enumerate(regions_to_check):
        field_name = entry[1]
        field_value = expected_data[i]
        
        # Repack the single item into a dictionary for the text_fields function
        temp_dict = {field_name: field_value}
        text_fields([entry], "final", temp_dict)

    # Final validation for checkboxes (using C_ coordinate tuples)
    dropdownmenu_result(allow_to_detect_result, C_ALLOW_TO_DETECT_CHECK)
    dropdownmenu_result(network_logging_result, C_NETWORK_LOGGING_CHECK)

main()