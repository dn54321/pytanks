import abc
from src import controller

class TankController(controller.Controller):
    def __init__(self, object_id):
        super().__init__(object_id)
    
    @abc.abstractmethod
    def shoot(self, grid):
        pass
    
    @abc.abstractmethod
    def forward(self, grid):
        pass

    @abc.abstractmethod
    def idle(self, grid):
        pass

    @abc.abstractmethod
    def reverse(self, grid):
        pass

    @abc.abstractmethod
    def rotate_left(self, grid):
        pass

    @abc.abstractmethod
    def rotate_right(self, grid):
        pass

    @abc.abstractmethod
    def update(self, grid):
        pass