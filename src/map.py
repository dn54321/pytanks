class Map:
    def __init__(self, name, width, height):
        self._objects = []
        self._width = None
        self._height = None
        self._name = None
    
    def get_width(self):
        return self._width
    
    def set_width(self, width):
        self._width = width

    def get_height(self):
        return self._width

    def set_height(self, height):
        self._height = height

    def get_name(self):
        return self._name

    def get_objects(self):
        return self._objects

    # getter/setter functions
    width = property(get_width, set_width)
    height = property(get_height, set_height)
    name = property(get_name) 
    objects = property(get_objects)