class Config:
    def __init__(self, **kwargs):
        self.data = kwargs
        
    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        else:  # Attribute does not exist in the dictionary
            raise AttributeError("'Config' object has no attribute '{}'".format(name))