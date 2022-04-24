class Passenger:
    def __init__(self, env, starting_stop, destination_stop):
        self.env = env
        self.current_stop = starting_stop
        self.destination_stop = destination_stop

    def __str__(self):
        return 'Pasażer jadący do ' + str(self.destination_stop) + ' obecnie w ' + str(self.current_stop)
