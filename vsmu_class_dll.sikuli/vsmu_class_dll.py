import sys


class VsmuTab:
    def __init__(self, tab_header, category, submenu, subcategory="none",
                 status=False, linked_parent=None):
        self.tab_header = tab_header
        self.category = category
        self.submenu = submenu
        self.subcategory = subcategory
        self.status = status
        self.linked_parent = linked_parent

    @property
    def hierarchy(self):
        return "child" if self.linked_parent else "parent"

    @property
    def enabled(self):
        if not self.linked_parent:
            return True  
        else:
            return self.linked_parent.status and self.linked_parent.enabled

    @property
    def linked_status(self):
        if self.linked_parent:
            return self.linked_parent.status
        return False

    def get_submenu(self):
        return self.submenu

    def get_status(self):
        return self.status

    def set_status(self, new_status):
        if self.enabled:
            self.status = bool(new_status)
        else:
            warning_msg = "WARNING: Status for '{}' cannot be changed because its parent '{}' is disabled.".format(
                self.tab_header, self.linked_parent.tab_header
            )
            print(warning_msg)
            return warning_msg

    def get_linked(self):
        return self.linked_parent

    def get_linked_status(self):
        return self.linked_status

    def __str__(self):
        return "tab_header={}, category={}, submenu={}, status={}, hierarchy={}, linked={}, linked_status={}, enabled={}".format(
            self.tab_header,
            self.category,
            self.submenu,
            self.status,
            self.hierarchy,
            self.linked_parent.tab_header if self.linked_parent else "None",
            self.linked_status,
            self.enabled
        )