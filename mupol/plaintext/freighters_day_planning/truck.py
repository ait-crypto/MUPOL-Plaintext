class Truck:
    next_id = 0

    def __init__(self, freighter, capacity, position):
        self.id = Truck.next_id
        Truck.next_id += 1
        self.freighter = freighter
        self.capacity = capacity
        self.position = position
        self.availabilities = list(range(64))
        self.next_availability = 0

    @staticmethod
    def slot2time(slot):
        hour = 6 + slot // 4
        minutes = (slot % 4) * 15
        str_time = f"{hour:02}:{minutes:02}-"

        hour = 6 + (slot + 1) // 4
        minutes = ((slot + 1) % 4) * 15
        str_time += f"{hour:02}:{minutes:02}"

        return str_time
