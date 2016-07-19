"""DataElement class

The general DataElement class described in the architecture. Each field you would like to extract should have its own extension of this class. 

Todo: 
  +Change all of the fields and add @property decorators to make it more pythonic.

"""
class DataElement(object):
    
    def __init__(self,extractedField=None, charOffset=None, extractorName=None, entityName=None):
        """Initializes the DataElement with information received from an Extractor that will be passed to the Assembler.
        
        Args:
            extractedField (str): the actual text extracted from the text
            charOffset (int): the offset of the extractedField in the raw text file
            extractorName (str): the name of the extractor that retrieved the data

        Returns:
            Initialized DataElement (obj)
        """
        self.extractedField = extractedField
        self.charOffset = charOffset
        self.extractorName = extractorName
        self.entityName = entityName

    def getExtractedField(self):
        """Gets the extracted field
        
        Args:
            None
            
        Returns:
            the extracted field (str)
        """
        return self.extractedField

    def setExtractedField(self,extractedField):
        """Sets the  extracted field
        
        Args:
            extractedField (str): the extracted field for this DataElement
            
        Returns:
            None
        """
        self.extractedField = extractedField

    def getCharOffset(self):
        """Gets the character offset.

        Args:
            None

        Returns:
           the character offset (int)
        """
        return self.charOffset

    def setCharOffset(self,charOffset):
        """Sets the character offset
        
        Args:
            charOffset (int): the character offset for this DataElement
            
        Returns:
            None
        """ 
        self.charOffset = charOffset

    def getExtractorName(self):
        """Gets the name of the Extractor.

        Args:
            None

        Returns:
           the Extractor that found this DataElement (str)
        """
        return self.extractorName

    def setExtractorName(self,extractorName):
        """Sets the Extractor name
        
        Args:
            extractorName (str): the name of the Extractor
            
        Returns:
            None
        """ 
        self.extractorName = extractorName

    def getEntityName(self):
        return self.entityName

    def setEntityName(self, entityName):
        self.entityName = entityName
