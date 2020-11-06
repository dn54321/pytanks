# Python Lib
import json
import math
# Project Library
from src import gameTile, constant
from lib import collision, VMath, utils

class GameGrid:
    def __init__(self, width, height):
        self._object_counter = 0
        self._width = width
        self._height = height
        self._objects = {}
        self._ids = {}
        self._controllers = {}
        self._map = utils.array_2d(height, width)

    # Adds an object to the grid.
    def add_object(self, obj, check_collision=True):
        if check_collision and not (self._within_grid(obj) 
            and self._check_collision(obj)):
                return -1
        id = self._object_counter
        self._object_counter += 1
        self._objects[id] = obj
        self._ids[obj] = id
        return id

    # Removes an object from the grid.
    def remove_object(self, id):
        obj = self._objects[id]
        obj.delete()
        if not isinstance(obj, gameTile.GameTile):
            self._controllers[id].delete()
            del self._controllers[id]
        del self._ids[self._objects[id]]
        del self._objects[id]
    

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
            c_dist, c_obj, c_line = self._get_closest_object(obj, dist)
            if __debug__: print(f"{c_dist} {obj.angle}, {obj.position}")
            if abs(dist) > c_dist:
                if dist < 0: c_dist = -c_dist
                self._handle_collision(obj, c_obj, moved=c_dist, line=c_line)
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
                self._handle_collision(obj, c_obj, move_type=constant.ROTATIONAL, 
                                       moved=-rads)
    
    # adds a controller to the grid
    def add_controller(self, controller):
        self._controllers[controller.object_id] = controller
    
    # Gets a list of controllers
    def get_controllers(self):
        return list(self._controllers.values())

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
    def _get_circle_collisions(self, obj, vel=0):
        collisions = []
        for controllers in self.controllers:
            obj1 = self._objects[controllers.object_id]
            if obj is not obj1 and collision.circle(obj, obj1, vel): collisions.append(obj1)
        return collisions

    # returns the distance of the closest object that this obj is facing
    def _get_closest_object(self, obj, dist):
        if dist >= 0: dir = constant.FORWARD
        else: dir = constant.REVERSE
        x,y = self._get_coords(obj)
        tiles = self._get_tile_objects(x,y)
        objs = self._get_circle_collisions(obj, dist)
        min_dist, collider, min_line = math.inf, None, None
        for obj1 in tiles + objs:
            dist, c_line = collision.get_distance(obj, obj1, moving=dir)
            if dist < min_dist:
                min_dist, collider, min_line = dist, obj1, c_line
        return min_dist, collider, min_line
        
    # returns whether a collision occurred with this object
    def _check_collision(self, obj):
        x,y = self._get_coords(obj)
        tiles = self._get_tile_objects(x,y)
        objs = self._get_circle_collisions(obj)
        min_dist, collider = math.inf, None
        for obj1 in tiles + objs:
            if collision.SAT(obj, obj1): return True, obj1
        return False, None

    def _handle_collision(self, obj, obj2, move_type=constant.TRANSLATIONAL, moved=None, line=None):
        self._handle_action(obj, obj2, move_type, moved, line)
        self._handle_action(obj2, obj, move_type, 0, line)

    def _handle_action(self, obj, obj2, move_type, moved, line):
        action = obj.on_collide(obj2)
        if move_type is constant.TRANSLATIONAL: move = obj.move
        else: move = obj.rotate
        
        if action is constant.BOUNCE: self._bounce_object(obj, moved, line)
        elif action is constant.DESTRUCT: self.remove_object(self._ids[obj])
        elif action is constant.REVERSE: move(moved)


    # Checks whether an object can be placed within the grid
    def _within_grid(self, obj):
        width = self._width*constant.GRID_SIZE
        height = self._height*constant.GRID_SIZE
        for x,y in obj.hitbox:
            if not (0 <= x <= width and 0 <= y <= height):
                return False
        return True

    # Bounces an object off an existing object
    def _bounce_object(self, obj, dist, line):
        id = self._ids[obj]
        if dist:
            obj.move(dist)
        x,y = VMath.subtract(line[0],line[1])
        l_angle = (math.atan2(y,x) + math.tau) % math.tau
        obj.rotate(2*(l_angle-obj.angle))
        
    ### property ###
    map = property(get_map)
    objects = property(get_objects)
    controllers = property(get_controllers)