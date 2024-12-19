import json
import os
import time

import pandas as pd
from tqdm import tqdm

from mupol.plaintext.freighters_day_planning.freighter import Freighter
from mupol.plaintext.freighters_day_planning.map import Map
from mupol.plaintext.freighters_day_planning.order import Order
from mupol.plaintext.freighters_day_planning.problem import Problem
from mupol.plaintext.freighters_day_planning.simple_solver import SimpleSolver
from mupol.plaintext.freighters_day_planning.truck import Truck


def load_instance(file_path):
    # Load JSON data from file
    with open(file_path, "r") as file:
        data = json.load(file)

    # Create a new Problem instance
    map = Map()
    problem = Problem(map)

    # Assuming map routes are directly loadable or need some conversion
    for route in data["map"]:
        problem.map.add_route(route["origin"], route["destination"], route["distance"])

    # Reconstruct trucks and assign to freighters
    freighters_dict = {}
    for truck_data in data["trucks"]:
        if truck_data["freighter"] not in freighters_dict:
            freighter = Freighter()
            freighters_dict[truck_data["freighter"]] = freighter
            problem.freighters.append(freighter)
        else:
            freighter = freighters_dict[truck_data["freighter"]]

        truck = Truck(freighter, truck_data["capacity"], truck_data["position"])
        truck.id = truck_data["truckId"]  # Assuming the truck ID needs to be preserved
        problem.trucks.append(truck)

    # Reconstruct orders
    for order_data in data["orders"]:
        order = Order(
            order_data["origin"],
            order_data["destination"],
            order_data["volume"],
            order_data["priority"],
        )  # , order_data['priority']
        order.id = order_data["orderId"]  # Assuming the order ID needs to be preserved
        problem.orders.append(order)

    return data["instance_id"], problem


def run_optimizer_and_record(
    instance_id,
    problem,
    num_iterations,
    num_orders,
    num_feighters,
    num_trucks,
    total_order_volume,
):
    solver = SimpleSolver()

    # Warm up the solver to reduce variability from initial overhead
    solver.optimize(problem.clone(), 1)

    start_time = time.perf_counter()
    solver.optimize(problem, num_iterations)
    end_time = time.perf_counter()

    average_empty = solver.get_average_empty()
    runtime = end_time - start_time

    empty_drives = solver.get_total_empty_drives()

    total_drives = solver.get_total_drives()

    total_empty = solver.get_total_empty()

    total_empty_times_km = solver.get_total_empty_times_km(solver.get_best_solution())

    total_empty_per_km = solver.get_total_empty_per_km(solver.get_best_solution())

    total_km = solver.get_total_km(solver.get_best_solution())

    number_of_bubble_swaps = solver.get_swaps(solver.get_best_solution())

    number_of_max_swaps = solver.get_swaps_max(solver.get_best_solution())

    get_swap_norm = solver.get_swap_norm(solver.get_best_solution())
    get_empty_km_norm = solver.get_empty_km_norm(solver.get_best_solution())

    opt_value = solver.get_best_opt()

    return {
        "instance_id": instance_id,
        "num_iterations": num_iterations,
        "average_empty": average_empty,
        "runtime": runtime,
        "num_orders": num_orders,
        "num_trucks": num_trucks,
        "num_feighters": num_feighters,
        "total_order_volume": total_order_volume,
        "total_drives": total_drives,
        "empty_drives": empty_drives,
        "times_empty_km": total_empty_times_km,
        "divide_empty_km": total_empty_per_km,
        "total_empty": total_empty,
        "total_km": total_km,
        "priority_bubble_swaps": number_of_bubble_swaps,
        "max_priority_blubble_swaps": number_of_max_swaps,
        "swap_norm": get_swap_norm,
        "empty_km_norm": get_empty_km_norm,
        "opt_value ": opt_value,
    }


def export_results_to_csv_and_excel(results):
    df = pd.DataFrame(results)
    csv_filename = "optimization_results1.csv"
    excel_filename = "optimization_results1.xlsx"

    df.to_csv(csv_filename, index=False)
    df.to_excel(excel_filename, index=False)

    print(f"Results have been saved to '{csv_filename}' and '{excel_filename}'.")


def main():

    directory_path = "priority_jsons"
    results = []

    # Loop through each file in the directory and solve it
    with tqdm(
        total=225, desc="Processing files"
    ) as pbar:  # update total by num_jsons * len([num_iterations])
        for filename in os.listdir(directory_path):
            if filename.endswith(".json"):
                file_path = os.path.join(directory_path, filename)
                instance_id, problem = load_instance(
                    os.path.join(directory_path, filename)
                )
                with open(file_path, "r") as file:
                    data = json.load(file)
                    num_orders = len(data["orders"])
                    num_trucks = len(data["trucks"])

                    freighter_ids = [truck["freighter"] for truck in data["trucks"]]
                    unique_freighters = set(freighter_ids)

                    num_feighters = len(unique_freighters)

                    total_order_volume = sum(
                        order["volume"] for order in data["orders"]
                    )

                for num_iterations in [1]:  # chane num iterations here
                    result = run_optimizer_and_record(
                        instance_id,
                        problem,
                        num_iterations,
                        num_orders,
                        num_feighters,
                        num_trucks,
                        total_order_volume,
                    )
                    results.append(result)
                    pbar.update(1)

    # Export the results to CSV and Excel files
    export_results_to_csv_and_excel(results)

    print("10000 it Results have been saved to 'optimization_results.csv'.")


main()
