# python libraries
import json

# project libraries
from lib import map, gameTile
from lib.gameObjects import *

class MapLoader:
    def __init__(self):
        self._data = None
        self._map = None

    def load(url):
        with open('maps/' + url) as json_file:
            self._data = json.load(json_file)
        name, width, height = data['name'], data['width'], data['height']
        self._map(name, width, height)

    def build_map(self):
        stage = self._data['map']
        orientation = self._data['orientation']
        visited = [0]*self.height*self.width
        legend = {
            'w': wall.Wall(),
            't': tank.Tank(),
            'a': None
        }
        y=0
        while y < self.height:
            x=0
            while x < self.width:
                if not visited[y*self.height+x] and issubclass(stage[y][x], gameTile.GameTile):
                    self._build_object(visited, stage, x, y)
                x += visited[y][x] + 1
            y += 1
        
    def generate_image(self):
        pass

    def _build_object(self, visited, stage, x0 , y0):
        width = 1
        height = 1
        x1,y1 = x0+1,y0
        object_type = stage[y0][x0]

        # Find width
        while stage[y1][x1] is object_type:
            width += 1
            x1 += 1

        # Find height
        y1 += 1
        has_row = True
        while y1 < self.height and has_row:
            x1 = x0
            while x1-x0 < width and has_row is True:
                if stage[y1][x1] is object_type: x1 += 1
                else: has_row is False
                if has_row: height += 1
        
        # Updated Visited
        for y in range(height):
            visited[y0+y][x0] = width - 1

        # Add Object
        obj = object_type(x0,y0, x1+width-1, y1+width-1)
        self.objects.append(obj)

    # Proxy Functions
    def __getattr__(self, name):
        return getattr(self._map, name)

    def __setattr__(self, name, value)
        if hasattr(self, name):
            self.__dict__[name] = value
        else:
            self._map.__setattr__(name, value)