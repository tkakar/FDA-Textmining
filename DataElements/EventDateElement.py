import sys
sys.path.append('../')
from DataElement import  DataElement

class EventDateElement(DataElement):

    def __init__(self, *args, **kwargs):
        super(EventDateElement, self).__init__(**kwargs)
