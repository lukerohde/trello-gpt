class Config:
    def __init__(self, **kwargs):  # Allows keyword arguments to be passed in as attributes during instantiation 
        self.attributes = kwargs   # Stores them as attributes in self.attributes

    def __getattr__(self, name):   # Getter method for the attributes stored in self.attributes 
        try:                       # Try clause handles KeyError if item not found in self.attributes dict 
            return self.attributes[name]  
        except KeyError as e:       # If the key is not found, raise AttributeError instead of KeyError  
            raise AttributeError("'{}' not found in config.".format(name))

    def __setattr__(self, name, value):      # Setter method for adding new attributes to config object     
        if 'attributes' not in self.__dict__:     # Check if 'attribute'
            super().__setattr__(name, value)  # If not in __dict__, call superclass setattr to create new attribute
        else:
            self.attributes[name] = value # If in __dict__, add new attribute to 'attributes' dict