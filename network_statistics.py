import numpy as np

class Statistics:
    def __init__(self, bus_size):
        self.bus_size = bus_size
        self.buses_load = []
        self.commute_times = []
        self.buses_in_traffic = 0

    def register_data(self, type, data):
        if type == "bus":
            self.buses_load.append(data)
        elif type == "pas":
            self.commute_times.append(data)
        elif type == "jam":
            self.buses_in_traffic += data

    def return_statistics(self):
        return [{"Bus load" : sum(self.buses_load) / (self.bus_size * len(self.buses_load)),
                 "Commuting time" :  sum(self.commute_times)  / len(self.commute_times),
                 "Traffic delays" : self.buses_in_traffic}]