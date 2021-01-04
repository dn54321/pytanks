# python libraries
import json, math, pygame, random

# project libraries
from src import map, gameTile, playerController, sentryController, gameObject, constant, gameRender
from lib import utils
from src.gameObjects import *
class MapLoader:
    _legend = {
        'w': wall.Wall,
        'p': tank.Tank,
        's': tank.Tank,
        'a': None,
        tank.Tank: playerController.PlayerController
    }

    _tanks = {
        'p': playerController.PlayerController,
        's': sentryController.SentryController
    }


    def __init__(self):
        self._data = None
        self._map = None
        self._renderer = None

    def load(self, url):
        with open('maps/' + url) as json_file:
            self._data = json.load(json_file)
        self._data['orientation'] = [(math.tau+math.radians(90-x))%math.tau for x in self._data['orientation']]
        name = self._data['name']
        width = self._data['width']
        height = self._data['height']
        self._map = map.Map(name, width, height)
        sz = (width*constant.GRID_SIZE, height*constant.GRID_SIZE)
        self._renderer = gameRender.GameRender(pygame.Surface(sz), width, height)
        
    def build(self, player_amount):
        counter, y = 0, 0
        stage = self._data['map']
        orientation = self._data['orientation']
        visited = [0]*self.height*self.width
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
                        if counter < player_amount:
                            self._build_controller(stage[y][x], x, y, orientation[counter])
                            counter += 1
                        x += 1
                x += visited[y*self.width+x]
            y += 1
        
    def get_renderer(self):
        return self._renderer

    def render_surface(self, seed=int(random.random()*999999999)):
        random.seed(seed)
        dims = w,h = self.width, self.height
        arr = utils.matrix_transpose(self._data['map'], (h,w))
        self._renderer.render_background()
        self._renderer.render_flowers(utils.msk_2d(arr, 'a', dims))
        self._renderer.render_walls(utils.msk_2d(arr, 'w', dims))
        return self._renderer.surface

    def _render_flowers(self, surface, tileset):
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

    def _render_walls(self, surface, tileset):
        visited = utils.array_2d(self.width, self.height, False)
        stage = self._data['map']
        for i in range(self.width):
            for j in range(self.height):
                if stage[j][i] == 'w' and not visited[i][j]: 
                    self._render_wall(i, j,surface, tileset , visited, stage)

    def _render_wall(self, x, y, surface, tileset, visited, stage):
        if not (0<=x<self.width and 0<=y<self.height) or visited[x][y]: return
        if stage[y][x] != 'w': 
            return self._render_shadows(x, y, surface, tileset, visited)

        gz = constant.GRID_SIZE
        key, y_offset = 0, 0
        if self._check(x-1, y, '!w'): key |= constant.LEFT
        elif self._check(x-1,y+1,'!w') and self._check(x,y+1,'w'): key |= constant.LEFT
        if self._check(x,y-1, '!w'): key |= constant.UP
        if self._check(x+1,y,'!w'): key |= constant.RIGHT
        elif self._check(x+1,y+1,'!w') and self._check(x,y+1,'w'): key |= constant.RIGHT
        if self._check(x,y+1,'!w'): y_offset = 4
        elif self._check(x,y+2,'!w'): key |= constant.DOWN
        if key or y_offset:
            i,j = MapLoader._direction[key]
            i,j = i+7,j+1+y_offset
            surface.blit(tileset[i][j], (x*gz,y*gz))
        if y_offset: visited[x][y] = -1
        else: visited[x][y] = 1
        self._render_wall(x+1, y, surface, tileset, visited, stage)
        self._render_wall(x, y+1, surface, tileset, visited, stage)

    def _render_shadows(self, x, y, surface, tileset, visited):
        gz = constant.GRID_SIZE
        if visited[x][y]: return
        
        if self._check(x-1, y, 'w'):
            if self._check(x,y-1, 'w'): 
                surface.blit(tileset[5][3], (x*gz,y*gz))
            elif self._check(x-1,y+1,'a'): 
                surface.blit(tileset[3][4], (x*gz,y*gz)) 
                surface.blit(tileset[5][1], (x*gz,(y+1)*gz))
            elif self._check(x-1,y-2,'a') and self._check(x-1,y-1,'w'):
                surface.blit(tileset[3][3], (x*gz,y*gz))
            elif self._check(x-1,y-1,'!a'):
                rval = random.randint(0,2)
                surface.blit(tileset[3][3+rval], (x*gz,y*gz)) 
        elif self._check(x,y-1, 'w'):
            if self._check(x-1,y-1,'a'): surface.blit(tileset[4][3], (x*gz,y*gz))
            else:
                rval = random.randint(0,2)
                surface.blit(tileset[3+rval][2], (x*gz, y*gz))
        visited[x][y] = 1
    
    def _render_entities(self, tanks, bullets, gameGrid, surface, tileset):
        gz = constant.GRID_SIZE
        self._render_tanks(tanks, gameGrid, surface, tileset)
       # self._render_bullets(bullet, gameGrid, surface, tileset)

    def _render_bullets(self, tanks, gameGrid, surface, tileset):
        gz = constant.GRID_SIZE
        
    def _render_tanks(self, players, gameGrid, surface, tileset):
        for player in players:
            colour, tank_id = player.tank_colour, player.tank_id

    def _check(self, x, y, symbol):
        if 0 <= x < self.width and 0 <= y < self.height:
            if symbol[0] == '!': return self._data['map'][y][x] != symbol[1]
            else: return self._data['map'][y][x] == symbol
        return False

    def _build_controller(self, obj_type, x, y, angle):
        control_type = MapLoader._tanks[obj_type]
        entity_type = MapLoader._legend[obj_type]
        obj = entity_type(x, y, angle)
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