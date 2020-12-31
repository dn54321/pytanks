from random import randint, shuffle

import pygame

from lib import utils, VMath
from src import constant


class GameRender:
    _direction = {
        0: (0,0),
        constant.UP: (0,-1),
        constant.DOWN: (0,1),
        constant.LEFT: (-1,0),
        constant.RIGHT: (1,0),
        constant.LEFT|constant.UP: (-1,-1),
        constant.RIGHT|constant.UP: (1,-1),
        constant.LEFT|constant.DOWN: (-1,1),
        constant.RIGHT|constant.DOWN: (1,1)
    }

    def __init__(self, surface, width, height):
        self._surface = surface
        self._sprite_sheet = self.get_tileset()
        self._bitmap = None
        self._width = width
        self._height = height
        self._cursor_pos = (0,0)

    # Changes the pygame surface to render objects on
    def set_surface(self, surface):
        self._surface = surface

    def get_surface(self):
        return self._surface

    # Goes to row and column of tile to be placed.
    def move_cursor(self, x, y):
        self._cursor_pos = (x,y)

    # Gets 16x16 textures and upscales to 32x32
    def get_tileset(self):
        image = pygame.image.load(constant.TILESET).convert_alpha()
        image_width, image_height = image.get_size()
        cols, rows = int(image_width/16), int(image_height/16)
        tileset = utils.array_2d(rows, cols)
        for x in range(cols):
            for y in range(rows):
                rect = pygame.Rect = (x*16, y*16, 16, 16)
                if y: tileset[x][y] = pygame.transform.scale2x(image.subsurface(rect))
        return tileset
    
    def render_tile(self, obj, x=None, y=None):
        if x is None:
            x = self._cursor_pos[0]*constant.GRID_SIZE
            y = self._cursor_pos[1]*constant.GRID_SIZE
        i,j = obj
        self._surface.blit(self._sprite_sheet[i][j], (x,y))
        
    def render_entity(self, surface, sprite, entity, colour=None, pivot=[0,0]):
        i,j = sprite
        tile = self._spite_sheet[i][j].copy().convert_alpha()
        rot_tile = pygame.transform.rotate(tile, entity.angle)
        center = rot_tile.get_width()/2, rot_tile.get_height()/2
        pos = VMath.subtract(entity.position, center)
        surface.blit(rot_tile, pos)
        

    def render_tank(self, surface, tank, colour=None):
        sprite = (0,0)
        self.render_entity(surface, sprite, tank, colour)

    def get_bullet_sprite(self):
        pass

    # Finds the correct tile wall sprite and returns the 2d index of it.
    def _get_wall_sprite(self):
        key, y_offset = 0, 0
        if self._is_bit(0, [-1,0]): key |= constant.LEFT
        elif self._is_bit(0, [-1,1]) and self._is_bit(1,[0,1]): key |= constant.LEFT
        if self._is_bit(0, [0,-1]): key |= constant.UP
        if self._is_bit(0, [1,0]): key |= constant.RIGHT
        elif self._is_bit(0, [1,1]) and self._is_bit(1,[0,1]): key |= constant.RIGHT
        if self._is_bit(0, [0,1]): y_offset = 4
        elif self._is_bit(0,[0,2]): key |= constant.DOWN
        i,j = GameRender._direction[key]
        return i+7, j+2+y_offset
            
    def get_shadow_sprite(self, bitmap):
        pass
    # Fills the surface with wall tiles.  
    def render_walls(self, bitmap):
        self._bitmap = bitmap
        for i in range(self._width):
            for  j in range(self._height):
                if bitmap[i][j]:
                    self.move_cursor(i,j)
                    tile = self._get_wall_sprite()
                    self.render_tile(tile)
                    
    # Fills the surface with grass tiles.
    def render_background(self):
        for i in range(self._width):
            for j in range(self._height):
                tile = (randint(0,5), 1)
                self.move_cursor(i,j)
                self.render_tile(tile)

    # Places some flowers at valid tile posiitons specified in bitmap
    def render_flowers(self, bitmap):
        has_flower = utils.array_2d(self._width, self._height, False)

        # Stores valid flower positions in a list and shuffles.
        flower_pos = []
        for i in range (self._width):
            for j in range(self._height):
                if bitmap[i][j]: flower_pos.append((i,j))
        shuffle(flower_pos)

        # Looks at a valid flower position and determines if a flower should spawn.
        for i,j in flower_pos:
            grass_count = 0
            flower_count = 0
            for k in [-1,0,1]:
                for l in [-1,0,1]:
                    x = i+k
                    y = j+l
                    if 0<=x<self._width and 0<=y<self._height:
                        if bitmap[x][y]: grass_count += 1
                        if has_flower[x][y]: flower_count += 1
            threshhold = 1 + grass_count*1 + flower_count*5
            if randint(0,100) <= threshhold:
                has_flower[i][j] = True
                flower_tile = (randint(0,4), 2)
                self.move_cursor(i,j)
                self.render_tile(flower_tile)
    
    # checks if the bit of the bitmap at position self._cursor_pos with some offset [offset]
    # is equal to [bit]. Note that this arguement returns false if this position is out of bounds.
    def _is_bit(self, bit, offset=[0,0], bitmap=None): 
        if bitmap is None: bitmap = self._bitmap
        x = self._cursor_pos[0] + offset[0] 
        y = self._cursor_pos[1] + offset[1]
        if 0 <= x < self._width and 0 <= y < self._height:
            return bitmap[x][y] == bit
        return False

    # property
    surface = property(get_surface, set_surface)