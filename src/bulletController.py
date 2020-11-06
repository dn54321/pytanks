import abc
from src import controller, gameGrid

class BulletController(controller.Controller):
    def __init__(self, object_id, controller):
        super().__init__(object_id)
        self._controller = controller
        
    def forward(self, grid):
        try: obj = grid.get_object(self.object_id)
        except: return
        else: grid.move_object(self._object_id, obj.velocity)

    def delete(self):
        self._controller.increment_ammo()

    def update(self, grid):
        self.forward(grid)