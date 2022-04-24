class Stop:
    def __init__(self, name, x_position=-1, y_position=-1):
        self.name = name
        self.x_position = x_position
        self.y_position = y_position
        self.passengers_at_stop = []
        self.stop_gui = None

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.x_position, self.y_position))

    def add_passenger(self, passenger):
        self.passengers_at_stop.append(passenger)

    def remove_passenger(self, passenger):
        self.passengers_at_stop.remove(passenger)

