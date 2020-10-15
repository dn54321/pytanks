import json

class GameGrid:
    def __init__(self):
        self._object_counter = 0
        self._object = {}
        self._map = None

    # Adds an object to the grid.
    def add_object(self, obj, id):
        self._object[id] = obj
        self._object_counter += 1

    # Removes an object from the grid.
    def remove_object(self, id):
        del object[id]
    
    # Loads a map into the gameGrid
    def load_map(self, url):
        FILE = open(maps + 'url')
        data = json