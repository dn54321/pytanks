import abc, math
from src import controller, bulletController
from src.gameObjects import bullet
from lib import VMath

class TankController(controller.Controller):
    def __init__(self, object_id):
        super().__init__(object_id)
        self._tank_rotation = math.pi/45
        self._nozzle_rotation = math.pi/90
        self._timer = 0

    def forward(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity < 4: tank.velocity += 1
        tank._distance += tank.velocity
        grid.move_object(self.object_id, tank.velocity)

    def idle(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity != 0: tank.velocity -= abs(tank.velocity)/tank.velocity
        grid.move_object(self.object_id, tank.velocity)
    
    def reverse(self, grid):
        tank = grid.get_object(self._object_id)
        if tank.velocity > 0: tank.velocity -= 2
        if tank.velocity <= 0: tank.velocity = -2
        tank._distance += tank.velocity
        grid.move_object(self.object_id, tank.velocity)
    
    def rotate_tank(self, grid, angle):
        tank = grid.get_object(self._object_id)
        grid.rotate_object(self.object_id, angle)

    def rotate_nozzle(self, grid, angle):
        tank = grid.get_object(self._object_id)
        tank.rotate_nozzle(angle)

    def shoot(self, grid):
        tank = grid.get_object(self._object_id)
        x,y = VMath.translate(tank.position, tank.nozzle_length, tank.nozzle_angle)
        projectile = bullet.Bullet(x,y,tank.nozzle_angle)
        id = grid.add_object(projectile)
        if id: grid.add_controller(bulletController.BulletController(id, self))

    @abc.abstractmethod
    def update(self, grid):
        pass

    # RUNS WHEN A BULLET GETS DESTROYED
    def event_ammo_destroy(self):
        return