# Python Libraries
import math
import configparser

# Project Libraries
from src import keyBind, tankController, constant, bulletController
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

    def increment_ammo(self):
        self._ammo += 1

    def beam(self, grid, pos, angle):
        gz = constant.GRID_SIZE
        x,y = pos
        gx,gy = int(x/gz), int(y/gz)
        h_angle = math.pi/2 - angle
        vx,vy = math.sin(h_angle),math.cos(h_angle)
        sx,sy = int(math.copysign(1,vx)), int(math.copysign(1,vy))
        dx,dy = math.inf, math.inf
        if round(vx,5): 
            dx = (0.5*gz*(1+sx)-(x%gz))/vx
            mxdx = gz/abs(vx)
        if round(vy,5): 
            dy = (0.5*gz*(1+sy)-(y%gz))/vy
            mxdy = gz/abs(vy)

        game.temp = []
        while not self.check_solid(grid[gx,gy]):
           # if angle not in self._amap[gx][gy]:
           #     self._amap[gx][gy].append(angle)
            if (dx < dy):
                dx += mxdx
                gx += sx
            else:
                dy += mxdy
                gy += sy
            game.temp.append((gx*gz,gy*gz))
        game.temp.append((gx*gz,gy*gz))
        self.check_solid(grid[gx,gy])

    def check_solid(self, tile):
        if tile: return tile._stationary and tile.solid
        return False

        
    def update(self, grid):
        key = self._bit_key.get_keys()
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
                self.shoot(grid)

                tank = grid.get_object(self._object_id)
                self.beam(grid, tank.position, tank.nozzle_angle)


                self.is_space = True
                self._timer = constant.TICKS/2
                self._ammo -= 1
        else: self.is_space = False
