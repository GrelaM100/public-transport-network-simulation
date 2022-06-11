import pandas as pd
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Statistics:
    def __init__(self, bus_size):
        self.bus_size = bus_size
        self.buses_load = []
        self.commute_times = []
        self.buses_in_traffic = 0
        self.statistics_table = None
        self.ax = None
        self.canvas = None
        self.indicator = 'Bus load'

    def register_data(self, type, data):
        if type == "bus":
            self.buses_load.append(data)
        elif type == "pas":
            self.commute_times.append(data)
        elif type == "jam":
            self.buses_in_traffic += data

    def return_statistics(self):
        return [{"Bus load": sum(self.buses_load) / (self.bus_size * len(self.buses_load)),
                 "Commuting time": sum(self.commute_times) / len(self.commute_times),
                 "Traffic delays": self.buses_in_traffic}]

    def update_table(self, time):
        try:
            data = {"Bus load": sum(self.buses_load) / (self.bus_size * len(self.buses_load)),
                    "Commuting time": sum(self.commute_times) / len(self.commute_times),
                    "Traffic delays": self.buses_in_traffic}
        except ZeroDivisionError:
            data = {"Bus load": 0,
                    "Commuting time": 0,
                    "Traffic delays": self.buses_in_traffic}

        if self.statistics_table is None:
            self.statistics_table = pd.DataFrame(data=data, index=[time])

        else:
            self.statistics_table = pd.concat([self.statistics_table, pd.DataFrame(data=data, index=[time])])

    def save_data_to_csv(self):
        self.statistics_table.to_csv('statistics.csv')

    def plot_data(self, indicator='Bus load'):
        self.ax.clear()
        self.ax.plot(self.statistics_table.index, self.statistics_table[indicator])
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def change_title_and_plot(self, window, indicator):
        self.indicator = indicator
        window.title(self.indicator)
        self.plot_data(self.indicator)

    def safe_window_close(self, window):
        self.ax = None
        self.canvas = None
        window.destroy()

    def window_plot_data(self, root):
        new_window = Toplevel(root)
        new_window.title('Bus load')
        fig = plt.Figure(figsize=(10, 8), dpi=100)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=new_window)
        new_window.protocol("WM_DELETE_WINDOW", lambda: self.safe_window_close(new_window))
        frame = Frame(new_window, bg='white')
        frame.pack(side=RIGHT, expand=True, fill=BOTH)
        bus_load_button = Button(frame, text='Bus load',
                                 command=lambda: self.change_title_and_plot(new_window, 'Bus load'))
        commute_times = Button(frame, text='Commute times',
                               command=lambda: self.change_title_and_plot(new_window, 'Commuting time'))
        buses_in_traffic_button = Button(frame, text='Traffic delays',
                                         command=lambda: self.change_title_and_plot(new_window, 'Traffic delays'))
        bus_load_button.pack(side=TOP)
        commute_times.pack(side=TOP)
        buses_in_traffic_button.pack(side=TOP)
        self.plot_data()

    def update_plot(self):
        if self.ax is not None and self.canvas is not None:
            self.plot_data(self.indicator)
