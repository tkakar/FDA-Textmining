"""AgeElement class

The following class extends the DataElement class, and includes any additional fields that need to be collected for the Age DataElement

"""

from DataElement import DataElement


class AgeElement(DataElement):
    def __init__(self, *args, **kwargs):
        """Calls the super"""
        super(AgeElement, self).__init__(*args, **kwargs)
