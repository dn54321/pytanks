# project libraries
from src import gameObjects, gameObject, gameTile, constant
from src.gameObjects import bullet

class Bullet(gameObject.GameObject):
    def __init__(self, x, y, angle, hitbox):
        w,h = constant.BULLET_SIZE
        w,h = w/2, h/2
        hitbox = [(w,-h), (w,h), (-w,h), (-w,-h)]
        super().__init__(x, y, hitbox)
        self._velocity = 10
        self.rotate(angle)
    
    def on_collide(self, o):
        if isinstance(o, gameTile.GameTile): return constant.BOUNCE
        if isinstance(o, bullet.Bullets): return constant.DESTRUCT
        if isinstance(o, bullet.Tank): return constant.DESTRUCT
        return constant.BOUNCE

    def get_velocity(self):
        return self._velocity
    
    def set_velocity(self, velocity):
        if velocity > self._terminal_velocity:
           velocity = self._terminal_velocity 
        self._velocity = velocity

    # Property Class
    velocity = property(get_velocity, set_velocity)
    
    
