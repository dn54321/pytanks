# Project Library
from src import gameObject, constant

class GameTile(gameObject.GameObject):
    def __init__(self, x0, y0, x1, y1):
        gz = constant.GRID_SIZE
        width = x1-x0+1
        height = y1-y0+1
        self._tile_boundary = [(x0,y0),(x1,y1)]
        x,y = width*gz/2, height*gz/2
        hitbox = [(x,-y), (x,y), (-x,y), (-x,-y)]
        super().__init__((x0+width/2)*gz, (y0+height/2)*gz, hitbox, stationary=True)

    def get_tile_boundary(self):
        return self._tile_boundary

    # Property
    tile_boundary = property(get_tile_boundary)