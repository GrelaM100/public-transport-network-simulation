class Bus:
    def __init__(self, env, line_colour, future_stops, size, from_end_to_start=None):
        self.env = env
        self.line_colour = line_colour
        self.future_stops = future_stops.copy()
        self.passengers = []
        self.size = size
        if from_end_to_start is not None:
            self.future_stops.reverse()

    def __str__(self):
        if len(self.future_stops) != 0:
            return "Autobus linii " + self.line_colour + " na przystanku " + self.future_stops[0]
        else:
            return "Autobus linii " + self.line_colour + " zjeżdża do zajezdni"

    def drive_from_stop(self):
        current_stop = self.future_stops.pop(0)
        if len(self.future_stops) == 0:
            end_of_the_line = True
        else:
            end_of_the_line = False
        return [current_stop, end_of_the_line]

    def drop_passengers_off(self):
        current_stop = self.future_stops[0]
        dropped_passengers = []
        for passenger_in_bus in self.passengers:
            if passenger_in_bus.destination_stop == current_stop:
                passenger_in_bus.current_stop = current_stop
                dropped_passengers.append(passenger_in_bus)
        for passenger in dropped_passengers:
            self.passengers.remove(passenger)
        return dropped_passengers

    def take_passengers(self, passengers_everywhere):
        current_stop = self.future_stops[0]
        taken_passengers = []
        for passenger in passengers_everywhere:
            if passenger.current_stop == current_stop and \
                    passenger.destination_stop in self.future_stops and \
                    len(self.passengers) < self.size:
                passenger.current_stop = "drodze"
                self.passengers.append(passenger)
                taken_passengers.append(passenger)
        return taken_passengers
