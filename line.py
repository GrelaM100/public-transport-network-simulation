class Line:
    def __init__(self, name, color, stops=None):
        self.name = name
        self.color = color
        if stops is None:
            self.stops = []
        else:
            self.stops = stops

    def __iter__(self):
        self.current_stop = self.stops[0]
        return self

    def __next__(self):
        idx = self.stops.index(self.current_stop) + 1
        if idx == len(self.stops):
            raise StopIteration

        self.current_stop = self.stops[idx]
        return self.current_stop

    def get_next_stop(self, current_stop):
        current_stop_index = self.stops.index(current_stop)
        if current_stop_index == len(self.stops) - 1:
            next_stop = None
        else:
            next_stop = self.stops[current_stop_index + 1]

        return next_stop
