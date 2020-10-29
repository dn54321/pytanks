import abc
from src import controller, gameGrid

class BulletController(controller.Controller):
    def __init__(self, object_id):
        super().__init__(object_id)
        
    @abc.abstractmethod
    def forward(self, grid):
        obj = grid.objects[self.object_id]
        grid.move_object(id, obj.velocity)
    
    @abc.abstractmethod
    def update(self, grid):
        self.foward(grid)