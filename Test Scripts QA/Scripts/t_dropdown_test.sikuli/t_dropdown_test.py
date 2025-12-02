# --- t_dropdown_test.sikuli ---

# Import necessary Sikuli modules for Region object etc.
from sikuli import *
import time # Ensure time is imported if used directly (e.g., time.sleep)

# Import the compareRegionState function from c_Validation_Dropdown_Menu
from c_Validation_Dropdown_Menu import compareRegionState

# Define your region coordinates (can be overridden in the calling script)
TEST_REGION_A_COORDS = (80,303,66,80) # Example coordinates
TEST_REGION_B_COORDS = (300,50,200,100) # Another example region


# --- Helper Functions for Test Scenarios ---
_ongoing_test_states = {}

def testRegionForChange(region_coords, phase="full", name_of_field="unknown"):
    region_key = str(Region(region_coords[0], region_coords[1], region_coords[2], region_coords[3]))

    print("\n--- Testing Region {} for NO CHANGE (Phase: {}) ---".format(Region(region_coords[0], region_coords[1], region_coords[2], region_coords[3]), phase.upper()))

    if phase.lower() == "initial":
        print("Step 1: Capturing initial state of " + name_of_field)
        initial_ok = compareRegionState("initial", region_coords)
        _ongoing_test_states[region_key] = {"status": initial_ok, "result": None} # Store status
        if not initial_ok:
            print("WARNING: Test FAILED: Initial capture failed. Cannot proceed with comparison later.")
        return initial_ok # Return success of initial capture

    elif phase.lower() == "final":
        # Check if initial phase was run and was successful
        if region_key not in _ongoing_test_states or not _ongoing_test_states[region_key]["status"]:
            print("WARNING: Test FAILED: Initial capture was not successfully completed for this region. Cannot perform final comparison.")
            return None # Indicate failure


        print("Step 3: Capturing final state and comparing to initial...")
        comparison_result = compareRegionState("final", region_coords) # True if identical, False if different

        if comparison_result is None:
            print("WARNING: Test FAILED: Comparison could not be performed due to an error.")
            _ongoing_test_states[region_key]["result"] = None
        elif comparison_result: # If True (they are IDENTICAL)
            print("Test PASSED: Region states MATCH for the following field - " + name_of_field)
            _ongoing_test_states[region_key]["result"] = True
        else: # If False (they are DIFFERENT)
            print("WARNING: Test FAILED: Region states DO NOT MATCH for the following field - " + name_of_field)
            _ongoing_test_states[region_key]["result"] = False
        
        # Return the comparison result for the 'final' phase
        return _ongoing_test_states[region_key]["result"]

    elif phase.lower() == "full":
        # Combines initial, action, and final into one call
        initial_ok = testRegionForChange(region_coords, phase="initial")
        if not initial_ok:
            return None # Initial capture failed

        # Perform final comparison
        return testRegionForChange(region_coords, phase="final")
    else:
        raise ValueError("Invalid phase provided. Must be 'initial', 'final', or 'full'.")

    
def dropdownmenu_result(result, region_used):
    print "Test 1: Taking final capture of Region and comparing..."
    result_tc1 = testRegionForChange(region_used, phase="final")

    if result_tc1 is not None:
        print "Test 1 Final Result: Region {0} initial state. Test {1}.".format(
            "MATCHED" if result_tc1 else "DID NOT MATCH",
            "PASSED" if result_tc1 else "WARNING:FAILED (expected no change)")
        return result_tc1
    else:
        print "Test 1 Final Result: Comparison failed."
        return None


# --- Main Test Execution (for t_dropdown_test.sikuli itself) ---
if __name__ == "__main__":
    print("--- Starting Automated UI Tests from t_dropdown_test ---")

    # --- Test Case 1: Verify a region remains unchanged (split calls) ---
    print("\n--- TEST CASE 1: App Header Stability Check (Split Calls) ---")
    
    # 1. Initial Call
    print("Main Script: Test Case 1 Initial Call...")
    initial_ok = testRegionForChange(TEST_REGION_A_COORDS, phase="initial")

    if initial_ok:
        print("Main Script: Initial capture successful. Perform manual action now for TEST_REGION_A (or none if expecting no change).")
        time.sleep(5) # Simulate manual intervention period or long running action

        # 2. Final Call
        print("Main Script: Test Case 1 Final Call...")
        final_result_tc1 = testRegionForChange(TEST_REGION_A_COORDS, phase="final")

        if final_result_tc1 is not None:
            print("Main Script: Final Result for TEST_CASE_1: {}".format("MATCH" if final_result_tc1 else "NO MATCH"))
        else:
            print("WARNING: Main Script: Final Result for TEST_CASE_1: Comparison failed.")
    else:
        print("WARNING: Main Script: Test Case 1 initial call failed.")
