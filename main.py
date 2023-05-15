from Knapsack import Knapsack
from generator import knapsack_instance_generator
from CoolingFunction import CoolingFunction
from solver import random_search, simulated_annealing

if __name__ == '__main__':
    weights, values, maximum_capacity = knapsack_instance_generator(20)
    knapsack = Knapsack(weights, values, maximum_capacity)

    print(knapsack)

    # Run the random search algorithm
    iterations = 100
    solution_RS = random_search(knapsack, iterations)
    # ---------------------------------------------------------------------------------
    # jaka powinna być inicjalna temperatura?
    start_temp = sum(knapsack.values) / 10
    # ---------------------------------------------------------------------------------
    solution_SA = simulated_annealing(knapsack, iterations, start_temp, 0.98, CoolingFunction.GEOMETRIC)

    # Print the solution
    print("Solution RS: ", solution_RS, "\nSolution SA: ", solution_SA)
