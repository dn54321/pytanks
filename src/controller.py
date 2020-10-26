import abc

class Controller(abc.ABC):
    def __init__(self, object_id):
        self._object_id = object_id

    def get_object_id(self):
        return self._object_id

    def set_object_id(self, object_id):
        self._object_id = object_id

    @abc.abstractmethod
    def update(self, gameGrid):
        pass