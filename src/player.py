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

    # Assigns the player the ID of the tank in the gameGrid which they can control.
    def get_colour(self):
        return self._colour
    
    # Gets the colour scheme for the tank for this player.
    def set_colour(self, colour):
        self._colour  = colour

    # Sets the colour scheme of the tank for this player.
    def set_controller(self, controller):
        self._controller = controller

    # Updates the actions this player is trying to do w/ their tank.
    def update(self, grid):
        if tank_id != None:
            if not self._controller.update(self._tank_id, grid):
                self._tank_id = None


    # Property Class | Setters | Getters
    tank_id = property(get_tank_id, assign_tank)
    colour = property(get_colour, set_colour)
    controller = property().setter(set_controller)