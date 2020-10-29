import abc
from src import controller

class BulletController(controller.Controller):
    def __init__(self, object_id):
        super().__init__(object_id)
        
    @abc.abstractmethod
    def forward(self, grid):
        pass
    
    @abc.abstractmethod
    def update(self, grid):
        pass