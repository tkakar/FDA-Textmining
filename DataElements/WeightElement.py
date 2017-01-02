"""WeightElement class

The following class extends the DataElement class, and includes any additional fields that need to be collected for the Weight DataElement

"""

from DataElement import DataElement


class WeightElement(DataElement):
    def __init__(self, *args, **kwargs):
        """Calls the super"""
        super(WeightElement, self).__init__(*args, **kwargs)
