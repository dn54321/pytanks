# project libraries
from src import entity, gameTile, constant
from src.gameObjects import tank

class Bullet(entity.Entity):
    def __init__(self, x, y, angle):
        w,h = constant.BULLET_SIZE
        w,h = w/2, h/2
        hitbox = [(w,-h), (w,h), (-w,h), (-w,-h)]
        super().__init__(x, y, angle, hitbox)
        self._velocity = 10
        self._bounce = constant.BULLET_BOUNCE
        self.force_rotate(angle)
      #  print(f"bullet spawn | position: {x}, {y}, angle: {angle}")
    
    def on_collide(self, o):
        if isinstance(o, Bullet): return constant.DESTRUCT
        if isinstance(o, tank.Tank): return constant.DESTRUCT
        if self._bounce > 0: 
            self._bounce -= 1
            return constant.BOUNCE
        return constant.DESTRUCT

    def get_velocity(self):
        return self._velocity
    
    def set_velocity(self, velocity):
        if velocity > self._terminal_velocity:
           velocity = self._terminal_velocity 
        self._velocity = velocity

    # Property Class
    velocity = property(get_velocity, set_velocity)
    
    
