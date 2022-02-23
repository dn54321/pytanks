# project libraries
from src import gameObjects, entity, gameTile, constant
from src.gameObjects import bullet

import math

class Tank(entity.Entity):
    def __init__(self, x, y, angle):
        sz = constant.TANK_SIZE/2
        gz = constant.GRID_SIZE
        x,y = x*gz+gz/2, y*gz+gz/2
        hitbox = [(sz,-sz), (sz,sz), (-sz,sz), (-sz,-sz)]
        super().__init__(x, y, angle, hitbox)
        self._distance = 0
        self._velocity = 0
        self._acceleration = 1
        self._terminal_velocity = 5
        self._nozzle_angle = 0
        self._nozzle_length = self._radius*1.5
        self._old_nozzle_angle = angle
        self.force_rotate(angle)
    
    def rotate(self, angle):
        super().rotate(angle)
        self.rotate_nozzle(angle)
    
    def force_rotate(self, angle):
        super().force_rotate(angle)
        self._nozzle_angle = angle
        self._old_nozzle_angle = angle
    
    def rotate_nozzle(self, angle):
        self._nozzle_angle = (self._nozzle_angle + angle) % math.tau
    
    def on_collide(self, o):
        if isinstance(o, gameTile.GameTile): 
            self._distance -= self._velocity
            return constant.REVERSE
        if isinstance(o, bullet.Bullet): return constant.DESTRUCT
        return constant.REVERSE

    def get_velocity(self):
        return self._velocity
    
    def set_velocity(self, velocity):
        self._velocity = velocity

    def get_nozzle_angle(self):
        return self._nozzle_angle 

    def set_nozzle_angle(self, angle):
        self._nozzle_angle = angle

    def get_old_nozzle_angle(self):
        return self._old_nozzle_angle

    def get_nozzle_length(self):
        return self._nozzle_length

    def get_frame(self):
        return int(self._distance/8) % 4

    def refresh(self):
        super().refresh()
        self._old_nozzle_angle = self._nozzle_angle

    # Property Class
    velocity = property(get_velocity, set_velocity)
    nozzle_angle = property(get_nozzle_angle, set_nozzle_angle)
    nozzle_length = property(get_nozzle_length)
    old_nozzle_angle = property(get_old_nozzle_angle)
    frame = property(get_frame)
    
