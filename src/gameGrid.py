# Python Lib
import json
import math
# Project Library
from src import mapLoader, gameTile, constant
from lib import collision, VMath

# Private functions
def _expand_one(bounds, width, height):
    x0,y0 = bounds[0]
    x1,y1 = bounds[1]
    x0 = max(x0-1, 0)
    y0 = max(y0-1, 0)
    x1 = min(x1+1, width-1)
    y1 = min(y1+1, height-1)
    return [(x0,y0), (x1,y1)]

class GameGrid:
    def __init__(self):
        self._object_counter = 0
        self._objects = {}
        self._controllers = []
        self._map = None

    # Adds an object to the grid.
    def add_object(self, obj):
        id = self._object_counter
        self._object_counter += 1
        self._object[id] = obj
        return id

    # Removes an object from the grid.
    def remove_object(self, id):
        del object[id]

    def get_object(self, id):
        return self._objects[id]

    def move_object(self, id, dist, check_collision=True):
        obj = self._objects[id]
        position = VMath.translate(obj.position, dist, obj.angle)
        obj.position = position
        if check_collision:
            c_dist, c_obj = self._check_collision(obj)
            if dist > c_dist:
                action = obj.on_collide(c_obj)
                if action is constant.REVERSE:
                    position = VMath.translate(obj.position, c_dist-dist, obj.angle + math.pi)
                    self.position = position

    def rotate_object(self, id, rads, check_collision=True):
        obj = self._objects[id]
        obj.rotate(rads)
        if check_collision and _check_collision(obj):
            has_collided, c_obj = _check_collision(obj, collision_method=collision.SAT)[0]
            if has_collided:
                action = obj.on_collide(c_obj)
                if action is constant.REVERSE:
                    obj.rotate(-rads)

    def _check_collision(self, obj, collision_method=collision.get_distance):
        x,y = obj.get_position()
        i,j = x % constant.GRID_SIZE, j % constant.GRID_SIZE
        min_dist = math.inf
        collision_object = None
        # Tile Collision
        for tile in self._map[i][j]:
            dist = collision_method(obj, tile)
            if dist < min_dist:
                min_dist = dist
                collision_object = tile
        
        # Object Collision
        for controllers in self._controllers:
            o2 = self._objects[controllers.object_id]
            if collision.circle(obj, o2):
                dist = collision_method(obj, o2)
            if dist < min_dist:
                min_dist = dist
                collision_object = o2
        
        if dist is math.inf: return False
        return [dist, collision_object]


    # Loads a map into the gameGrid
    def load_map(self, url):
        stage = mapLoader.MapLoader()
        stage.load(url)
        
        # Create empty grid map
        self._map = []
        for y in range(stage.height):
            cell = []
            for x in range(stage.width):
                cell.append([])
            self._map.append([])

        # Fill in map
        for obj in stage.objects:
            id = self.add_object(obj)
            (x0,y0),(x1,y1) = _expand_one(obj.tile_boundary, stage.width, stage.height)
            for x in range(x0+1,x1+1):
                for y in range(y0+1,y1+1):
                    self._map[x][y].append(id)