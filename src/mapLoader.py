# python libraries
import json
import math

# project libraries
from src import map, gameTile, playerController, gameObject
from src.gameObjects import *
class MapLoader:
    def __init__(self):
        self._data = None
        self._map = None
        self._legend = {
            'w': wall.Wall,
            'p': tank.Tank,
            'a': None,
            tank.Tank: playerController.PlayerController
        }

    def load(self, url):
        with open('maps/' + url) as json_file:
            self._data = json.load(json_file)
        self._data['orientation'] = [math.radians(90-x) for x in self._data['orientation']]
        name = self._data['name']
        width = self._data['width']
        height = self._data['height']
        self._map = map.Map(name, width, height)
        
    def build(self):
        stage = self._data['map']
        orientation = self._data['orientation']
        counter = 0
        visited = [0]*self.height*self.width
        y=0
        while y < self.height:
            x=0
            while x < self.width:
                object_type = self._legend[stage[y][x]]
                if not visited[y*self.width+x]:
                    if object_type is None:
                        x += 1
                    elif issubclass(object_type, gameTile.GameTile):
                        self._build_tile(visited, stage, x, y)
                    elif issubclass(object_type, gameObject.GameObject):
                        self._build_controller(object_type, x, y, orientation[counter])
                        counter += 1
                        x += 1
                x += visited[y*self.width+x]
            y += 1
        
    def generate_image(self):
        pass

    def _build_controller(self, obj_type, x, y, angle):
        control_type = self._legend[obj_type]
        obj = obj_type(x, y, angle)
        self._map.objects.append(obj)
        self._map.controllers.append(control_type)

    def _build_tile(self, visited, stage, x0 , y0):
        w = 1
        h = 1
        object_type = stage[y0][x0]

        # Find width
        while x0 + w < self.width and stage[y0][x0+w] is object_type:
            w += 1

        # Find height
        has_row = True
        while y0 + h < self.height and has_row:
            x1 = x0
            while x1-x0 < w and has_row is True:
                if stage[y0+h][x1] is object_type: x1 += 1
                else: has_row = False
            if has_row: h += 1
        
        # Updated Visited
        for y in range(h):
            visited[(y0+y)*self.width + x0] = w

        # Add Object
        obj = self._legend[object_type](x0,y0, x0+w-1, y0+h-1)
        self.objects.append(obj)

    # Proxy Functions
    def __getattr__(self, name):
        return getattr(self._map, name)

    def __setattr__(self, name, value):
        if  name[0] == '_':
            self.__dict__[name] = value
        else:
            self._map.__setattr__(name, value)