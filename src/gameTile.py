# Project Library
from src import gameObject, constant

class GameTile(gameObject.GameObject):
    def __init__(self, x0, y0, x1, y1):
        gz = constant.GRID_SIZE
        self._tile_boundary = [(x0,y0),(x1,y1)]
        x0, y0, x1, y1 = x0*gz, y0*gz, (x1+1)*gz, (y1+1)*gz
        hitbox = [(x1,y0), (x1,y1), (x0,y1), (x0,y0)]
        super.__init__(x0+gz/2, y0+gz/2, hitbox, stationary=True)

    def get_tile_boundary(self):
        return self._tile_boundary

    # Property
    tile_boundary = property(get_tile_boundary)