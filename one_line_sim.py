import simpy
import random
from tkinter import *
from network import Network
from stop import Stop
from line import Line
import threading
import time
from tkinter.colorchooser import askcolor


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
        self.start_button = Button(text='Start', command=self.initial_drawing)
        self.canvas.create_window(130, 110, window=self.start_button)
        self.lines = None
        self.chosen_line = None
        self.previous_stop = None
        self.all_stops = []

    def start_simulation(self):
        self.canvas.delete('all')
        env = simpy.Environment()
        self.network = Network(env, int(self.entry_bus_size.get()), int(self.entry_bus_frequency.get()), self.canvas)
        self.canvas.unbind('<Button 1>')
        self.network.setup(self.lines)
        self.network.draw_network()
        self.main(self.network)

    def initial_drawing(self):
        self.canvas.destroy()
        width = 1124
        height = 1024
        self.canvas = Canvas(self.window, width=width, height=height, bg='black')
        self.canvas.pack(fill='both', expand=True)
        side_bar = Canvas(self.canvas, width=100, height=1024, bg='grey')
        self.start_button = Button(text='Start', command=lambda: threading.Thread(target=self.start_simulation).start())
        add_line_button = Button(text='Add line', command=self.add_line)
        side_bar.create_window(50, 100, window=self.start_button)
        side_bar.create_window(50, 40, window=add_line_button)
        self.canvas.create_window(1130, 0, anchor=NE, window=side_bar)
        self.canvas.bind("<Button-1>", self.add_stop)

    def add_line(self):
        self.previous_stop = None
        line_name_entry = Entry(self.window)
        line_name_entry.bind('<Return>', lambda event: self.accept_line_name(event, line_name_entry))
        self.canvas.create_window(500, 500, window=line_name_entry)

    def accept_line_name(self, event, line_name_entry):
        line_name = line_name_entry.get()
        line_name_entry.destroy()
        color = askcolor(title='Line color')
        line = Line(line_name, color[1])
        if self.lines is None:
            self.lines = []
        self.lines.append(line)
        self.chosen_line = line

    def add_stop(self, event):
        if self.chosen_line is not None:
            x = event.x
            y = event.y
            stop_checker = self.get_stop_from_network(x, y)
            if stop_checker is None:
                bus_stop_entry = Entry(self.window)
                bus_stop_entry.bind('<Return>', lambda event: self.accept_name(event, bus_stop_entry, x, y))
                self.canvas.create_window(x, y, window=bus_stop_entry)
            else:
                self.accept_name(None, None, x, y, stop_checker)

    def accept_name(self, event, bus_stop_entry, x, y, stop_in_network=None):
        if stop_in_network is None:
            bus_stop_name = bus_stop_entry.get()
            bus_stop_entry.destroy()
            added_stop = Stop(bus_stop_name, x, y)
            self.canvas.create_text(x, y, fill='red', text=added_stop)
        else:
            added_stop = stop_in_network

        self.chosen_line.add_stop_to_line(added_stop)
        if self.previous_stop is not None:
            self.canvas.create_line(self.previous_stop.x_position, self.previous_stop.y_position, added_stop.x_position,
                                    added_stop.y_position, fill=self.chosen_line.color)

        self.previous_stop = added_stop
        if added_stop not in self.all_stops:
            self.all_stops.append(added_stop)

    def get_stop_from_network(self, x, y):
        for stop in self.all_stops:
            if x - 10 <= stop.x_position <= x + 10:
                if y - 10 <= stop.y_position <= y + 10:
                    return stop

        return None

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
