import random
import numpy as np
from Knapsack import Knapsack
from CoolingFunction import CoolingFunction
from InitialSolution import InitialSolution


def generate_best_of_n_solutions(knapsack: Knapsack, n) -> []:
    """
    This function is used to get initial solution for Knapsack Problem

    :param knapsack: instance of Knapsack class
    :param n: number of randomly selected binary arrays
    :return: best binary list from n random
    """
    best_array = []
    best_value = 0

    for i in range(n):
        binary_array = [random.randint(0, 1) for i in range(knapsack.number_of_items)]
        value, weight = calculate_value_weight(binary_array, knapsack)
        if value > best_value and weight <= knapsack.maximum_capacity:
            best_value = value
            best_array = binary_array

    return best_array


def generate_initial_solution(knapsack: Knapsack) -> []:
    while True:
        solution = [random.randint(0, 1) for i in range(knapsack.number_of_items)]
        value, weight = calculate_value_weight(solution, knapsack)
        if weight <= knapsack.maximum_capacity:
            return solution


def random_search(knapsack: Knapsack, iterations, initial_solution_mode: InitialSolution = InitialSolution.ZEROS):
    """
    This function is a simple random search metaheuristic algorithm for Knapsack Problem

    :param initial_solution_mode: enum for selecting type of initial solution
    :param knapsack: object of class Knapsack
    :param iterations: maximum number of iterations that the algorithm should do to find solution
    :return: found solution for the Knapsack Problem in form of a binary array, value and weight
    """
    # Initialize initial solution
    if initial_solution_mode.value == 0:
        solution = [0] * knapsack.number_of_items
    elif initial_solution_mode.value == 1:
        solution = generate_initial_solution(knapsack)
    elif initial_solution_mode.value == 2:
        solution = generate_best_of_n_solutions(knapsack, 100)
    else:
        raise ValueError("Incorrect initial solution mode")

    # Calculate the initial value and weight of the knapsack
    current_value, current_weight = calculate_value_weight(solution, knapsack)

    # Iterate for the specified number of iterations
    for i in range(iterations):
        # Choose a random bit to negate
        index = random.randint(0, len(solution) - 1)
        # Negate the bit
        solution[index] = 1 - solution[index]
        # Calculate the new value and weight of the knapsack
        neighbour_value, neighbour_weight = calculate_value_weight(solution, knapsack)

        # Check if the new knapsack is valid and has a higher value
        if neighbour_weight <= knapsack.maximum_capacity and neighbour_value > current_value:
            # If so, update the current knapsack and values
            current_value = neighbour_value
            current_weight = neighbour_weight

        else:
            # Otherwise, revert the change to the knapsack
            solution[index] = 1 - solution[index]

    # Return the final knapsack as a binary array
    return solution, sum(np.multiply(solution, knapsack.values)), sum(
        np.multiply(solution, knapsack.weights))


def calculate_value_weight(solution, knapsack: Knapsack):
    """
    Functions for calculating weight and value of items in knapsack

    :param solution: current solution in form of a binary array
    :param knapsack: object from class Knapsack
    :return: the value and weight of items
    """
    # Calculate the total value and weight of the knapsack
    value = sum(np.multiply(solution, knapsack.values))
    weight = sum(np.multiply(solution, knapsack.weights))
    return value, weight


def find_neighbour(knapsack, solution) -> []:
    """
    This function is used to find random neighbour for a solution
    by negating one bit

    :param knapsack: class Knapsack object
    :param solution: current solution in for of a binary array
    :return: new binary array with negated bit
    """
    index = random.randint(0, knapsack.number_of_items - 1)
    new_solution = solution.copy()
    new_solution[index] = 1 - new_solution[index]
    return new_solution


def simulated_annealing(knapsack: Knapsack, iterations, initial_temperature, alpha,
                        cooling: CoolingFunction = CoolingFunction.GEOMETRIC,
                        initial_solution_mode: InitialSolution = InitialSolution.FIRST, final_temperature=0):
    """
    This is a Simulated Annealing algorithm for Knapsack Problem, it is
    a metaheuristic algorithm where we can operate the parameters to find solution for this problem
    which is not always the optimal one.

    :param initial_solution_mode: enum for selecting type of initial solution
    :param knapsack: Knapsack class object
    :param iterations: maximum number of iterations
    :param initial_temperature: the initial temperature for SA
    :param alpha: parameter for cooling function
    :param cooling: enum parameter - cooling mode
    :param final_temperature: optional argument, if we want to achieve some final temperature and
    after that stop the process, default is 0
    :return: solution for the knapsack problem, value and weight
    """
    # Get best current solution from random 100
    if initial_solution_mode.value == 0:
        current_solution = [0] * knapsack.number_of_items
    elif initial_solution_mode.value == 1:
        current_solution = generate_initial_solution(knapsack)
    elif initial_solution_mode.value == 2:
        current_solution = generate_best_of_n_solutions(knapsack, 100)
    else:
        raise ValueError("Incorrect initial solution mode")

    # Calculate value and weight for this solution
    current_value, current_weight = calculate_value_weight(current_solution, knapsack)

    # Store best solution and best value so far
    best_solution = current_solution.copy()
    best_value = current_value
    i = 0
    temperature = initial_temperature

    # While the number of iterations and final temperature condition is not met
    while i < iterations and temperature > final_temperature:

        # Find neighbour solution
        neighbour_solution = find_neighbour(knapsack, current_solution)
        neighbour_value, neighbour_weight = calculate_value_weight(neighbour_solution, knapsack)

        # Calculate the difference between neigbour and current solution
        delta_value = neighbour_value - current_value

        # Check if weight is correct and if neighbour solution is better or the probability conditions is met then
        # current_solution <- neighbour_solution
        if neighbour_weight <= knapsack.maximum_capacity and (
                delta_value > 0 or np.exp(-delta_value / initial_temperature) > random.random()):
            current_solution = neighbour_solution
            current_value = neighbour_value
            current_weight = neighbour_weight

        # Check if f(x) > f(x_best) if so then update best_solution
        if current_value > best_value:
            best_solution = current_solution.copy()
            best_value = current_value

        # Choose cooling mode
        if cooling.value == 0:
            temperature -= alpha
        elif cooling.value == 1:
            temperature *= alpha
        else:
            raise ValueError("Invalid cooling mode")
        i += 1

    return best_solution, sum(np.multiply(best_solution, knapsack.values)), sum(
        np.multiply(best_solution, knapsack.weights))
