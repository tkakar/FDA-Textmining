"""DosageElement class

The following class extends the DataElement class, and includes any additional fields that need to be collected for the Dosage DataElement

"""

from DataElement import DataElement


class DosageElement(DataElement):
    def __init__(self, *args, **kwargs):
        """Calls the super"""
        super(DosageElement, self).__init__(*args, **kwargs)
