class Map:
    def __init__(self, name, width, height):
        self._objects = []
        self._controllers = []
        self._name = name
        self._width = width
        self._height = height

    def get_width(self):
        return self._width
    
    def set_width(self, width):
        self._width = width

    def get_height(self):
        return self._height

    def set_height(self, height):
        self._height = height

    def get_name(self):
        return self._name

    def get_objects(self):
        return self._objects

    def get_controllers(self):
        return self._controllers

    # getter/setter functions
    width = property(get_width, set_width)
    height = property(get_height, set_height)
    name = property(get_name) 
    objects = property(get_objects)
    controllers = property(get_controllers)