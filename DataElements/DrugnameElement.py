"""DrugnameElementclass

The following class extends the DataElement class, and includes any additional fields that need to be collected for the Drugname DataElement

"""

from DataElement import DataElement


class DrugnameElement(DataElement):
    def __init__(self, *args, **kwargs):
        """Calls the super"""
        super(DrugnameElement, self).__init__(*args, **kwargs)
