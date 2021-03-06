import random
import math
from passenger import Passenger
from bus import Bus
from stop import Stop
from line import Line
from network_statistics import Statistics
import networkx as nx
import json


class Network:
    def __init__(self, env, bus_size, bus_frequency, traffic_rate, canvas):
        self.env = env
        self.bus_size = bus_size
        self.bus_frequency = bus_frequency
        if traffic_rate == "small":
            self.traffic_rate = 0.3
        elif traffic_rate == "heavy":
            self.traffic_rate = 3
        else:
            self.traffic_rate = 1.2
        self.lines_stops = {}
        self.all_stops = []
        self.passengers_at_stops = []
        self.buses = []
        self.canvas = canvas
        self.graph = None
        self.traffic_jams = []
        self.statistics = None
        self.time_passed = 0

    def setup(self, lines=None):
        self.initialize_network(lines)
        self.graph = self.create_graph()
        self.drive_from_depot()
        self.passengers_arriving()
        self.statistics = Statistics(self.bus_size)

    def passengers_arriving(self):
        self.time_passed += 1
        no_of_passengers = random.randint(math.floor(self.traffic_rate * len(self.all_stops)) - 3,
                                          math.floor(self.traffic_rate * len(self.all_stops)) + 3)
        for i in range(no_of_passengers):
            rand_start = random.sample(self.all_stops, 1)
            rand_destination = random.sample(self.all_stops, 1)
            while rand_start == rand_destination:
                rand_destination = random.sample(self.all_stops, 1)
            itinerary = nx.shortest_path(self.graph, rand_start[0], rand_destination[0])
            new_passenger = Passenger(self.env, rand_start[0], rand_destination[0], itinerary)
            self.passengers_at_stops.append(new_passenger)
            rand_start[0].add_passenger(new_passenger)

    def drive_from_depot(self):
        for name, line in self.lines_stops.items():
            if (self.time_passed + line.start_time) % self.bus_frequency == 0:
                bus1 = Bus(self.env, name, line.color, line.stops, self.bus_size)
                bus2 = Bus(self.env, name, line.color, line.stops, self.bus_size, "other_way")
                self.buses.append(bus1)
                self.buses.append(bus2)
                bus1.visualize_bus_at_stop(bus1.future_stops[0], self.canvas)
                bus2.visualize_bus_at_stop(bus2.future_stops[0], self.canvas)

    def run_lines(self):
        buses_ending_route = []
        self.visualize_passengers_at_stops()
        for bus in self.buses:
            if bus.future_stops[0] in self.traffic_jams:
                for passenger in bus.passengers:
                    passenger.time_commuting += 1
                self.statistics.register_data("jam", 1)
                self.statistics.register_data("bus", len(bus.passengers))
            else:
                hopped_off = bus.drop_passengers_off()
                hopped_overcrowded = bus.take_passengers(self.passengers_at_stops)
                if "overcrowded" in hopped_overcrowded:
                    self.statistics.register_data("crowd", 1)
                    hopped_on = list(filter(lambda a: a != "overcrowded", hopped_overcrowded))
                else:
                    hopped_on = hopped_overcrowded
                current_stop, end_of_line = bus.drive_from_stop()
                for passenger in hopped_off:
                    if passenger.end_journey() is not None:
                        self.statistics.register_data("pas", passenger.end_journey())
                    else:
                        self.passengers_at_stops.append(passenger)
                for passenger in hopped_on:
                    self.passengers_at_stops.remove(passenger)
                if end_of_line:
                    buses_ending_route.append(bus)
                else:
                    self.statistics.register_data("bus", len(bus.passengers))

        for passenger in self.passengers_at_stops:
            passenger.time_commuting += 1
        for bus in buses_ending_route:
            self.buses.remove(bus)

    def initialize_network(self, lines=None):
        if lines is None:
            green_line_stops = [Stop("Trawa", 50, 50), Stop("??wiat??o", 240, 240), Stop("Jab??ko", 460, 460),
                                Stop("Poj??cie", 600, 600), Stop("??aba", 750, 750)]
            green_line = Line('Zielona', 'green', self.bus_frequency)
            yellow_line = Line('??????ta', 'yellow', self.bus_frequency)
            yellow_line_stops = [Stop("Piasek", 50, 600), Stop("S??o??ce", 100, 400), Stop("??wiat??o", 240, 240),
                                 Stop("Z??by", 420, 220), Stop("??????tko", 620, 100), Stop("Banan", 850, 80)]
            self.add_line_to_network(green_line, green_line_stops)
            self.add_line_to_network(yellow_line, yellow_line_stops)
        else:
            for line in lines:
                self.add_line_to_network(Line(line.name, line.color, self.bus_frequency), line.stops)

    def add_line_to_network(self, line, stops):
        if line.name not in self.lines_stops:
            self.lines_stops[line.name] = line
            for stop in stops:
                stop_to_add = self.get_stop_by_name(stop.name)
                if stop_to_add is None:
                    stop_to_add = stop
                    self.all_stops.append(stop_to_add)
                line.add_stop_to_line(stop_to_add)

    def get_stop_by_name(self, name):
        for stop in self.all_stops:
            if stop.name == name:
                return stop
        return None

    def draw_network(self):
        for line in self.lines_stops.values():
            for stop in line.stops:
                self.canvas.create_text(stop.x_position, stop.y_position, fill='red', text=stop)
                next_stop = line.get_next_stop(stop)
                if next_stop is not None:
                    self.canvas.create_line(stop.x_position, stop.y_position, next_stop.x_position,
                                            next_stop.y_position, fill=line.color)

    def visualize_passengers_at_stops(self):
        for stop in self.all_stops:
            if stop.stop_gui is None:
                stop.stop_gui = self.canvas.create_text(stop.x_position, stop.y_position - 20,
                                                        text=str(len(stop.passengers_at_stop)), fill='red', font='20')
            else:
                self.canvas.itemconfig(stop.stop_gui, text=str(len(stop.passengers_at_stop)))

    def create_graph(self):
        graph = nx.Graph()
        graph.add_nodes_from(self.all_stops)
        for line in self.lines_stops.values():
            connected_stops = []
            for i in range(len(line.stops)):
                if i != len(line.stops) - 1:
                    connected_stops.append((line.stops[i], line.stops[i + 1]))
                if i != 0:
                    connected_stops.append((line.stops[i - 1], line.stops[i]))
            graph.add_edges_from(connected_stops)
        return graph

    def create_traffic_jams(self):
        no_of_jams = random.randint(0, 2)
        self.traffic_jams = random.sample(self.all_stops, no_of_jams)

    def get_configuration(self):
        configuration = []
        for line in self.lines_stops.values():
            configuration.append(line.get_identifiers())
        return configuration

    def save_configuration(self, filename):
        json_string = json.dumps(self.get_configuration())
        with open(filename, "w") as json_file:
            json_file.write(json_string)