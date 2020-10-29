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

    # Gets an object from the grid.
    def get_object(self, id):
        return self._objects[id]

    # Gets all objects that exist in the grid.
    def get_objects(self):
        return self._objects.values()

    # Moves an object a distance and responds if there is a collision.
    def move_object(self, id, dist, check_collision=True):
        if not dist: return
        obj = self._objects[id]
        if check_collision:
            dir = constant.FORWARD if dist>=0 else constant.REVERSE
            c_dist, c_obj = self._get_closest_object(obj, dir)
            if __debug__: print(f"{c_dist} {obj.angle}, {obj.position}")
            if abs(dist) > c_dist:
                if dist < 0: c_dist = -c_dist
                action = obj.on_collide(c_obj)
                if action is constant.REVERSE: obj.move(c_dist)
            else: obj.move(dist)
        else:
            obj.move(dist)

    # Rotates an object and responds if there is a collision.
    def rotate_object(self, id, rads, check_collision=True):
        obj = self._objects[id]
        obj.rotate(rads)
        if check_collision:
            flag, c_obj = self._check_collision(obj)
            if flag:
                action = obj.on_collide(c_obj)
                if action is constant.REVERSE:
                    obj.rotate(-rads)
    
    # Gets the current map
    def get_map(self):
        return self._map

    ### Private Functions ###
    # gets the grid coordinates of the object.
    def _get_coords(self, obj):
        x,y = obj.position
        return int(x / constant.GRID_SIZE), int(y / constant.GRID_SIZE)

    # gets objects listed in the grid at x,y.
    def _get_tile_objects(self, x, y):
        return [self._objects[id] for id in self._map[x][y]]

    # gets objects that are within obj radius.
    def _get_circle_collisions(self, obj):
        collisions = []
        for controllers in self._controllers:
            obj1 = self._objects[controllers.object_id]
            if collision.circle(obj, obj1): collisions.append(obj1)
        return collisions

    # returns the distance of the closest object that this obj is facing
    def _get_closest_object(self, obj, dir):
        x,y = self._get_coords(obj)
        tiles = self._get_tile_objects(x,y)
        objs = self._get_circle_collisions(obj)
        min_dist, collider = math.inf, None
        for obj1 in tiles + objs:
            dist = collision.get_distance(obj, obj1, moving=dir)
            if dist < min_dist:
                min_dist, collider = dist, obj1
        return min_dist, collider
        
    # returns whether a collision occurred with this object
    def _check_collision(self, obj):
        x,y = self._get_coords(obj)
        tiles = self._get_tile_objects(x,y)
        objs = self._get_circle_collisions(obj)
        min_dist, collider = math.inf, None
        for obj1 in tiles + objs:
            if collision.SAT(obj, obj1): return True, obj1
        return False, None

    ### property ###
    map = property(get_map)
    objects = property(get_objects)