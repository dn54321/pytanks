# python libraries
import json, math, pygame, random

# project libraries
from src import map, gameTile, playerController, gameObject, constant
from lib import utils
from src.gameObjects import *
class MapLoader:
    _legend = {
        'w': wall.Wall,
        'p': tank.Tank,
        'a': None,
        tank.Tank: playerController.PlayerController
    }
    _direction = {
        0: (0,0),
        constant.UP: (0,-1),
        constant.DOWN: (0,1),
        constant.LEFT: (-1,0),
        constant.RIGHT: (1,0),
        constant.LEFT|constant.UP: (-1,-1),
        constant.RIGHT|constant.UP: (1,-1),
        constant.LEFT|constant.DOWN: (-1,1),
        constant.RIGHT|constant.DOWN: (1,1)
    }

    def __init__(self):
        self._data = None
        self._map = None

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
                object_type = MapLoader._legend[stage[y][x]]
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
        
    def generate_surface(self, seed=int(random.random()*999999999)):
        random.seed(seed)
        gz = constant.GRID_SIZE
        stage = self._data['map']
        surface = pygame.Surface((self.width*gz, self.height*gz))
        tileset = self.get_tileset()
        self._generate_background(surface, tileset)
        self._generate_walls(surface, tileset)
        return surface

    def get_tileset(self):
        image = pygame.image.load(constant.TILESET).convert_alpha()
        image_width, image_height = image.get_size()
        cols, rows = int(image_width/16), int(image_height/16)
        tileset = utils.array_2d(rows, cols)
        for x in range(cols):
            for y in range(rows):
                rect = pygame.Rect = (x*16, y*16, 16, 16)
                tileset[x][y] = pygame.transform.scale2x(image.subsurface(rect))
        return tileset

    def _generate_background(self, surface, tileset):
        gz = constant.GRID_SIZE
        for i in range(self.width):
            for j in range(self.height):
                rval = random.randint(0,5)
                surface.blit(tileset[rval][0], (i*gz, j*gz))
        self._generate_flowers(surface, tileset)

    def _generate_flowers(self, surface, tileset):
        stage = self._data['map']
        gz = constant.GRID_SIZE
        flower = utils.array_2d(self.width, self.height, False)
        for i in range(self.width):
            for j in range(self.height):
                grass_count = 0
                flower_count = 0
                for k in [-1,0,1]:
                    for l in [-1,0,1]:
                        x = i+k
                        y = j+l
                        if 0<=x<self.width and 0<=y<self.height:
                            if stage[y][x] == 'a': grass_count += 1
                            if flower[x][y]: flower_count += 1
                threshhold = 1+grass_count*0.5 + flower_count*5
                if random.randint(0,100) <= threshhold:
                    flower[i][j] = True
                    rval = random.randint(0,4)
                    surface.blit(tileset[rval][1], (i*gz, j*gz))
        
    def _generate_walls(self, surface, tileset):
        stage = self._data['map']
        gz = constant.GRID_SIZE

        for i in range(self.width):
            for j in range(self.height):
                if stage[j][i] == 'w':
                    key = 0
                    is_wall = 0
                    if i-1>=0:
                        if stage[j][i-1] != 'w': key = key | constant.LEFT
                        elif j+1<self.height and stage[j+1][i] == 'w' and stage[j+1][i-1] != 'w': 
                            key = key | constant.LEFT
                    if i+1<self.width:
                        if stage[j][i+1] != 'w': key = key | constant.RIGHT
                        elif j+1<self.height and stage[j+1][i] == 'w' and stage[j+1][i+1] != 'w':
                            key = key | constant.RIGHT
                    if j-1>=0 and stage[j-1][i] != 'w': key = key | constant.UP
                    if j+1<self.height and stage[j+1][i] != 'w': is_wall = 4
                    elif j+2<self.height and stage[j+2][i] != 'w': key = key | constant.DOWN
                    if key+is_wall: 
                        x_offset, y_offset = MapLoader._direction[key]
                        x_offset, y_offset = x_offset+7, y_offset+is_wall+1
                        surface.blit(tileset[x_offset][y_offset], (i*gz, j*gz))
                        if key & constant.RIGHT & constant.DOWN and j+1<self.height and i+1 <self.width:
                            surface.blit(tileset[5][1], ((i+1)*gz, (j+1)*gz))
                        elif key & constant.RIGHT and i+1<self.width:
                            rval = random.randint(0,1)
                            surface.blit(tileset[3][3+rval], ((i+1)*gz, j*gz))
                        elif is_wall and j+1<self.height:
                            rval = random.randint(0,2)
                            surface.blit(tileset[3+rval][2], (i*gz, (j+1)*gz))

    def _build_controller(self, obj_type, x, y, angle):
        control_type = MapLoader._legend[obj_type]
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
        obj = MapLoader._legend[object_type](x0,y0, x0+w-1, y0+h-1)
        self.objects.append(obj)

    # Proxy Functions
    def __getattr__(self, name):
        return getattr(self._map, name)

    def __setattr__(self, name, value):
        if  name[0] == '_':
            self.__dict__[name] = value
        else:
            self._map.__setattr__(name, value)