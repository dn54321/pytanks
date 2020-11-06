# Python Libraries
import math
import configparser

# Project Libraries
from src import keyBind, tankController, constant, bulletController
from src.gameObjects import bullet
from lib import VMath

class PlayerController(tankController.TankController):
    def __init__(self, object_id):
        super().__init__(object_id)
        self._bit_key = keyBind.KeyBind()
        self._tank_rotation = math.pi/45
        self._nozzle_rotation = math.pi/90
        self._timer = 0
        self._is_space = False
        self._ammo = 3
        if __debug__: self._key = None
        
    def forward(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity < 4: tank.velocity += 1
        grid.move_object(self.object_id, tank.velocity)

    def idle(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity != 0: tank.velocity -= abs(tank.velocity)/tank.velocity
        grid.move_object(self.object_id, tank.velocity)
    
    def reverse(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity > 0: tank.velocity -= 2
        if tank.velocity <= 0: tank.velocity = -2
        grid.move_object(self.object_id, tank.velocity)
    
    def rotate_tank(self, grid, angle):
        tank = grid.get_object(self._object_id)
        grid.rotate_object(self.object_id, angle)

    def rotate_muzzle(self, grid, angle):
        tank = grid.get_object(self._object_id)
        tank.nozzle_angle += angle

    def shoot(self, grid):
        tank = grid.get_object(self._object_id)
        x,y = VMath.translate(tank.position, tank.muzzle_length, tank.muzzle_angle)
        projectile = bullet.Bullet(x,y,tank.muzzle_angle)
        id = grid.add_object(projectile)
        grid.add_controller(bulletController.BulletController(id, self))

    def increment_ammo(self):
        self._ammo += 1
        
    def update(self, grid):
        key = self._bit_key.get_keys()
        if __debug__:
            if self._key is not key:
                self._key = key
                print(f"key press: {bin(key)}")

        vertical = constant.FORWARD | constant.REVERSE
        horizontal = constant.LEFT | constant.RIGHT
        nozzle_turn = constant.NOZZLE_LEFT | constant.NOZZLE_RIGHT
        if self._timer > 0: self._timer -= 1
        if (key & horizontal) and key & horizontal != horizontal:
            if key & constant.LEFT: self.rotate_tank(grid, -self._tank_rotation)
            else: self.rotate_tank(grid, self._tank_rotation)
        if (key & nozzle_turn) and key & nozzle_turn != nozzle_turn:
            if key & constant.NOZZLE_LEFT: self.rotate_nozzle(grid, -self._nozzle_rotation)
            else: self.rotate_nozzle(grid, self._nozzle_rotation)
        if (key & vertical) and key & vertical != vertical:
            if key & constant.FORWARD: self.forward(grid)
            else: self.reverse(grid)
        else: self.idle(grid)
        if key & constant.FIRE:
            if self._ammo and not (self.is_space and self._timer): 
                self.shoot(grid)
                self.is_space = True
                self._timer = constant.TICKS
                self._ammo -= 1
        else: self.is_space = False
