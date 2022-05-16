class Passenger:
    def __init__(self, env, starting_stop, destination_stop, itinerary):
        self.env = env
        self.current_stop = starting_stop
        self.destination_stop = destination_stop
        self.itinerary = itinerary
        self.itinerary.remove(self.current_stop)
        self.time_commuting = 0

    def __str__(self):
        return 'Pasażer jadący do ' + str(self.destination_stop) + ' przez ' + str(self.itinerary) \
               + ' obecnie w ' + str(self.current_stop)

    def decide_to_hop_off(self, current_stop, next_stop):
        if current_stop == self.destination_stop or next_stop not in self.itinerary:
            return True
        return False

    def decide_to_hop_on(self, next_stop):
        if next_stop in self.itinerary:
            return True
        return False

    def at_stop(self, stop):
        self.itinerary.remove(stop)

    def end_journey(self):
        if len(self.itinerary) == 0:
            return self.time_commuting
        return None
