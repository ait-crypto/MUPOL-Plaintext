import copy


class Problem:
    def __init__(self, map):
        self.map = map
        self.orders = []
        self.trucks = []
        self.freighters = []

    def __str__(self):
        freighters_info = " ".join(str(freighter) for freighter in self.freighters)
        orders_info = " ".join(str(order) for order in self.orders)
        return f"Freighters: {freighters_info} Orders: {orders_info}"

    def clone(self):
        # Deep copy this Problem instance to ensure complete separation of data
        return copy.deepcopy(self)
