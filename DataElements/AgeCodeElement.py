"""AgeElement class

The following class extends the DataElement class, and includes any additional fields that need to be collected for the Age DataElement

"""

from DataElement import DataElement


class AgeCodeElement(DataElement):
    def __init__(self, *args, **kwargs):
        """Calls the super"""
        super(AgeCodeElement, self).__init__(*args, **kwargs)
