# project libraries
from src import gameObjects, gameObject, gameTile, constant
from src.gameObjects import bullet

class Tank(gameObject.GameObject):
    def __init__(self, x, y, angle):
        sz = constant.TANK_SIZE/2
        gz = constant.GRID_SIZE
        x,y = x*gz+gz/2, y*gz+gz/2
        hitbox = [(sz,-sz), (sz,sz), (-sz,sz), (-sz,-sz)]
        super().__init__(x, y, hitbox)
        self._velocity = 0
        self._acceleration = 1
        self._terminal_velocity = 5
        self.rotate(angle)
    
    def on_collide(self, o):
        if isinstance(o, gameTile.GameTile): return constant.REVERSE
        if isinstance(o, bullet.Bullet): return constant.DESTRUCT
        return constant.REVERSE

    def get_velocity(self):
        return self._velocity
    
    def set_velocity(self, velocity):
        if velocity > self._terminal_velocity:
           velocity = self._terminal_velocity 
        self._velocity = velocity

    # Property Class
    velocity = property(get_velocity, set_velocity)
    
    
