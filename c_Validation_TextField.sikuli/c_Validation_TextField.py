import time
from sikuli import *

def text_fields(regions_to_check, phase, expected_data=None):
    print("Entering '{0}' state to {1} fields".format(phase, "update" if phase == "initial" else "validate"))
    
    for region_entry in regions_to_check:
        # Unpack the coordinate tuple and the field name
        region_coords = region_entry[0]
        name = region_entry[1]
        region = Region(*region_coords)
        
        try:
            expected_value = expected_data.get(name, "")
            
            if phase == "initial":
                print("Updating field '{0}' with: '{1}'".format(name, expected_value))
                region.click(); wait(0.5)
                type("a", Key.CTRL); wait(0.3)
                type(expected_value)
                
            elif phase == "final":
                print("Validating field '{0}'...".format(name))
                region.click(); wait(0.5)
                type("a", Key.CTRL); wait(0.3)
                type("c", Key.CTRL); wait(0.5)
                
                current_value = App.getClipboard().strip()
                
                if current_value == expected_value:
                    print("  - PASSED: Field '{0}' matched. Found: '{1}'".format(name, current_value))
                else:
                    print("  - FAILED: Field '{0}' MISMATCH! Found: '{1}', Expected: '{2}'".format(name, current_value, expected_value))
        
        except Exception as e:
            print("An error occurred while processing field '{0}': {1}".format(name, e))
