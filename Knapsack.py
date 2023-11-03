class Knapsack:
    def __init__(self, weights, values, maximum_capacity):
        self.weights = weights
        self.values = values
        self.maximum_capacity = maximum_capacity
        self.number_of_items = len(weights)

    def __str__(self):
        return f"Weights: {self.weights}, values: {self.values}, " \
               f" maximum capacity: {self.maximum_capacity}," \
               f" number of items: {self.number_of_items}"
