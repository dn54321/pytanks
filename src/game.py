from src import mapLoader, gameTile, gameGrid, constant
import pygame
# Private Helper functions
size = [800, 800]
screen = pygame.display.set_mode(size)

def _expand_one(bounds, width, height):
    x0,y0 = bounds[0]
    x1,y1 = bounds[1]
    x0 = max(x0-1, 0)
    y0 = max(y0-1, 0)
    x1 = min(x1+1, width-1)
    y1 = min(y1+1, height-1)
    return [(x0,y0), (x1,y1)]

class Game:
    def __init__(self):
        self._grid = None
        self._bg = None
        self._players = []
        self._controllers = []
        
    def add_player(self, player):
        self._player.append(player)

    def update_physics(self):
        for controller in self._grid.controllers:
            controller.update(self._grid)
            
    def update_frames(self):
        pass

    def start(self):
        clock = pygame.time.Clock()
        tick = 0
        while True:
            tick += 1
            if tick > constant.TICKS: tick = 1
            clock.tick(constant.TICKS)
            pygame.event.pump()
            self.update_physics()
            self.draw(clock, tick)

    def draw_hitbox(self, clock, tick):
        screen.fill((255,255,255))
        for obj in self._grid.objects:
            pygame.draw.polygon(screen, (0,0,0), obj.get_hitbox(to_int=True))
        self.draw_text(screen, str(int(clock.get_fps())), 10)
        self.draw_text(screen, str(tick), 30)
        pygame.display.flip()
    
    def draw(self, clock, tick):
        screen.fill((255,255,255))
        screen.blit(self._bg, (0,0))

        self.draw_text(screen, str(int(clock.get_fps())), 10)
        self.draw_text(screen, str(tick), 30)
        pygame.display.flip()

    def draw_text(self, screen, val, hor):
        font = pygame.font.Font(None, 20)
        text = font.render(val, 1, pygame.Color("coral"))
        screen.blit(text, (hor,0))

    def load_map(self, url):
        stage = mapLoader.MapLoader()
        stage.load(url)
        self._bg = stage.generate_surface()
        self._grid = gameGrid.GameGrid(stage.width, stage.height)
        grid = self._grid.get_map()
        stage.build()
        obj = stage.objects
        controllers = 0

        # Fill in map
        for obj in stage.objects:
            id = self._grid.add_object(obj, check_collision=False)
            if isinstance(obj, gameTile.GameTile):
                bounds = _expand_one(obj.tile_boundary, stage.width, stage.height)
                (x0,y0),(x1,y1) = bounds
                for x in range(x0,x1+1):
                    for y in range(y0,y1+1):
                        grid[x][y].append(id)
            else:
                controller = stage.controllers[controllers](id)
                controllers += 1
                self._grid.add_controller(controller)