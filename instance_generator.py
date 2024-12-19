"""
Warning: this file does not provide the option to specify a folder for the generated
json files.
It is recommended to manually create a new folder (e.g. json_files, which will be
compatible with prio_json.py), cd to the folder and run this code from there.
"""

import itertools
import json

from mupol.plaintext.freighters_day_planning.freighter import Freighter
from mupol.plaintext.freighters_day_planning.order import Order
from mupol.plaintext.freighters_day_planning.random_problem_generator import (
    RandomProblemGenerator,
)
from mupol.plaintext.freighters_day_planning.truck import Truck


def generate_problem_json(
    instance_id,
    num_freighters,
    min_num_trucks,
    max_num_trucks,
    truck_capacity,
    num_orders,
    min_order_volume,
    max_order_volume,
):
    Truck.next_id = 0
    Order.next_id = 0
    Freighter.next_id = 0

    # Assuming 'generator_input' is a dictionary with necessary parameters
    generator = RandomProblemGenerator(
        num_freighters,
        min_num_trucks,
        max_num_trucks,
        truck_capacity,
        num_orders,
        min_order_volume,
        max_order_volume,
    )
    problem = generator.get_problem()

    # Creating JSON data structure
    problem_data = {
        "instance_id": instance_id,
        "trucks": [
            {
                "truckId": truck.id,
                "position": truck.position,
                "capacity": truck.capacity,
                "freighter": truck.freighter.id,
            }
            for truck in problem.trucks
        ],
        "map": [
            {"origin": key[0], "destination": key[1], "distance": value}
            for key, value in problem.map.routes.items()
        ],
        "orders": [
            {
                "orderId": order.id,
                "origin": order.origin,
                "destination": order.destination,
                "volume": order.volume,
            }
            for order in problem.orders
        ],
        "solution": None,  # Placeholder for solution
    }

    # Serialize to JSON
    json_filename = f"problem_instance_{instance_id}.json"
    with open(json_filename, "w") as f:
        json.dump(problem_data, f, indent=4)

    print(f"Problem instance saved to {json_filename}")
    return json_filename


num_freighters_options = [1, 2, 3, 4, 5]
num_orders_options = [50, 100, 500]
min_max_trucks_options = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
min_max_order_options = [(1, 10), (1, 20), (1, 32)]
truck_capacity = 32


# Generate all combinations

counter = 0
for combination in itertools.product(
    num_freighters_options,
    min_max_trucks_options,
    num_orders_options,
    min_max_order_options,
):
    counter += 1
    (
        num_freighters,
        (min_trucks, max_trucks),
        num_orders,
        (min_order_volume, max_order_volume),
    ) = combination
    instance_id = counter
    generate_problem_json(
        instance_id,
        num_freighters,
        min_trucks,
        max_trucks,
        truck_capacity,
        num_orders,
        min_order_volume,
        max_order_volume,
    )
