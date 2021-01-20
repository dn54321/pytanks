# Python Libraries
import math
from math import sin, cos, tan
import configparser

# Project Libraries
from src import keyBind, tankController, constant, bulletController, gameTile
from src.gameObjects import bullet
from lib import VMath

from src import game
import pygame

class PlayerController(tankController.TankController):
    def __init__(self, object_id):
        super().__init__(object_id)
        self._bit_key = keyBind.KeyBind()
        self._is_space = False
        if __debug__: self._key = None
        self._ammo = 3

    def event_ammo_destroy(self):
        self._ammo += 1
   
    def update_logic(self, grid):
        key = self._bit_key.get_keys()
        tank = grid.get_object(self._object_id)
        if __debug__:
            '''
            if self._key is None:
                self._key = 1
                tank = grid.get_object(self._object_id)
                tank._x, tank._y = 244.0690229049188, 88.01884026187207
                tank.rotate(5.51524043630209)
                self._keys = [1,1,1,1,1,1,9,9,9,9,9,9,9,9,1,1,1,1,1,5,5,5,5,5,5,1,9,9,9,9,9,9,9,1,5,5,5,5,5,5,1]
                print(key, end=',')
            if self._keys:
                key = self._keys.pop(0)
            '''

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
            if self._ammo and not (self.is_space or self._timer): 
                self.beamV3(grid)
                self.shoot(grid)
                self.is_space = True
                self._timer = constant.TICKS/2
                self._ammo -= 1
        else: self.is_space = False
