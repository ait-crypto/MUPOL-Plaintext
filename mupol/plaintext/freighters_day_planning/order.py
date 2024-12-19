class Order:
    next_id = 0

    def __init__(self, origin, destination, volume, priority=None, freighter=None):
        self.id = Order.next_id
        Order.next_id += 1
        self.volume = volume
        self.origin = origin
        self.destination = destination
        self.freighter = freighter
        self.priority = priority

    def __str__(self):
        return f"order{self.id} ({self.volume}) {self.origin}->{self.destination} \
            {self.priority}"

    def __repr__(self):
        return self.__str__()

    def get_size(self):
        return self.volume
