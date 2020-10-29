# Python Library
import math
import abc
# Project Library
from lib import VMath

class GameObject(abc.ABC):
    def __init__(self, x, y, hitbox, stationary=False):
        self._x = x
        self._y = y
        self._hitbox = hitbox
        self._area = self._get_area()
        self._radius = self._get_radius()
        self._stationary = stationary
        self._angle = 0

    def on_collide(self, o):
        pass

    def rotate(self, angle):
        self._hitbox = VMath.rotate(self._hitbox, angle)
        self._angle = (math.tau + self._angle + angle) % math.tau

    def move(self, distance):
        self.position = VMath.translate(self.position, distance, self._angle)

    def get_hitbox(self, to_int=False, get_raw=False):
        if get_raw: return self._hitbox
        if to_int:
            hitbox = [(int(round(x+self._x)),int(round(y+self._y))) for x,y in self._hitbox]
        else:
            hitbox = [(x+self._x,y+self._y) for x,y in self._hitbox]
        return hitbox
    
    def set_hitbox(self, hitbox):
        self._hitbox = hitbox

    def get_position(self):
        return self._x,self._y
    
    def set_position(self, position):
        self._x, self._y = position
    
    def get_radius(self):
        return self._hitbox
    
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

    def _get_radius(self):
        r = 0
        for point in self._hitbox:
            dist = VMath.distance((0,0), point)
            if dist > r: r = dist
        self._radius = r

    def _get_area(self):
        h = (self._hitbox[0][1] - self._hitbox[1][1])
        w = (self._hitbox[1][0] - self._hitbox[2][0])
        return abs(w*h)


    # property
    hitbox = property(get_hitbox, set_hitbox)
    position = property(get_position, set_position)
    radius = property(get_radius, set_radius)
    angle = property(get_angle, set_angle)
    area = property(get_area, set_area)