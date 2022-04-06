import simpy
import random
from network import Network


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
    # sim_params = get_params_for_sim()
    sim_params = [22, 4]
    env.process(run_simulation(env, sim_params[0], sim_params[1]))
    env.run(until=10)


if __name__ == "__main__":
    main()
