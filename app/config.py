class Config:
    def __init__(self, **kwargs):  # Allows keyword arguments to be passed in as attributes during instantiation 
        self.attributes = kwargs   # Stores them as attributes in self.attributes

    def __getattr__(self, name):   # Getter method for the attributes stored in self.attributes 
        try:                       # Try clause handles KeyError if item not found in self.attributes dict 
            return self.attributes[name]  
        except KeyError as e:       # If the key is not found, raise AttributeError instead of KeyError  
            raise AttributeError("'{}' not found in config.".format(name))