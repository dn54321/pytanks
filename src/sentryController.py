# Python Libraries
import math
import configparser
from math import sin, cos, tan, copysign

# Project Libraries
from src import keyBind, tankController, constant, bulletController, playerController, gameTile
from src.gameObjects import bullet
from lib import VMath, utils, collision


#testing
from src import game
import pygame

class SentryController(tankController.TankController):
    def __init__(self, object_id):
        super().__init__(object_id)
        self._2damap = None
        self._amap = []
        self._bullet_bounce = []
        self._asafe = []
        self._itoa = []
        self._atoi = {}
        self._move = []
        self._moves = []
        self._idle = 0
        self._setup = 1
        self._target = None
        self._action = []
        self._health = 3
        
    # 
    def event_ammo_destroy(self):
        self._idle = 0

    def setup(self, grid, point=None):
        angles = []
        tank = grid.get_object(self._object_id)
        self.get_angles(tank, int(math.degrees(tank.nozzle_angle)%360))
        self._2damap = utils.array_2d(grid.width, grid.height)
        for i in range(len(self._itoa)):
            angle = self._itoa[i]
            bp, bep, c = self.beamV3(grid, angle = math.radians(angle))
            for p,b in bp: self._2damap[p[0]][p[1]].append(i*10+constant.BULLET_BOUNCE-b)
            self._amap[i] = bep
            
    # Gets all possible angles the tank can rotate to
    # initial_angle, relative_angle, angle_delta
    def get_angles(self, tank, base_angle, relative_angle=0, angle_delta=0, dp=None, moves=0):
        if dp is None: 
            dp = [-1]*360
            self._moves = [math.inf]*360
            self._move = [False]*360
        net_angle = (base_angle + relative_angle) % 360
        if dp[net_angle] >= 0 and dp[net_angle] <= moves: return
        dp[net_angle] = moves

        if net_angle in self._atoi:
            id = self._atoi[net_angle]
        else:
            id = len(self._itoa)
            self._atoi[net_angle] = id
            self._itoa.append(net_angle)
            self._amap.append([])
            self._bullet_bounce.append([])
            self._asafe.append(True)
        self._moves[relative_angle] = moves
        self._move[relative_angle] = abs(angle_delta)

        a1 = int(math.degrees(self._nozzle_rotation))
        a2 = int(math.degrees(self._tank_rotation))
        self.get_angles(tank, base_angle, (relative_angle+a2)%360, a2, dp, moves+1)
        self.get_angles(tank, base_angle, (relative_angle-a2)%360, a2, dp, moves+1)
        self.get_angles(tank, base_angle, (relative_angle+a1)%360, a1, dp, moves+1)
        self.get_angles(tank, base_angle, (relative_angle-a1)%360, a1, dp, moves+1)

    def target(self, enemy_tank, grid):
        gz = constant.GRID_SIZE
        tank = grid.get_object(self._object_id)
        x,y = enemy_tank.position
        enemy_hitbox = enemy_tank.hitbox
        gx,gy = int(x/gz), int(y/gz)
        t_angle = tank.angle
        mna, mxa = math.inf,-math.inf
        a1, a2 = None, None
        for bullet_angle in self._2damap[gx][gy]:
            trajectory = int(bullet_angle/10)
            bounce = bullet_angle % 10
            if not self._asafe[trajectory]: continue
            l0 = self._amap[trajectory][bounce-1] if bounce !=0 else tank.position 
            l1 = self._amap[trajectory][bounce]
            line = [l0,l1]
            if (collision.line_square(line, enemy_hitbox)):
                bullet_dir = math.atan2(l1[1]-l0[1],l1[0]-l0[0])
                a_diff = VMath.angle_diff(bullet_dir, enemy_tank.angle)
                a_diff = VMath.astc(a_diff)
                if a_diff < mna:
                    a1 = trajectory
                    mna = a_diff
                if a_diff > mxa:
                    a2 = trajectory
                    mxa = a_diff
        if a1 is None and a2 is None: return False
        if a1 == a2: return [a1]
        else: return [a1,a2]
            
    def delete(self):
        if self._health:
            self._health -= 1
        else: return True
        return False


    def update_logic(self, grid):
        tank = grid.get_object(self._object_id)
        if self._setup:
            self.setup(grid)
            self._setup = False
        if self._idle:
            self._idle -= 1
            self.idle(grid)
            return
        if self._target is None:
            for controller in grid.controllers:
                if isinstance(controller, playerController.PlayerController):
                    self._target = grid.get_object(controller.object_id)
                    break
        if not self._action:
            self._action = self.target(self._target, grid)
        if self._action:
            angle_index = self._action[0]
            angle_diff = VMath.angle_diff(tank.nozzle_angle,math.radians(self._itoa[angle_index]))
            angle_diff = round(math.degrees(angle_diff))
           # print(f"tank: {math.degrees(tank.nozzle_angle)}, to_angle: {self._itoa[angle_index]}")
           # print(angle_diff)
            if self._moves[angle_diff] < self._moves[-angle_diff%360]: best_rotation = angle_diff
            else: best_rotation = -angle_diff%360
            best_move = self._move[best_rotation]
            if (self._itoa[angle_index]-math.degrees(tank.nozzle_angle)+540)%360-180>=0:
                sign = 1
            else: sign = -1
            if best_move == 0:
                self.shoot(grid)
                self._action.pop(0)
               # self._idle = constant.TICKS/2
            elif not round(abs(best_move) - math.degrees(self._tank_rotation), 5):
                self.rotate_tank(grid, sign*self._tank_rotation)
            else:
                self.rotate_nozzle(grid, sign*self._nozzle_rotation)
            #tank.nozzle_angle = 2.426007660272118
            #self.rotate_nozzle(grid, self._nozzle_rotation)
            #print(tank._nozzle_angle)
            #self.beamV3(grid, tank.position, tank.nozzle_angle, tank.hitbox)
            #self.shoot(grid)
        
    
