import copy
import random

from mupol.plaintext.freighters_day_planning.freighter import Freighter
from mupol.plaintext.freighters_day_planning.map import Map
from mupol.plaintext.freighters_day_planning.order import Order
from mupol.plaintext.freighters_day_planning.problem import Problem


class RandomProblemGenerator:
    def __init__(
        self,
        num_freighters,
        min_num_trucks,
        max_num_trucks,
        truck_capacity,
        num_orders,
        min_order_volume,
        max_order_volume,
        random_seed=None,
    ):
        self.num_freighters = num_freighters
        self.min_num_trucks = min_num_trucks
        self.max_num_trucks = max_num_trucks
        self.truck_capacity = truck_capacity
        self.num_orders = num_orders
        self.min_order_volume = min_order_volume
        self.max_order_volume = max_order_volume
        self.random_seed = random_seed

    def get_problem(self):
        map = Map()

        map.add_route(1, 2, 6)
        map.add_route(1, 3, 14)
        map.add_route(1, 4, 11)
        map.add_route(2, 1, 6)
        map.add_route(2, 3, 10)
        map.add_route(2, 4, 12)
        map.add_route(3, 1, 14)
        map.add_route(3, 2, 10)
        map.add_route(3, 4, 13)
        map.add_route(4, 1, 11)
        map.add_route(4, 2, 12)
        map.add_route(4, 3, 13)

        problem = Problem(map)
        positions = map.get_positions()
        origins = map.get_origins()

        destinations = map.get_destinations()

        rng = random.Random(self.random_seed)

        for _ in range(self.num_freighters):
            freighter = Freighter()
            num_trucks = rng.randint(self.min_num_trucks, self.max_num_trucks)

            for _ in range(num_trucks):
                pos_index = rng.randint(0, len(positions) - 1)
                problem.trucks.append(
                    freighter.create_truck(self.truck_capacity, positions[pos_index])
                )

            problem.freighters.append(freighter)

        for i in range(self.num_orders):
            origin_index = rng.randint(0, len(origins) - 1)
            destination_index = rng.randint(0, len(destinations) - 1)

            while destination_index == origin_index:
                destination_index = rng.randint(0, len(destinations) - 1)

            priority = rng.randint(1, 3)

            volume = self.min_order_volume + rng.randint(
                0, self.max_order_volume - self.min_order_volume
            )
            problem.orders.append(
                Order(
                    origins[origin_index],
                    destinations[destination_index],
                    volume,
                    priority,
                )
            )

        return problem

    def get_clone(self, problem):

        # print(copy.deepcopy(problem))
        return copy.deepcopy(problem)
