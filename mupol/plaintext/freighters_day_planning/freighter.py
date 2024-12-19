from mupol.plaintext.freighters_day_planning.truck import Truck


class Freighter:
    next_id = 0

    def __init__(self, name=None):
        self.id = Freighter.next_id
        Freighter.next_id += 1
        self.name = name if name is not None else f"freighter{self.id}"
        self.trucks = []

    def create_truck(self, capacity, position):
        truck = Truck(self, capacity, position)
        self.trucks.append(truck)
        return truck

    def __str__(self):
        trucks_info = ", ".join(
            f"{truck.id} ({truck.capacity} position: {truck.position})"
            for truck in self.trucks
        )
        return f"{self.name}; trucks [{trucks_info}]"
