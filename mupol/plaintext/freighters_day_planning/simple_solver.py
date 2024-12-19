import copy
import random

from mupol.plaintext.freighters_day_planning.truck_drive import TruckDrive


class SimpleSolver:

    def __init__(self):
        self.solution = []
        self.best_value = 100
        self.best_solution = []

    def solve(self, problem):
        self.solution = []

        trucks = list(problem.trucks)
        orders = list(problem.orders)
        shuf_orders = []
        random.shuffle(trucks)

        priority_one_orders = []
        priority_two_orders = []
        priority_three_orders = []

        # Loop through each order in the list
        for order in orders:
            # Check if the order has priority 1
            if order.priority == 1:
                # Add the order to the priority one orders list
                priority_one_orders.append(order)
            elif order.priority == 2:
                # Add the order to the priority one orders list
                priority_two_orders.append(order)
            elif order.priority == 3:
                # Add the order to the priority one orders list
                priority_three_orders.append(order)

        random.shuffle(priority_one_orders)
        random.shuffle(priority_two_orders)
        random.shuffle(priority_three_orders)

        shuf_orders.extend(priority_one_orders)
        shuf_orders.extend(priority_two_orders)
        shuf_orders.extend(priority_three_orders)

        # print(shuf_orders[0])

        # random.shuffle(orders)

        while shuf_orders:

            drive = self.create_truck_drive(trucks, shuf_orders, problem.map)

            if not drive:

                drive = self.create_empty_truck_drive(trucks, shuf_orders, problem.map)
                # print("DRIVE", drive)

                self.solution.append(drive)
                drive.truck.next_availability = drive.end
                drive.truck.position = drive.destination

            if drive:

                self.fill_drive(drive, shuf_orders)

                if drive.orders:
                    self.solution.append(drive)
                    drive.truck.next_availability = drive.end
                    drive.truck.position = drive.destination

        if not self.solution:
            print("No solutions were added.")
            return 0

        swap_norm = self.get_swap_norm(self.solution)
        empty_km_norm = self.get_empty_km_norm(self.solution)

        alpha = 0.5

        weighted_sum = alpha * empty_km_norm + (1 - alpha) * swap_norm

        # objective_value = \
        #     sum(d.get_empty_space() for d in self.solution) / len(self.solution)
        # print("Objective value calculated:", objective_value)
        return weighted_sum

    def optimize(self, problem, num_it):

        random.seed(1234)
        self.best_value = float("inf")  # reset best value
        self.best_solution = []

        while num_it > 0:

            clone_prob = copy.deepcopy(problem)
            objective_value = self.solve(clone_prob)  # new ov

            if objective_value < self.best_value:
                self.best_value = objective_value
                self.best_solution = self.solution

            num_it -= 1

        # return self.best_value

    def create_truck_drive(self, trucks, orders, map):
        best_drive = None
        lowest_cost = float("inf")
        for truck in trucks:
            for order in orders:
                if truck.position != order.origin:
                    # Skip this truck-order pair if the truck is not at the order's
                    # origin
                    continue
                cost = map.get_costs(truck.position, order.destination)
                if cost != -1 and cost < lowest_cost:
                    # Found a more optimal drive
                    best_drive = TruckDrive(
                        truck,
                        truck.position,
                        order.destination,
                        truck.next_availability,
                        cost + truck.next_availability,
                    )
                    lowest_cost = cost
                    # print(f"Potential drive from {truck.position} to \
                    # {order.destination} with truck ID {truck.id} at cost {cost}")
        # if best_drive:
        # print(f"Selected optimal drive with truck ID {best_drive.truck.id} to \
        # {best_drive.destination}")
        return best_drive

    def fill_drive(self, drive, orders):
        remaining_orders = []
        for order in orders:
            if order.origin == drive.origin and order.destination == drive.destination:
                if drive.get_empty_space() >= order.volume:
                    drive.orders.append(order)
                else:
                    remaining_orders.append(order)
            else:
                remaining_orders.append(order)
        orders[:] = (
            remaining_orders  # Update the main orders list with remaining orders
        )

    def create_empty_truck_drive(self, trucks, orders, map):
        if not orders:
            # print("Exiting: No orders to process.")
            return None

        destination = orders[0].origin
        cheapest = float("inf")
        selected_truck = None

        # print("Destination for empty drive:", destination)
        for truck in trucks:
            cost = map.get_costs(truck.position, destination)
            # print(f"Checking truck at position {truck.position} to destination \
            # {destination}: cost = {cost}")

            if cost != -1 and cost < cheapest:
                cheapest = cost
                selected_truck = truck

        if not selected_truck:
            print(
                f"No truck found for empty drive to destination: {destination}, \
                cheapest found: {cheapest}"
            )
            return None

        return TruckDrive(
            selected_truck,
            selected_truck.position,
            destination,
            selected_truck.next_availability,
            cheapest + selected_truck.next_availability,
        )

    def get_best_solution(self):
        return self.best_solution

    def get_text_solution(self):
        result = "best_solution:\n"
        total_empty = 0.0

        for drive in self.best_solution:
            result += f"{drive}\n"
            total_empty += drive.get_empty_space()

        if self.best_solution:

            average_empty = total_empty / len(self.best_solution)
            result += f"avg. empty: {average_empty}"

        return result

    def get_average_empty(self):
        total_empty = 0.0

        for drive in self.best_solution:
            total_empty += drive.get_empty_space()

        if self.best_solution:
            average_empty = total_empty / len(self.best_solution)

        return average_empty

    def get_total_empty_drives(self):
        empty_drives = 0
        for drive in self.best_solution:
            if drive.truck.capacity == drive.get_empty_space():
                empty_drives += 1

        return empty_drives

    def get_total_drives(self):
        drives = 0
        for drive in self.best_solution:
            drives += 1
        return drives

    def get_total_empty(self):
        total_empty = 0
        for drive in self.best_solution:
            total_empty += drive.get_empty_space()
        return total_empty

    def get_total_empty_per_km(self, solution):

        total_empty_km = 0

        for drive in solution:

            drive_km = drive.end - drive.start  # start & end times == distance on map
            drive_empty = drive.get_empty_space()  # empty space on this drive

            total_empty_km += (
                drive_empty / drive_km
            )  # empty space on this drive * km driven

        return total_empty_km

    def get_total_km(self, solution):
        total_km = 0
        for drive in solution:
            drive_km = drive.end - drive.start  # start & end times == distance on map
            total_km += drive_km
        return total_km

    def get_total_empty_times_km(self, solution):

        total_empty_km = 0

        for drive in solution:

            drive_km = drive.end - drive.start  # start & end times == distance on map
            drive_empty = drive.get_empty_space()  # empty space on this drive

            total_empty_km += (
                drive_km * drive_empty
            )  # empty space on this drive * km driven

        return total_empty_km

    # Create a progress bar

    def get_empty_km_norm(self, solution):
        empty_km_norm = self.get_total_empty_times_km(solution) / (
            self.get_total_km(solution) * 32
        )
        return empty_km_norm

    def get_best_opt(self):
        swap_norm = self.get_swap_norm(self.best_solution)
        empty_km_norm = self.get_empty_km_norm(self.best_solution)
        return swap_norm + empty_km_norm

    def bubble_sort(self, arr):
        n = len(arr)
        swaps = 0
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1
        return arr, swaps

    def get_swaps(self, solution):
        arr = []

        for drive in solution:

            drive_ords = []

            for order in drive.orders:

                drive_ords.append(order.priority)

                sorted_ords = sorted(drive_ords)

            arr.extend(sorted_ords)

        sorted_arr, num_swaps = self.bubble_sort(arr)
        sorted_arr.reverse()
        sorted_max, max_swaps = self.bubble_sort(sorted_arr)

        return num_swaps

    def get_swaps_max(self, solution):
        arr = []

        for drive in solution:
            drive_ords = []

            for order in drive.orders:
                drive_ords.append(order.priority)
                sorted_ords = sorted(drive_ords)

            arr.extend(sorted_ords)

        sorted_arr, num_swaps = self.bubble_sort(arr)
        sorted_arr.reverse()
        sorted_max, max_swaps = self.bubble_sort(sorted_arr)

        return max_swaps

    def get_swap_norm(self, solution):
        swap_norm = self.get_swaps(solution) / self.get_swaps_max(solution)
        return swap_norm


def move_items_to_end(lst, n):
    # Ensure n is not greater than the length of the list
    n = min(n, len(lst))
    # Take the first n elements and the rest of the list
    return lst[n:] + lst[:n]
