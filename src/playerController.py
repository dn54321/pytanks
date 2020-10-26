# Python Libraries
import math
import configparser

# Project Libraries
from src import keyBind, tankController, constant
from lib import VMath

class PlayerController(tankController.TankController):
    def __init__(self, object_id):
        super.__init__(object_id)
        self._bit_key = keyBind.KeyBind()

    def shoot(self, grid):
        pass
    
    def forward(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity < 8: tank.velocity += 1
        pos = VMath.translate(tank.position, tank.velocity, tank.angle)
        grid.move_object(id, pos)

    def stop(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity > 1: tank.velocity -= 1
        pos = VMath.translate(tank.position, tank.velocity, tank.angle)
        grid.move_object(id, pos)
    
    def reverse(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity >= 4: tank.velocity -= 4
        else: tank.velocity = 0
        pos = VMath.translate(tank.position, tank.velocity, tank.angle)
        grid.move_object(id, pos)
    
    def rotate_left(self, grid):
        tank = grid.get_object(self._object_id)
        angle = -math.pi/90
        grid.rotate_object(id, angle)

    def rotate_right(self, grid):
        tank = grid.get_object(self._object_id)
        angle = math.pi/90
        grid.rotate_object(id, angle)
    
    def update(self, grid):
        key = self._bit_key.get_keys()
        vertical = constant.FORWARD | constant.REVERSE
        horizontal = constant.LEFT | constant.RIGHT
        if key is not constant.IDLE:
            if (key & vertical) and key & vertical != vertical:
                if key & constant.FORWARD: self.forward(grid)
                else: self.reverse(grid)
            if (key & horizontal) and key & horizontal != horizontal:
                if key & constant.LEFT: self.rotate_left(grid)
                else: self.rotate_right(grid)
            if key & constant.FIRE:
                self.shoot(grid)