from typing import Dict, List, Set


class Map:
    def __init__(self):
        self.routes: Dict[[int, int], int] = {}
        self.origins: Set(int) = set()  # or list?
        self.destinations: Set(int) = set()  # ?
        self.positions: List[int] = []

    def add_route(self, origin, destination, costs):
        self.routes[(origin, destination)] = costs
        self.origins.add(origin)
        self.destinations.add(destination)
        if origin not in self.positions:
            self.positions.append(origin)
        if destination not in self.positions:
            self.positions.append(destination)

    def get_num_positions(self):
        return len(self.positions)

    def get_num_origins(self):
        return len(self.origins)

    def get_num_destinations(self):
        return len(self.destinations)

    def get_positions(self):
        return list(self.positions)

    def get_origins(self):
        return list(self.origins)

    def get_destinations(self):
        return list(self.destinations)

    def get_costs(self, origin, destination):
        # Retrieve the cost using the same tuple forma
        return self.routes.get((origin, destination), -1)

    def get_cheapest_origin(self, destination):
        best = -1
        best_val = float("inf")
        for origin in self.origins:
            cost = self.routes.get(
                (origin, destination), float("inf")
            )  # use tuple for key and provide default if not found
            if cost < best_val:
                best_val = cost
                best = origin
        return best

    def compute_route_matrix(self) -> List[List[int]]:
        """
        Function to produce an n-by-n matrix M, where n is the number of nodes, and
        where M[i][j] = cost(route i->j).
        """
        routes_matrix = [
            [-1 for _ in range(len(self.positions))] for _ in range(len(self.positions))
        ]
        for origin, destination in self.routes.keys():
            routes_matrix[self.positions.index(origin)][
                self.positions.index(destination)
            ] = self.routes[(origin, destination)]
        return routes_matrix
