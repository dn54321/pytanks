# Python Libraries
import math
import configparser

# Project Libraries
from src import keyBind, tankController, constant
from lib import VMath

class PlayerController(tankController.TankController):
    def __init__(self, object_id):
        super().__init__(object_id)
        self._bit_key = keyBind.KeyBind()
    
    def forward(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity < 8: tank.velocity += 1
        grid.move_object(self.object_id, tank.velocity)

    def stop(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity != 0: tank.velocity -= abs(tank.velocity)/tank.velocity
        grid.move_object(self.object_id, tank.velocity)
    
    def reverse(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity >= -4: tank.velocity -= 2
        grid.move_object(self.object_id, tank.velocity)
    
    def rotate_left(self, grid):
        tank = grid.get_object(self._object_id)
        angle = -math.pi/60
        grid.rotate_object(self.object_id, angle)

    def rotate_right(self, grid):
        tank = grid.get_object(self._object_id)
        angle = math.pi/60
        grid.rotate_object(self.object_id, angle)
    
    def update(self, grid):
        key = self._bit_key.get_keys()
        vertical = constant.FORWARD | constant.REVERSE
        horizontal = constant.LEFT | constant.RIGHT
        if (key & vertical) and key & vertical != vertical:
            if key & constant.FORWARD: self.forward(grid)
            else: self.reverse(grid)
        else:
            self.stop(grid)
        if (key & horizontal) and key & horizontal != horizontal:
            if key & constant.LEFT: self.rotate_left(grid)
            else: self.rotate_right(grid)
        if key & constant.FIRE:
            self.shoot(grid)

    def shoot(self, grid):
        pass