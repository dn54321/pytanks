from src import mapLoader, gameTile, gameGrid, constant, tankController, keyBind, playerController
from src.gameObjects import tank
import time
import pygame
from lib import VMath
# Private Helper functions
size = [800, 800]
screen = pygame.display.set_mode(size)
temp = []
line = []
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
        self._itop = {}
        self._keybind = keyBind.KeyBind()
    def add_player(self, player):
        self._players.append(player)

    def update_physics(self):
        for controller in self._grid.controllers:
            controller.update(self._grid)
            
    def update_frames(self):
        pass

    def start(self):
        tick = 0
        tick_length = 1e+9/constant.TICKS
        frames = 0
        fps = 0
        loading_time = constant.TICKS*5
        render = self._renderer
        while True:
            tick = (tick+1) % constant.TICKS
            if loading_time: loading_time -= 1
            else: self.update_physics()
            ns_start = ns = time.time_ns()
            while ns-ns_start < tick_length:
                period = min((ns-ns_start)/(tick_length), 1) # Fraction, how long till end of tick
                ##############################################
                self.draw(period, loading_time)
                w, h = size[0], size[1]
                render.draw_text(screen, (w-300,10), "FPS: "+ str(fps), 500, colour=(255,255,0))
                render.draw_text(screen, (w-200,10), "TICKS: "+ str(tick), 500, colour=(255,255,0))
                if 0 < loading_time < constant.TICKS:
                    pos = w/2, h/2
                    render.draw_text(screen, pos, "- START -", 5000)
                ##############################################
                pygame.display.flip()
                pygame.event.pump()
                ns = time.time_ns()
                frames += 1
            if not tick:
                fps = frames
                frames = 0

    def draw_hitbox(self, tick, clock):
        clock.tick(constant.TICKS)
        screen = pygame.display.set_mode(size).fill((255,255,255))
        for obj in self._grid.objects:
            pygame.draw.polygon(screen, (0,0,0), obj.get_hitbox(to_int=True))
    
    def draw(self, period, stage):
        surface = self.render_entities(period, stage)
        screen.blit(surface, (0,0))

    def draw_text(self, surface, val, hor):
        font = pygame.font.SysFont('arial', 20)
        text = font.render(val, 1, pygame.Color("coral"))
        surface.blit(text, (hor,0))

    def load_map(self, url):
        stage = mapLoader.MapLoader()
        stage.load(url)
        stage.build(len(self._players))
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
                tb = obj.tile_boundary
                bounds = _expand_one(tb, stage.width, stage.height)
                (x0,y0),(x1,y1) = bounds
                for x in range(x0,x1+1):
                    for y in range(y0,y1+1):
                        if tb[0][0]<=x<=tb[1][0] and tb[0][1]<=y<=tb[1][1]: 
                            grid[x][y].append(id)
                        else:
                            grid[x][y].insert(0,-id) 
                            
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
            self._itop[id] = player
            i += offset

    def render_entities(self, time_step, stage):
        surface = self._bg.copy().convert_alpha()
        controllers = self._grid.get_controllers()
        show_name = (self._keybind.get_keys() & constant.SHOW_NAMES) | stage
        for i in range(len(controllers)):
            controller = controllers[i]
            obj = self._grid.get_object(controller.object_id)
            if isinstance(obj, tank.Tank):
                if not isinstance(controller, playerController.PlayerController): stage = False
                player = self._itop[controller.object_id]
                self._renderer.render_tank(surface, obj, player, time_step, show_name=show_name, show_arrow=stage)
            else:
                self._renderer.render_bullet(surface, obj, time_step, colour=None)



        gz = constant.GRID_SIZE
        for ff in temp:
            path = pygame.Surface((gz,gz))
            path.set_alpha(128)
            path.fill(ff[2])
            surface.blit(path,ff[0:2])
        
        for lin in line:
            pygame.draw.line(surface, (0,0,0), lin[0], VMath.translate(lin[0],500,lin[1]))
        return surface