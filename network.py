import functools
import operator
import random
from passenger import Passenger
from bus import Bus
from stop import Stop
from line import Line


class Network:
    # docelowo będzie można podawać własne nazwy linii
    def __init__(self, env, bus_size, bus_frequency, canvas):
        self.env = env
        self.bus_size = bus_size
        self.bus_frequency = bus_frequency
        self.lines_stops = None
        self.passengers_at_stops = []
        self.buses = []
        self.canvas = canvas

    def setup(self, lines=None):
        self.initialize_network(lines)
        self.drive_from_depot()
        self.passengers_arriving()

    def passengers_arriving(self):
        all_stops = list(set(functools.reduce(operator.iconcat, self.lines_stops.values(), [])))
        print(all_stops)

        no_of_passengers = random.randint(4, 7)
        for i in range(no_of_passengers):
            rand_start = random.sample(all_stops, 1)
            rand_destination = random.sample(all_stops, 1)
            while rand_start == rand_destination:
                rand_destination = random.sample(all_stops, 1)
            new_passenger = Passenger(self.env, rand_start[0], rand_destination[0])
            self.passengers_at_stops.append(new_passenger)
            print(str(new_passenger) + " przyszedł na przystanek")

    def drive_from_depot(self):
        for name, line in self.lines_stops.items():
            bus1 = Bus(self.env, name, line.color, line.stops, self.bus_size)
            bus2 = Bus(self.env, name, line.color, line.stops, self.bus_size, "other_way")
            self.buses.append(bus1)
            self.buses.append(bus2)
            print(str(bus1) + " wyjechał z zajezdni")
            bus1.visualize_bus_at_stop(bus1.future_stops[0], self.canvas)
            print(str(bus2) + " wyjechał z zajezdni")
            bus2.visualize_bus_at_stop(bus2.future_stops[0], self.canvas)

    def run_lines(self):
        buses_ending_route = []
        for bus in self.buses:
            hopped_off = bus.drop_passengers_off()
            hopped_on = bus.take_passengers(self.passengers_at_stops)
            current_stop, end_of_line = bus.drive_from_stop()
            print("Przystanek: ", current_stop)
            print("Wysiedli: ")
            for passenger in hopped_off:
                self.passengers_at_stops.append(passenger)
                print(str(passenger))
            print("Wsiedli: ")
            for passenger in hopped_on:
                self.passengers_at_stops.remove(passenger)
                print(str(passenger))
            if end_of_line:
                buses_ending_route.append(bus)
            print("\n")

        for bus in buses_ending_route:
            self.buses.remove(bus)
            print(str(bus))

    def initialize_network(self, lines=None):
        green_line = Line('Zielona', 'green',
                          [Stop("Trawa", 20, 20), Stop("Światło", 240, 240), Stop("Jabłko", 460, 460),
                           Stop("Pojęcie", 680, 680), Stop("Żaba", 900, 900)])
        yellow_line = Line('Żółta', 'yellow', [Stop("Piasek", 20, 1000), Stop("Słońce", 220, 820), Stop("Światło", 240, 240),
                                               Stop("Zęby", 420, 220),
                                               Stop("Żółtko", 620, 100),
                                               Stop("Banan", 1000, 20)])

        default_network_lines = {green_line.name: green_line, yellow_line.name: yellow_line}

        if lines is None:
            lines = default_network_lines

        self.lines_stops = lines

    def draw_network(self):
        for line in self.lines_stops.values():
            for stop in line.stops:
                self.canvas.create_text(stop.x_position, stop.y_position, fill='red', text=stop)
                next_stop = line.get_next_stop(stop)
                if next_stop is not None:
                    self.canvas.create_line(stop.x_position, stop.y_position, next_stop.x_position, next_stop.y_position,
                                            fill=line.color)
