import simpy
import random
from tkinter import *
from network import Network
import threading
import time


def get_params_for_sim():
    bus_size = int(input("Ile miejsc ma być w autobusach?"))
    bus_frequency = int(input("Co ile czasu mają jeździć autobusy?"))
    return [bus_size, bus_frequency]


class MainWindow:
    def __init__(self, main_window):
        self.network = None
        self.window = main_window
        self.canvas = Canvas(self.window, width=200, height=200)
        self.canvas.pack(fill='both', expand=True)
        self.entry_bus_size = Entry(self.window)
        self.entry_bus_size.insert(END, '22')
        self.entry_bus_frequency = Entry(self.window)
        self.entry_bus_frequency.insert(END, '4')
        self.canvas.create_text(85, 20, text='Bus size')
        self.canvas.create_window(85, 40, window=self.entry_bus_size)
        self.canvas.create_text(85, 60, text='Bus frequency')
        self.canvas.create_window(85, 80, window=self.entry_bus_frequency)
        self.start_button = Button(text='Start', command=lambda: threading.Thread(target=self.start_simulation).start())
        self.canvas.create_window(130, 110, window=self.start_button)

    def start_simulation(self):
        self.initial_drawing()
        self.main(self.network)

    def initial_drawing(self):
        self.canvas.destroy()
        width = 1024
        height = 1024
        self.canvas = Canvas(self.window, width=width, height=height, bg='black')
        self.canvas.pack(fill='both', expand=True)
        env = simpy.Environment()
        self.network = Network(env, int(self.entry_bus_size.get()), int(self.entry_bus_frequency.get()), self.canvas)
        self.network.setup()
        self.network.draw_network()

    def main(self, network):
        network.env.process(self.run_simulation(network.env, network.bus_size, network.bus_frequency))
        network.env.run()

    def run_simulation(self, env, bus_size, bus_frequency, line_colour="Zielona"):
        time_passed = 0

        while True:
            self.network.run_lines()
            time.sleep(1)
            yield env.timeout(1)
            time_passed += 1
            if time_passed % bus_frequency == 0:
                self.network.drive_from_depot()
            self.network.passengers_arriving()


if __name__ == "__main__":
    root = Tk()
    MainWindow(root)
    root.mainloop()
