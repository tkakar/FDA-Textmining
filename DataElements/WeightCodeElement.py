"""WeightCodeElement class

The following class extends the DataElement class, and includes any additional fields that need to be collected for the WeightCode DataElement

"""

from DataElement import DataElement


class WeightCodeElement(DataElement):
    def __init__(self, *args, **kwargs):
        """Calls the super"""
        super(WeightCodeElement, self).__init__(*args, **kwargs)
