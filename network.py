import functools
import operator
import random
from passenger import Passenger
from bus import Bus

class Network:
    # docelowo będzie można podawać własne nazwy linii
    def __init__(self, env, bus_size, bus_frequency):
        self.env = env
        self.bus_size = bus_size
        self.bus_frequency = bus_frequency
        self.lines_stops = {"Zielona": ["Trawa", "Światło", "Jabłko", "Pojęcie", "Żaba"],
                            "Żółta": ["Piasek", "Słońce", "Zęby", "Żółtko", "Światło", "Banan"]}
        self.passengers_at_stops = []
        self.buses = []

    def setup(self):
        self.drive_from_depot()
        self.passengers_arriving()

    def passengers_arriving(self):
        all_stops = list(set(functools.reduce(operator.iconcat, self.lines_stops.values(), [])))
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
        for line, stops in self.lines_stops.items():
            self.buses.append(Bus(self.env, line, stops, self.bus_size))
            self.buses.append(Bus(self.env, line, stops, self.bus_size, "other_way"))
            print(str(Bus(self.env, line, stops, self.bus_size)) + " wyjechał z zajezdni")
            print(str(Bus(self.env, line, stops, self.bus_size, "other_way")) + " wyjechał z zajezdni")

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
