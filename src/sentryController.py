# Python Libraries
import math
import configparser

# Project Libraries
from src import keyBind, tankController, constant, bulletController
from src.gameObjects import bullet
from lib import VMath, utils


#testing
from src import game
import pygame

class SentryController(tankController.TankController):
    def __init__(self, object_id):
        super().__init__(object_id)
        self._amap = None

    def setup(self, grid, point=None):
        angles = []
        tank = grid.get_object(self._object_id)
        self.get_angles(math.degrees(tank.angle), tank, angles)
        self._amap = utils.array_2d(grid.width, grid.height, [])
        for angle in angles:
            beam(grid, tank.position, angle)

    #ref paper: http://www.cse.yorku.ca/~amana/research/grid.pdf 
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


    def get_angles(self, angle, tank, grid, dp=None):
        if dp is None: dp = [False]*360
        if dp[angle]: return
        dp[angle] = True
        grid.append(math.radians(angle))
        a1 = angle+int(math.degrees(self._nozzle_rotation))
        a2 = angle+int(math.degrees(self._tank_rotation))
        get_angles(a1, tank, grid, dp)
        get_angles(a2, tank, grid, dp)



    def update(self, grid):
        tank = grid.get_object(self._object_id)
        #self.beam(grid, tank.position, tank.angle)
        self.idle(grid)
