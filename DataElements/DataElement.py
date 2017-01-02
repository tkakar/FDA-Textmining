"""DataElement class

The general DataElement class described in the architecture. Each field you would like to extract should have its own extension of this class. 

Todo: 
  +Change all of the fields and add @property decorators to make it more pythonic.

"""


class DataElement(object):
    def __init__(self, extractedField=None, charOffset=None, extractorName=None, entityName=None):
        """Initializes the DataElement with information received from an Extractor that will be passed to the Assembler.
        
        Args:
            extractedField (str): the actual text extracted from the text
            charOffset (int): the offset of the extractedField in the raw text file
            extractorName (str): the name of the extractor that retrieved the data

        Returns:
            Initialized DataElement (obj)
        """
        self._extractedField = extractedField
        self._charOffset = charOffset
        self._extractorName = extractorName
        self._entityName = entityName

    # def __repr__(self):
    #     charOffset = [str(x)+':'+str(y)+';' for x,y in self.charOffset]
    #     return 'Extracted Field: ', self.extractedField, 'charOffset: ', charOffset, 'extractorName: ', self.extractorName, 'entityName: ', self.entityName
    @property
    def extractedField(self):
        """Gets the extracted field
        
        Args:
            None
            
        Returns:
            the extracted field (str)
        """
        return self._extractedField

    @extractedField.setter
    def extractedField(self, extractedField):
        """Sets the  extracted field
        
        Args:
            extractedField (str): the extracted field for this DataElement
            
        Returns:
            None
        """
        self._extractedField = extractedField

    @property
    def charOffset(self):
        """Gets the character offset.

        Args:
            None

        Returns:
           the character offset (int)
        """
        return self._charOffset

    @charOffset.setter
    def charOffset(self, charOffset):
        """Sets the character offset
        
        Args:
            charOffset (int): the character offset for this DataElement
            
        Returns:
            None
        """
        self._charOffset = charOffset

    @property
    def extractorName(self):
        """Gets the name of the Extractor.

        Args:
            None

        Returns:
           the Extractor that found this DataElement (str)
        """
        return self._extractorName

    @extractorName.setter
    def extractorName(self, extractorName):
        """Sets the Extractor name
        
        Args:
            extractorName (str): the name of the Extractor
            
        Returns:
            None
        """
        self._extractorName = extractorName

    @property
    def entityName(self):
        return self._entityName

    @entityName.setter
    def entityName(self, entityName):
        self._entityName = entityName
