# Python Libraries
import math
import configparser
from math import sin, cos, tan, copysign

# Project Libraries
from src import keyBind, tankController, constant, bulletController, playerController
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
            bp, bep, c = self.beamV3(grid, tank.position, math.radians(angle), tank.hitbox)
            for p,b in bp: self._2damap[p[0]][p[1]].append(i*10+constant.BULLET_BOUNCE-b)
            self._amap[i] = bep
            
    # Ref Paper used: http://www.cse.yorku.ca/~amana/research/grid.pdf 
    # Predicts the path of a bullet. Does not consider moving entities.
    # This is the third revision of the algorithm which works efficiently 
    # and accurately. The algorithm shoots two rays (beams) from an imaginary 
    # bullet, one beam for each of the bullet walls. When a beam collides,
    # calculations are done to determine the bounce path taken by the bullet.
    #
    # There are three scenarios that could happen when a bullet collides towards
    # a wall:
    # 1. The beams hit the same side of the wall.
    # 2. One beam hits the X axis of the wall whilst another beam hits the Y axis.
    # 3. One beam hits one wall, the other beam hits another wall.
    #
    # for 1. the bounce is simply 180-theta where theta is the angle of the wall
    # for 2. The bullet head hits the corner of the wall, from there, the center
    # position of the bullet can be calculated. To find what angle the wall is, 
    # we calculate whether a ray that passes through the center point of the bullet
    # will collide with the y or x axis of the beam and use the angle of the wall that
    # collided with the beam.
    # for 3. the beam that hits a wall first will be used to calculate the bounce/
    # position.

    def beamV3(self, grid, pos, angle, hitbox, bounce=constant.BULLET_BOUNCE, old_angle=None):
        if old_angle is None: old_angle = angle
        new_position = None
        new_angle = None
        cpb = [0]*2             # collision point boundary (1: x, 2: y)
        hc = [0]*2              # left or right point of bullet wall, has it collided?
        ctr = -1                # counter, once a collision with one of the ray hits,
                                # the 2nd ray can move only up to two steps.
        bpt = []

        # Return Variables #
        bp = []                 # store the grid index of the bullet path
        bep = []                # stores the bullet end points
        ct = False              # Determines whether trajectory has collided with tank

        gz = constant.GRID_SIZE
        (bw,bh) = constant.BULLET_SIZE  # Bullet width/height
        
        # Get the starting position of the two rays which define the trajectory
        # the bullet will take and find the grid position of those two points.
        offset = VMath.rotate([(0.5*bw,0.5*bh),(0.5*bw,-0.5*bh)], angle)
        pts = VMath.sum(pos,offset[0]), VMath.sum(pos,offset[1])
        gpts = [int(pts[0][0]/gz),int(pts[0][1]/gz)],[int(pts[1][0]/gz),int(pts[1][1]/gz)]


        ### DEBUGGER ###
        if bounce == constant.BULLET_BOUNCE: 
            game.temp = []
            game.line = []
        game.line.append([pts[0], angle])
        game.line.append([pts[1], angle])
        #print(f"b: {bounce}, l1: y-{pts[0][1]} = {math.tan(angle)}(x-{pts[0][0]})")
        #print(f"b: {bounce}, l2: y-{pts[1][1]} = {math.tan(angle)}(x-{pts[1][0]})")
        # Calculate direction vector

        # Find velocity vector of the bullet
        h_angle = math.pi/2 - angle
        vx,vy = sin(h_angle),cos(h_angle)
        sx,sy = int(math.copysign(1,vx)), int(math.copysign(1,vy))
        
        # Given a velocity vector V and intial position U, find dx, dy
        # such that U+V*dx and U+V*dy will be a point that intersect
        # the x and y grid edges respectively. Note, mxdx, mxdy is the 
        # distance the projectile needs to travel one horizontal/vertical grid tile.

        dx = [math.inf]*2
        dy = [math.inf]*2
        if round(vx,5):
            mxdx = gz/abs(vx)
            dx[0] = mxdx-(pts[0][0]*sx%gz)*sx/vx
            dx[1] = mxdx-(pts[1][0]*sx%gz)*sx/vx
            
        if round(vy,5):
            mxdy = gz/abs(vy)
            dy[0] = mxdy-(pts[0][1]*sy%gz)*sy/vy
            dy[1] = mxdy-(pts[1][1]*sy%gz)*sy/vy
            
        mx = 1 if dx[1]<dx[0] else 0        # Find min_x
        my = 1 if dy[1]<dy[0] else 0        # Find min_y

        # March dx/dy as specified in paper and stop marching when a collision
        # occurs. Keep track of what collision happened first and whether it
        # was a horizontal or vertical collision.

        while not (cpb[0] and cpb[1]) and ctr:
            if dx[mx] < dy[my]:
                gpts[mx][0] += sx
                if self.check_solid(grid[gpts[mx][0],gpts[mx][1]]):
                    cpb[mx] = 'x'
                    ctr = 3
                    hc[mx] = hc[1-mx]+1
                    if hc[my]: my = 1 - my
                else: 
                    dx[mx] += mxdx
                    bgpt = gpts[mx][0],gpts[mx][1]
                    if not bpt or bpt[-1] != bgpt: bpt.append(bgpt)
                if not hc[1-mx]: mx = 1 - mx
            else:
                gpts[my][1] += sy
                if self.check_solid(grid[gpts[my][0],gpts[my][1]]):
                    cpb[my] = 'y'
                    ctr = 3
                    hc[my] = hc[1-my]+1
                    if hc[mx]: mx = 1 - mx
                else: 
                    dy[my] += mxdy
                    bgpt = gpts[mx][0],gpts[mx][1]
                    if not bpt or bpt[-1] != bgpt: bpt.append(bgpt)
                if not hc[1-my]: my = 1 - my        
            ctr -= 1

        # From the three scenarios mentioned above
        # Find collision by X or Y axis
        # Find collsiion is at p1 or p2
        angles = [(math.pi-angle)%math.tau, (-angle)%math.tau]
        cpt = 0
        # Get position/angle based on scenario
        if VMath.equals(gpts[mx],gpts[my]) and cpb[0] and cpb[1] and cpb[0] != cpb[1]:
            grid_corner = (gpts[0][0]*gz+0.5*gz*(1-sx),gpts[0][1]*gz+0.5*gz*(1-sy))
            bp0 = collision.line_intersection2(pts[0],angle,grid_corner,angle-math.pi/2)
            bpd = VMath.distance(bp0, grid_corner)
            if VMath.distance(bp0, grid_corner) > 0.5*bh: ca = 1 if sx*sy>0 else 0
            else: ca = 0 if sx*sy>0 else 1
            new_pos = VMath.subtract(bp0, offset[0])
            new_angle = angles[1-ca]
        else:   
            if hc[0] == 1: ca = ord(cpb[0]) - ord('x')
            else: ca = ord(cpb[1]) - ord('x')                           
            if hc[1] == 1: cpt = 1 
            d = dy[cpt] if ca else dx[cpt]
            pt = (pts[cpt][0]+vx*d,pts[cpt][1]+vy*d)
            new_pos = VMath.subtract(pt, offset[cpt])
            new_angle = angles[ca]

        # Check if this point has passed the tank
        cpt = None
        pts2 = VMath.sum(new_pos,offset[0]), VMath.sum(new_pos,offset[1])
        if bounce < constant.BULLET_BOUNCE:
            cpt = collision.line_square((pts[0], pts2[0]), hitbox)
            if cpt: cpt = VMath.subtract(cpt,offset[0])
            else:
                cpt = collision.line_square((pts[1], pts2[1]), hitbox)
                if cpt: cpt = VMath.subtract(cpt,offset[1])

        if cpt: 
            bep.append(cpt)
            ct = True
            gx, gy = int(cpt[0]/gz), int(cpt[1]/gz)
        else:
            bep.append(new_pos)
            if bounce:
                bpf, bepf, ctf = self.beamV3(grid, new_pos, new_angle, hitbox, bounce-1, old_angle)
                bep.extend(bepf)
                bp.extend(bpf)
                if ctf: ct = True

        if not cpt: 
            for p in bpt: bp.append((p,bounce))
        else:
            for p in bpt:
                if p[0]*sx < gx*sx and p[1]*sy < gy*sy: bp.append((p,bounce))

        return bp, bep, ct

    # Determines if this is a tile and if the tile is a solid 
    def check_solid(self, tile):
        if tile: return tile._stationary and tile.solid
        return False


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
            



    def update(self, grid):
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
            print(f"tank: {math.degrees(tank.nozzle_angle)}, to_angle: {self._itoa[angle_index]}")
            print(angle_diff)
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
    
