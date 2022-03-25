import random
import simpy
import pygame

global lines


class BusStop:
    def __init__(self, name):
        self.name = name
        self.passengers = []

    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)

    def get_name(self):
        return self.name


lines = {"Zielona": [BusStop("Trawa"), BusStop("Światło"), BusStop("Jabłko"), BusStop("Pojęcie"), BusStop("Żaba")],
         "Żółta": ["Piasek", "Słońce", "Zęby", "Żółtko", "Światło", "Banan"]}


class Passenger:
    def __init__(self, env, starting_stop, destination_stop):
        self.env = env
        self.current_stop = starting_stop
        self.destination_stop = destination_stop

    def __str__(self):
        return 'Pasażer jadący do ' + str(self.destination_stop.get_name()) + ' obecnie w ' + str(self.current_stop.get_name())


class Bus:
    def __init__(self, env, line_colour, future_stops):
        self.env = env
        self.line_colour = line_colour
        self.future_stops = future_stops.copy()
        self.passengers = []

    def __str__(self):
        return "Autobus linii " + self.line_colour + " na przystanku " + self.future_stops[0].get_name()

    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)


class Line:
    def __init__(self, env, line_colour, bus_size, bus_frequency, passengers):
        self.env = env
        self.line_colour = line_colour
        global lines
        self.stops = lines[self.line_colour]
        self.bus_size = bus_size
        self.bus_frequency = bus_frequency
        self.buses = []
        self.passengers_at_stops = passengers

    def passengers_arriving(self):
        no_of_passengers = random.randint(1, 6)
        for i in range(no_of_passengers):
            rand_start = random.sample(self.stops, 1)
            rand_destination = random.sample(self.stops, 1)
            while rand_start == rand_destination:
                rand_destination = random.sample(self.stops, 1)
            new_passenger = Passenger(self.env, rand_start[0], rand_destination[0])
            self.passengers_at_stops.append(new_passenger)
            rand_start[0].add_passenger(new_passenger)
            print(str(new_passenger) + " przyszedł na przystanek")

    def drive_from_depot(self):
        self.buses.append(Bus(self.env, self.line_colour, self.stops))
        print(str(Bus(self.env, self.line_colour, self.stops)) + " wyjechał na linię")

    def arrive_at_stop(self, bus):
        current_stop = bus.future_stops.pop(0)
        print("Przystanek: ", current_stop.get_name())
        print("Wysiedli: ")
        hopped_off = []
        for passenger_in_bus in bus.passengers:
            if passenger_in_bus.destination_stop == current_stop:
                passenger_in_bus.current_stop = current_stop
                print(str(passenger_in_bus))
        for passenger in hopped_off:
            bus.remove_passenger(passenger)
            current_stop.add_passenger(passenger)
        print("Wsiedli: ")
        hopped_on = []
        for passenger_at_stop in self.passengers_at_stops:
            if passenger_at_stop.current_stop == current_stop and \
                    passenger_at_stop.destination_stop in bus.future_stops and \
                    len(bus.passengers) < self.bus_size:
                passenger_at_stop.current_stop = current_stop
                bus.passengers.append(passenger_at_stop)
                hopped_on.append(passenger_at_stop)
                print(str(passenger_at_stop))
        for passenger in hopped_on:
            self.passengers_at_stops.remove(passenger)
            current_stop.remove_passenger(passenger)
        if len(bus.future_stops) == 0:
            self.buses.remove(bus)
        print("\n")


def run_line(env, bus_size, bus_frequency, line_colour="Zielona"):
    passenger_at_every_stop = [Passenger(env, "Trawa", "Jabłko"), Passenger(env, "Światło", "Pojęcie"),
                               Passenger(env, "Jabłko", "Żaba"), Passenger(env, "Pojęcie", "Żaba")]
    line = Line(env, line_colour, bus_size, bus_frequency, passenger_at_every_stop)
    line.drive_from_depot()
    time_passed = 0

    while True:
        line.passengers_arriving()
        for bus in line.buses:
            line.arrive_at_stop(bus)
        yield env.timeout(1)
        time_passed += 1
        if time_passed % line.bus_frequency == 0:
            line.drive_from_depot()


def get_params_for_sim():
    bus_frequency = int(input("Co ile czasu mają jeździć autobusy?"))
    bus_size = int(input("Ile miejsc ma być w autobusach?"))
    return [bus_size, bus_frequency]


def main():
    random.seed(15)
    env = simpy.Environment()
    sim_params = get_params_for_sim()
    env.process(run_line(env, sim_params[0], sim_params[1]))
    env.run(until=10)


if __name__ == "__main__":
    main()
