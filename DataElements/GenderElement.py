"""GenderElement class

The following class extends the DataElement class, and includes any additional fields that need to be collected for the Gender DataElement

"""

from DataElement import DataElement


class GenderElement(DataElement):
    def __init__(self, *args, **kwargs):
        """Calls the super"""
        super(GenderElement, self).__init__(*args, **kwargs)
