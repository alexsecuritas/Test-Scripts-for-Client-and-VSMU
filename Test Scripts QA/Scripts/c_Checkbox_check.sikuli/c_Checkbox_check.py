import time
from sikuli import *

def checkbox(vsmu_object, checkboxregion, name):
    if checkboxregion.exists("1758898967925.png"):
        vsmu_object.set_status(True)
        with open("vsmu_status.txt", "a") as f: f.write(str(vsmu_object) + "\n")
        print "Checked setting: %s" % name
    else:
        vsmu_object.set_status(False)
        with open("vsmu_status.txt", "a") as f: f.write(str(vsmu_object) + "\n")
        print "Un-checked setting: %s" % name
        
def save_all_settings(settings_dict, command="none"):
    with open("vsmu_status.txt", "w") as f: f.write("")
    for name, (obj, region) in settings_dict.iteritems():
        checkbox(obj, region, name)
    print "Initial status of all settings captured and saved (overwritten)."

def load_settings_from_file(settings_dict, filename="vsmu_status.txt"):
    print "Attempting to load settings from %s..." % filename
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except IOError:
        print "Info: Status file '%s' not found. Will use default object statuses." % filename
        return 
    
    header_to_object_map = {obj.tab_header: obj for name, (obj, region) in settings_dict.iteritems()}

    for line in lines:
        line = line.strip()
        if not line:
            continue 
        try:
            attrs = dict(item.split('=', 1) for item in line.split(', '))
            
            tab_header = attrs.get('tab_header')
            status_str = attrs.get('status')

            if tab_header is None or status_str is None:
                print "Warning: Malformed line, skipping: %s" % line
                continue

            new_status = (status_str == 'True')

            if tab_header in header_to_object_map:
                vsmu_object = header_to_object_map[tab_header]
                vsmu_object.set_status(new_status)
            else:
                print "Warning: Object with header '%s' from file not found in current settings dictionary." % tab_header

        except ValueError:
            print "Warning: Could not parse malformed line, skipping: %s" % line
            continue
    
    print "Finished loading settings from file."
