import abc

class Controller(abc.ABC):
    def __init__(self, object_id):
        self._object_id = object_id

    def get_object_id(self):
        return self._object_id

    def set_object_id(self, object_id):
        self._object_id = object_id

    def delete(self):
        return True

    def update(self, grid):
        entity = grid.get_object(self._object_id)
        entity.refresh()
        self.update_logic(grid)

    @abc.abstractmethod
    def update_logic(self, grid):
        pass
    # property
    object_id = property(get_object_id, set_object_id)