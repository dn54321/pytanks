# Python Library
import math
import abc
# Project Library
from lib import VMath

class GameObject:
    def __init__(self, x, y, hitbox, stationary=False, solid=True):
        self._position = x, y
        self._hitbox = hitbox
        self._area = self._get_area()
        self._radius = self._get_radius()
        self._stationary = stationary
        self._solid = solid
        self._angle = 0

        if not stationary:
            self._old_position = x,y

    def on_collide(self, o):
        pass

    def rotate(self, angle):
        self._hitbox = VMath.rotate(self._hitbox, angle)
        self._angle = (self._angle + angle) % math.tau

    def move(self, distance):
        self._old_position = self._position
        self.position = VMath.translate(self.position, distance, self._angle)

    def get_hitbox(self, to_int=False, get_raw=False):
        if get_raw: return self._hitbox
        x0,y0 = self._position
        if to_int:
            hitbox = [(int(round(x+x0)),int(round(y+y0))) for x,y in self._hitbox]
        else:
            hitbox = [(x+x0,y+y0) for x,y in self._hitbox]
        return hitbox
    
    def set_hitbox(self, hitbox):
        self._hitbox = hitbox

    def get_old_position(self):
        return self._old_position

    def get_position(self):
        return self._position
    
    def set_position(self, position):
        self._position = position
    
    def get_radius(self):
        return self._radius
    
    def set_radius(self, radius):
        self._radius = radius

    def get_angle(self):
        return self._angle

    def set_angle(self, angle):
        self._angle = angle

    def is_stationary(self):
        return self.stationary
        
    def get_area(self):
        return self._area

    def set_area(self, area):
        self._area = area

    def is_solid(self):
        return self._solid
    def is_stationary(self):
        return self._stationary

    def delete(self):
        return True
        
    def _get_radius(self):
        r = 0
        for point in self._hitbox:
            dist = VMath.distance((0,0), point)
            if dist > r: r = dist
        return r

    def _get_area(self):
        h = (self._hitbox[0][1] - self._hitbox[1][1])
        w = (self._hitbox[1][0] - self._hitbox[2][0])
        return abs(w*h)

    # property
    hitbox = property(get_hitbox, set_hitbox)
    position = property(get_position, set_position)
    old_position = property(get_old_position)
    radius = property(get_radius, set_radius)
    angle = property(get_angle, set_angle)
    area = property(get_area, set_area)
    solid = property(is_solid)
    stationary = property(is_stationary)