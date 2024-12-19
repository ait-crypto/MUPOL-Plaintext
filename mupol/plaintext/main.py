import os
import sys

from mupol.plaintext.args_handler import ArgsHandler
from mupol.plaintext.freighters_day_planning.random_problem_generator import (
    RandomProblemGenerator,
)
from mupol.plaintext.freighters_day_planning.simple_solver import SimpleSolver

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def main():
    # Initialize the problem generator with specific parameters
    args = ArgsHandler(sys.argv[1:]).args
    generator = RandomProblemGenerator(
        args.num_freighters,
        args.min_num_trucks,
        args.max_num_trucks,
        args.truck_capacity,
        args.num_orders,
        args.min_order_volume,
        args.max_order_volume,
        args.random_seed,
    )
    problem = generator.get_problem()

    # Print the problem description
    # print(problem)

    # Initialize the solver and solve the problem
    solver = SimpleSolver()
    solver.optimize(problem, args.num_iters)

    # Print the solution

    print(solver.get_text_solution())


if __name__ == "__main__":
    main()
