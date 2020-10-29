class Animation:
    def __init__(self, id):
        self._id = id
        self._translation = 0
        self._angle = 0

    def add_translation(self, new_position):
        self._translation = new_position
    def add_angle(self, new_angle):
        self._angle = new_angle
    
    def get_state(current_frame, max_frame, object_list):
        obj = object_list[id]
        obj.get_position()
        if ()