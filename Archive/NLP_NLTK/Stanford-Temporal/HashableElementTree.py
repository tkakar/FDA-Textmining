from  xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import fromstring


class HashableElementTree(ElementTree):
    pass

    # def __init__(self, element=None, file=None):
    #    self.et = ElementTree()
    #    self.et.element = element
    #    self.et.file = file

    def __eq__(self, other):
        return self._root.text == other._root.text

    def __hash__(self):
        return hash(str(self._root.text))

    #    def fromstring(self,text):
    #       return super(ElementTree, self).fromstring(text)
