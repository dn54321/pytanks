# Python Lib
import json
import math
# Project Library
from src import gameTile, constant
from lib import collision, VMath


class GameGrid:
    def __init__(self):
        self._object_counter = 0
        self._objects = {}
        self._controllers = []
        self._map = []

    # Adds an object to the grid.
    def add_object(self, obj):
        id = self._object_counter
        self._object_counter += 1
        self._objects[id] = obj
        return id

    # Removes an object from the grid.
    def remove_object(self, id):
        del object[id]

    def get_object(self, id):
        return self._objects[id]

    def get_objects(self):
        return self._objects.values()

    def move_object(self, id, dist, check_collision=True):
        obj = self._objects[id]
        if check_collision:
            dir = constant.FORWARD if dist>=0 else constant.REVERSE
            c_dist, c_obj = self._check_collision(obj, moving=dir)
            # print(f"{c_dist} {obj.angle}, {obj.position}")
            if abs(dist) > c_dist:
                if dist<0: c_dist = -c_dist
                action = obj.on_collide(c_obj)
                if action is constant.REVERSE: obj.move(c_dist)
            else: obj.move(dist)
        else:
            obj.move(dist)

    def rotate_object(self, id, rads, check_collision=True):
        obj = self._objects[id]
        obj.rotate(rads)
        if check_collision:
            has_collided, c_obj = self._check_collision(obj, collision_method=collision.SAT)
            if has_collided:
                action = obj.on_collide(c_obj)
                if action is constant.REVERSE:
                    obj.rotate(-rads)
    
    def _check_collision(self, obj, collision_method=collision.get_distance, moving=constant.FORWARD):
        x,y = obj.get_position()
        i,j = int(x / constant.GRID_SIZE), int(y / constant.GRID_SIZE)
        min_dist = math.inf
        collision_object = None
        # Tile Collision
        for tile_id in self._map[i][j]:
            tile = self._objects[tile_id]
            dist = collision_method(obj, tile, moving)
            if dist < min_dist:
                min_dist = dist
                collision_object = tile
        
        # Object Collision
        for controllers in self._controllers:
            o2 = self._objects[controllers.object_id]
            if collision.circle(obj, o2):
                dist = collision_method(obj, o2, moving)
            if dist < min_dist:
                min_dist = dist
                collision_object = o2

        if min_dist is math.inf: return [math.inf, None]
        return [min_dist, collision_object]

    def get_map(self):
        return self._map

    # property
    map = property(get_map)
    objects = property(get_objects)