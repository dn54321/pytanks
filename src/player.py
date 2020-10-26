# Controllers always control a certain tank

class Player:
    def __init__(self, name):
        self._name = name
        self._tank_id = None
        self._colour = None

    # Assigns the player the ID of the tank in the gameGrid which they can control.
    def assign_tank(self, id):
        self._tank_id = id
    
    # Gets the ID of the tank in the gameGrid in which they can control.
    def get_tank_id(self):
        return self._tank_id

    # Sets the controller (the method of which the tank is controlled)s
    def set_controller(self, controller):
        self._controller = controller

    # Updates the actions this player is trying to do w/ their tank.
    def update(self, grid):
        if tank_id != None:
            if not self._controller.update(self._tank_id, grid):
                self._tank_id = None


    # Property Class | Setters | Getters
    tank_id = property(get_tank_id, assign_tank)
    controller = property().setter(set_controller)