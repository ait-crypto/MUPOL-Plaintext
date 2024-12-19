class TruckDrive:
    def __init__(self, truck, origin, destination, start, end):
        self.truck = truck
        self.origin = origin
        self.destination = destination
        self.start = start
        self.end = end
        self.orders = []

    def get_empty_space(self):
        total = sum(order.volume for order in self.orders)
        return self.truck.capacity - total

    def __str__(self):
        empty_space = self.get_empty_space()
        return f"truck: {self.truck.id} origin: {self.origin} destination: \
        {self.destination} emptySpace: {empty_space} startTime: {self.start} \
        endTime: {self.end}"
