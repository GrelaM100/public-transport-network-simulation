import random
import simpy
import functools
import operator

class Network:
    # docelowo będzie można podawać własne nazwy linii
    def __init__(self, env, bus_size, bus_frequency):
        self.env = env
        self.bus_size = bus_size
        self.bus_frequency = bus_frequency
        self.lines_stops = {"Zielona" : ["Trawa", "Światło", "Jabłko", "Pojęcie", "Żaba"],
         "Żółta" : ["Piasek", "Słońce", "Zęby", "Żółtko", "Światło", "Banan"]}
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
            if end_of_line == True:
                buses_ending_route.append(bus)
            print("\n")

        for bus in buses_ending_route:
            self.buses.remove(bus)
            print(str(bus))

class Passenger:
    def __init__(self, env, starting_stop, destination_stop):
        self.env = env
        self.current_stop = starting_stop
        self.destination_stop = destination_stop

    def __str__(self):
        return  'Pasażer jadący do ' + str(self.destination_stop) + ' obecnie w ' + str(self.current_stop)

class Bus:
    def __init__(self, env, line_colour, future_stops, size, from_end_to_start = None):
        self.env = env
        self.line_colour = line_colour
        self.future_stops = future_stops.copy()
        self.passengers = []
        self.size = size
        if from_end_to_start != None:
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

def run_simulation(env, bus_size, bus_frequency, line_colour="Zielona"):
    network = Network(env, bus_size, bus_frequency)
    network.setup()
    time_passed = 0

    while True:
        network.run_lines()
        yield env.timeout(1)
        time_passed += 1
        if time_passed % bus_frequency == 0:
            network.drive_from_depot()
        network.passengers_arriving()

def get_params_for_sim():
    bus_size = int(input("Ile miejsc ma być w autobusach?"))
    bus_frequency = int(input("Co ile czasu mają jeździć autobusy?"))
    return [bus_size, bus_frequency]

def main():
    random.seed(15)
    env = simpy.Environment()
    #sim_params = get_params_for_sim()
    sim_params = [22, 4]
    env.process(run_simulation(env, sim_params[0], sim_params[1]))
    env.run(until=10)


if __name__ == "__main__":
    main()

