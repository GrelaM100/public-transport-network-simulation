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
            data = {"Bus load": sum(self.buses_load) / (self.bus_size * len(self.buses_load)),
                    "Commuting time": 0,
                    "Traffic delays": self.buses_in_traffic}

        if self.statistics_table is None:
            self.statistics_table = pd.DataFrame(data=data, index=[time])

        else:
            self.statistics_table = pd.concat([self.statistics_table, pd.DataFrame(data=data, index=[time])])

    def save_data_to_csv(self):
        self.statistics_table.to_csv('statistics.csv')

    def plot_data(self, canvas, ax, indicator='Bus load'):
        ax.clear()
        ax.plot(self.statistics_table.index, self.statistics_table[indicator])
        canvas.draw()
        canvas.get_tk_widget().pack()

    def change_title_and_plot(self, window, canvas, ax, indicator):
        window.title(indicator)
        self.plot_data(canvas, ax, indicator)

    def window_plot_data(self, root):
        new_window = Toplevel(root)
        new_window.title('Bus load')
        fig = plt.Figure(figsize=(10, 8), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        frame = Frame(new_window, bg='white')
        frame.pack(side=RIGHT, expand=True, fill=BOTH)
        bus_load_button = Button(frame, text='Bus load',
                                 command=lambda: self.change_title_and_plot(new_window, canvas, ax, 'Bus load'))
        commute_times = Button(frame, text='Commute times',
                               command=lambda: self.change_title_and_plot(new_window, canvas, ax, 'Commuting time'))
        buses_in_traffic_button = Button(frame, text='Traffic delays',
                                         command=lambda: self.change_title_and_plot(new_window, canvas, ax, 'Traffic delays'))
        bus_load_button.pack(side=TOP)
        commute_times.pack(side=TOP)
        buses_in_traffic_button.pack(side=TOP)
        self.plot_data(canvas, ax)
