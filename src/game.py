from src import mapLoader, gameTile, gameGrid, constant, tankController
from src.gameObjects import tank
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
        self._bg = pygame.display.set_mode(size)
        self._players = []
        
    def add_player(self, player):
        self._players.append(player)

    def update_physics(self):
        for controller in self._grid.controllers:
            controller.update(self._grid)
            
    def update_frames(self):
        pass

    def start(self):
        tick = 0
        clock = pygame.time.Clock()
        while True:
            tick += 1
            if tick > constant.TICKS: tick = 1
            pygame.event.pump()
            self.update_physics()
            self.draw(tick, clock)

    def draw_hitbox(self, tick, clock):
        clock.tick(constant.TICKS)
        screen = pygame.display.set_mode(size).fill((255,255,255))
        for obj in self._grid.objects:
            pygame.draw.polygon(screen, (0,0,0), obj.get_hitbox(to_int=True))
        self.draw_text(screen, str(int(clock.get_fps())), 10)
        self.draw_text(screen, str(tick), 30)
        pygame.display.flip()
    
    def draw(self, tick, clock):
        surface = self.render_entities(tick)
        clock.tick(constant.TICKS)
        self.draw_text(surface, str(int(clock.get_fps())), 10)
        self.draw_text(surface, str(tick), 30)
        screen.blit(surface, (0,0))
        pygame.display.flip()

    def draw_text(self, surface, val, hor):
        font = pygame.font.Font(None, 20)
        text = font.render(val, 1, pygame.Color("coral"))
        surface.blit(text, (hor,0))

    def load_map(self, url):
        stage = mapLoader.MapLoader()
        stage.load(url)
        stage.build()
        self._bg = stage.render_surface()
        self._grid = gameGrid.GameGrid(stage.width, stage.height)
        self._renderer = stage.get_renderer()
        grid = self._grid.get_map()
        
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

    def assign_tanks(self):
        player_sz = len(self._players)
        controllers = self._grid.get_controllers()
        offset = len(controllers) - player_sz + 1
        i = 0
        for player in self._players:
            id = controllers[i].get_object_id()
            player.assign_tank(id)
            i += offset

    def render_entities(self, tick):
        surface = self._bg.copy().convert_alpha()
        controllers = self._grid.get_controllers()
        for i in range(len(controllers)):
            controller = controllers[i]
            obj = self._grid.get_object(controller.object_id)
            if isinstance(obj, tank.Tank):
                colour = self._players[i].colour
                self._renderer.render_tank(surface, obj, colour=colour)
            else:
                self._renderer.render_bullet(surface, obj, colour=None)
        return surface