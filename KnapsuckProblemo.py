import random
import numpy as np
from Knapsack import Knapsack
from generator import knapsack_instance_generator
from CoolingFunction import CoolingFunction

"""
Sąsiedztwo typu swap ma rozmiar n2. Cała przestrzeń rozwiązań jest n silnia. Wszystkie algorytmy bazują na sprawdzaniu sąseidztwa - najbardziej popularny jest swap, 
insercja też jest, invert, reverse lub twist w przypadku komiwojażera. Jak mamy zaplątanie, jak jest przestrzeń euklidesowa to odwrócenia są dobre.
Losowy jest dla nieskończenie wielkich instancji, jesli damy np. mneijszą liczbę iteracji. S
Są też inne sąsiedztwa - dedukowane do różnych problemów. Wyznacza się ścieżkę krytyczną, poruszamy tylko zadania skrajne. Jest jedno rozwiązanie. Będzie istatona kalibracja parametróœ liczbowych - liczba iteracji i dedykowana do algorytmu.
Rozwiązanie początkowe i liczb aiteracji. W Wersji rozszerzonej będą już dedykowane do algorytmu. 
Reprezentacja rozwiązania - w dyskretnym ciąg binarny mówiący czy wchodzą czy nie wchodzą.


1 ścieżka
W dwuplecakowym jest np. negacja bitu. Może to prowadzić do rozwiązań niedopuszczalnych i to trzeba nadzorować.

Przeszukiwanie losowe - trywialny bo mieści się w trzech korkach:
1) startujemy z jakiegoś rozwiązania
2) dopóki warunek stopu nie jest spełniony - wylosuj rozwiązanie x spośród sąsiadów x'
 -jeśli f(x')<f(x) to wykonujemy x<-x'
3) Wypisz rozwiązanie

W każdej iteracji losuje jedno sąsiednie rozwiązanie - robimy jednego losowego swapa, zamieniamy i przeliczamy, akcpetujemy je tylko wtedy jeśli jest lepsze. Przez to jeśli pierwsze rozwiązanie będzie optimum 
no to on po prostu sie na nim zatrzyma.

W poszukiwaniu zstępującym przewaga jest taka, że iteracja ma dużą złożoność, jest wolniejszy ale nie ma w sobie nic losowego, jest w pełni deterministyczny. W losowym za każdym razem znajdujemy inne rozwiązanie.

Rozszerzone:

Symolowane wyżarzania

Trzeba mieć zminna która przechowuje najlepsze dotychczasowe rozwiązanie. 
Jest ten wzorek, jak go wpiszemy do kodu bez zrozumienia to tez będzie git.Geometryczna często sprawdza sie lepiej niż liniowa, ale można wrzucić switcha żeby to sobie sprawdzić w kodzie
t=t-B albo t=At gdzie A to między 0.95 a 0.9999. 

Temperatura początkowa to też jest do przetestowania jaką najlepiej wybrać. Największy wpły będzie miał schemat chłodzenia i jego parametr niż sama temperatura poczatkowa (chociaż jak
bedzie na niska to też źle).


Poszukiwanie z zakazami

Schemat jest bardzo zblizony
"""""


def best_of_n(knapsack: Knapsack, n):
    best_array = []
    best_value = 0

    for i in range(n):
        binary_array = [random.randint(0, 1) for i in range(knapsack.number_of_items)]
        value, weight = calculate_value_weight(binary_array, knapsack)
        if value > best_value and weight <= knapsack.maximum_capacity:
            best_value = value
            best_array = binary_array

    return best_array


def random_search(knapsack: Knapsack, iterations):
    # Initialize a best random bianry array from a 100
    solution = best_of_n(knapsack, 100)
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
    # Calculate the total value and weight of the knapsack
    value = sum(np.multiply(solution, knapsack.values))
    weight = sum(np.multiply(solution, knapsack.weights))
    return value, weight


def find_neighbour(knapsack, solution):
    index = random.randint(0, knapsack.number_of_items - 1)
    new_solution = solution.copy()
    new_solution[index] = 1 - new_solution[index]
    return new_solution


def simulated_annealing(knapsack: Knapsack, iterations, initial_temperature, alpha,
                        cooling: CoolingFunction = CoolingFunction.GEOMETRIC,
                        final_temperature=0):
    # Get best current solution from random 100
    current_solution = best_of_n(knapsack, 100)

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
        neighbour_value, neighbour_weight = calculate_value_weight(neighbour_solution,
                                                                   knapsack)

        # Calculate the difference between neigbour and current solution
        delta_value = neighbour_value - current_value

        # Check if weight is correct and if neighbour solution is better or the probability conditions is met then
        # current_solution <- neighbour_solution
        if neighbour_weight <= knapsack.maximum_capacity and (
                delta_value > 0 or np.exp(
            -delta_value / initial_temperature) > random.random()):
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


# def simulated_annealing(knapsack: Knapsack, iterations, start_temperature, alpha):
#     solution = best_of_n(knapsack, 100)
#     # Calculate the initial value and weight of the knapsack
#     current_value, current_weight = calculate_value_weight(solution, knapsack)
#     current_temperature = start_temperature
#     best_solution = solution
#     best_value = current_value
#     accepted_worse = 0
#
#     # Iterate for the specified number of iterations
#     for i in range(iterations):
#         # Choose a random bit to negate
#         index = random.randint(0, len(solution) - 1)
#         # Negate the bit
#         solution[index] = 1 - solution[index]
#         # Calculate the new value and weight of the knapsack
#         new_value, new_weight = calculate_value_weight(solution, knapsack)
#
#         # Check if the new knapsack is valid and has a higher value
#         if new_weight <= knapsack.maximum_capacity and new_value > current_value:
#             # If so, update the current knapsack and values
#             current_value = new_value
#             current_weight = new_weight
#
#         else:
#             # Otherwise, calculate probability
#             delta = new_value - current_value
#             accept_p = np.exp((-delta) / current_temperature)
#             # print("Accept p ", accept_p, "Delta ",current_value-new_value)
#             p = random.random()
#             # ---------------------------------------------------------------------------------
#             # no wlasnie ten warunk p<accpe_P? Jak to ma być, kiedy to mamy akceptować????
#             # ---------------------------------------------------------------------------------
#
#             if p < accept_p and new_weight <= knapsack.maximum_capacity:
#                 current_value = new_value
#                 current_weight = new_weight
#                 accepted_worse += 1
#             else:
#                 solution[index] = 1 - solution[index]
#
#         if current_value > best_value:
#             best_solution = solution
#             best_value = current_value
#
#         # Update temperature
#         # print("Current temp ", current_temperature)
#         current_temperature = alpha * current_temperature
#     print(accepted_worse)
#
#     # Return the final knapsack as a binary array
#     return best_solution, sum(np.multiply(best_solution, knapsack.values)), sum(
#         np.multiply(best_solution, knapsack.weights))

if __name__ == "__main__":
    weights, values, maximum_capacity = knapsack_instance_generator(1)
    knapsack = Knapsack(weights, values, maximum_capacity)
    print(random_search(knapsack, 10))
