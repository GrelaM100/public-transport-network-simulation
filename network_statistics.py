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

    def plot_data(self, root):
        new_window = Toplevel(root)
        new_window.title('Bus load')
        fig = plt.Figure(figsize=(10, 8), dpi=100)
        fig.add_subplot(111).plot(self.statistics_table.index, self.statistics_table['Bus load'])
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
