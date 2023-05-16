from Knapsack import Knapsack
from generator import knapsack_instance_generator
from CoolingFunction import CoolingFunction
from solver import random_search, simulated_annealing
import time
import pandas as pd
from InitialSolution import InitialSolution

if __name__ == '__main__':

    times = []
    solutions = []
    items = list(range(5, 205, 5))
    iterations = list(range(10,1010,10))
    alphas = [0.01 * i for i in range(1, 100)]

    temperatures = list(range(50,1000,50))





    number_of_test = 100
    for i in items:
        weights, values, maximum_capacity = knapsack_instance_generator(i)
        knapsack = Knapsack(weights, values, maximum_capacity)
        for _ in range(25):

            # Run the random search algorithm
            iterations = 1000
            start_time = time.time()
            start_temp = sum(knapsack.values)
            cooling_mode = CoolingFunction.GEOMETRIC
            alpha = 0.98
            #solution_SA = simulated_annealing(knapsack, iterations, start_temp,alpha,CoolingFunction.GEOMETRIC)
            solution_SA = random_search(knapsack, iterations)

            elapsed_time = time.time() - start_time
            times.append(elapsed_time)
            solutions.append(
                {
                    "Algorithm": "Random Search",
                    "Items": knapsack.number_of_items,
                    #"Alpha" : alpha,
                    #"InitialTemp" : start_temp,
                    #"CoolingMode" : cooling_mode.name,
                    "BinaryArray": solution_SA[0],
                    "Iterations": iterations,
                    "Time": elapsed_time,
                    "Value": solution_SA[1],
                    "Weight": solution_SA[2]
                }
            )
    df = pd.DataFrame.from_dict(solutions)
    df.to_csv("data/rs_items_time_25.csv", index=False)


    #print(solution[3],solution[4],solution[5])
    print(df.head())
        # ---------------------------------------------------------------------------------
        # jaka powinna być inicjalna temperatura?
        #start_temp = sum(knapsack.values) / 10
        # ---------------------------------------------------------------------------------
        #solution_SA = simulated_annealing(knapsack, iterations, start_temp, 0.98, CoolingFunction.GEOMETRIC)

        # Print the solution
