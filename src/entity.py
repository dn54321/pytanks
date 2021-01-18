from src import gameObject
import math
class Entity(gameObject.GameObject):
    def __init__(self, x, y, angle, hitbox, solid=True):
        super().__init__(x, y, hitbox)
        self._old_position = (x,y)
        self._old_angle = angle

    def move(self, distance):
        self._old_position = self._position
        if distance: super().move(distance)
    
    def teleport(self, position):
        self._position = position
        self._old_positon = position
    
    def force_rotate(self, angle):
        super().rotate((angle-self._angle)%math.tau)
        self._old_angle = angle
        
    def rotate(self, angle):
        self._old_angle = self._angle
        if angle: super().rotate(angle)

    def get_old_position(self):
        return self._old_position
    
    def get_old_angle(self):
        return self._old_angle
    
    def refresh(self):
        self._old_position = self._position
        self._old_angle = self._angle

    # property
    old_position = property(get_old_position)
    old_angle = property(get_old_angle)
