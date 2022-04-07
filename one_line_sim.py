import simpy
import random
from tkinter import *
from network import Network


def get_params_for_sim():
    bus_size = int(input("Ile miejsc ma być w autobusach?"))
    bus_frequency = int(input("Co ile czasu mają jeździć autobusy?"))
    return [bus_size, bus_frequency]


class MainWindow:
    def __init__(self, main_window):
        self.network = None
        self.window = main_window
        self.canvas = Canvas(self.window, width=200, height=200)
        self.canvas.pack()
        self.entry_bus_size = Entry(self.window)
        self.entry_bus_frequency = Entry(self.window)
        self.canvas.create_window(70, 20, window=self.entry_bus_size)
        self.canvas.create_window(70, 40, window=self.entry_bus_frequency)
        self.start_button = Button(text='Start', command=self.start_simulation)
        self.canvas.create_window(110, 70, window=self.start_button)

    def start_simulation(self):
        bus_size = int(self.entry_bus_size.get())
        bus_frequency = int(self.entry_bus_frequency.get())
        self.main(bus_size, bus_frequency)
        self.initial_drawing()

    def initial_drawing(self):
        self.canvas.destroy()
        width = 1024
        height = 1024
        self.canvas = Canvas(self.window, width=width, height=height, bg='black')
        self.canvas.pack()
        x_start = 20
        y_start = 20
        x_end = 200
        y_end = 200
        lines = []

        for stops in self.network.lines_stops['Zielona']:
            self.canvas.create_text(x_start, y_start, fill='red', text=stops)
            lines.append((x_start, y_start, x_end, y_end))
            x_start = x_end
            y_start = y_end
            x_end = x_start + 200 + random.randint(0, 50)
            y_end = y_start + 200 + random.randint(0, 50)


        lines = lines[:-1]
        for line in lines:
            self.canvas.create_line(line[0], line[1], line[2], line[3], fill='green')


    def main(self, bus_size, bus_frequency):
        # random.seed(15)
        env = simpy.Environment()
        # sim_params = get_params_for_sim()
        env.process(self.run_simulation(env, bus_size, bus_frequency))
        env.run(until=10)

    def run_simulation(self, env, bus_size, bus_frequency, line_colour="Zielona"):
        self.network = Network(env, bus_size, bus_frequency)
        self.network.setup()
        time_passed = 0

        while True:
            self.network.run_lines()
            yield env.timeout(1)
            time_passed += 1
            if time_passed % bus_frequency == 0:
                self.network.drive_from_depot()
            self.network.passengers_arriving()


if __name__ == "__main__":
    root = Tk()
    MainWindow(root)
    root.mainloop()
