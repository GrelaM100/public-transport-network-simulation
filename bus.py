from stop import Stop
import time


class Bus:
    def __init__(self, env, line_name, line_colour, future_stops, size, from_end_to_start=None):
        self.env = env
        self.line_name = line_name
        self.line_colour = line_colour
        self.future_stops = future_stops.copy()
        self.passengers = []
        self.size = size
        if from_end_to_start is not None:
            self.future_stops.reverse()
        self.bus_gui = None
        self.canvas = None

    def __str__(self):
        if len(self.future_stops) != 0:
            return "Autobus linii " + self.line_colour + " na przystanku " + str(self.future_stops[0])
        else:
            return "Autobus linii " + self.line_colour + " zjeżdża do zajezdni"

    def drive_from_stop(self):
        current_stop = self.future_stops.pop(0)
        if len(self.future_stops) == 0:
            end_of_the_line = True
            self.canvas.delete(self.bus_gui)
        else:
            end_of_the_line = False
            self.visualize_bus_at_stop(current_stop, self.canvas)
        return [current_stop, end_of_the_line]

    def drop_passengers_off(self):
        current_stop = self.future_stops[0]
        dropped_passengers = []
        if len(self.future_stops) > 1:
            for passenger_in_bus in self.passengers:
                passenger_in_bus.at_stop(current_stop)
                if passenger_in_bus.decide_to_hop_off(current_stop, self.future_stops[1]):
                    passenger_in_bus.current_stop = current_stop
                    dropped_passengers.append(passenger_in_bus)
            for passenger in dropped_passengers:
                self.passengers.remove(passenger)
        else:
            dropped_passengers == self.passengers.copy()
        return dropped_passengers


    def take_passengers(self, passengers_everywhere):
        current_stop = self.future_stops[0]
        taken_passengers = []
        if len(self.future_stops) > 1:
            for passenger in passengers_everywhere:
                if passenger.current_stop == current_stop and \
                        passenger.decide_to_hop_on(self.future_stops[1]) and \
                        len(self.passengers) < self.size:
                    passenger.current_stop = Stop('drodze')
                    if passenger in current_stop.passengers_at_stop:
                        current_stop.remove_passenger(passenger)
                    self.passengers.append(passenger)
                    taken_passengers.append(passenger)
            for passenger in self.passengers:
                passenger.time_commuting += 1
        return taken_passengers

    def visualize_bus_at_stop(self, stop, canvas):
        x_position = stop.x_position
        y_position = stop.y_position
        if x_position != -1 and y_position != -1:
            if self.bus_gui is None:
                self.canvas = canvas
                self.bus_gui = self.canvas.create_rectangle(x_position - 10, y_position - 5, x_position + 10,
                                                            y_position + 5, fill=self.line_colour)
            else:
                self.canvas.coords(self.bus_gui, x_position - 10, y_position - 5, x_position + 10, y_position + 5)
                self.canvas.pack()
