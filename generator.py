import math


class RandomNumberGenerator:
    def __init__(self, seedValue=None):
        self.__seed = seedValue

    def nextInt(self, low, high):
        m = 2147483647
        a = 16807
        b = 127773
        c = 2836
        k = int(self.__seed / b)
        self.__seed = a * (self.__seed % b) - k * c
        if self.__seed < 0:
            self.__seed = self.__seed + m
        value_0_1 = self.__seed
        value_0_1 = value_0_1 / m
        return low + int(math.floor(value_0_1 * (high - low + 1)))

    def nextFloat(self, low, high):
        low *= 100000
        high *= 100000
        val = self.nextInt(low, high) / 100000.0
        return val


def knapsack_instance_generator(n):
    generator = RandomNumberGenerator(seedValue=22)
    values = [generator.nextInt(1, 30) for _ in range(n)]
    weights = [generator.nextInt(1, 30) for _ in range(n)]
    capacity = generator.nextInt(n * 5, n * 10)

    return values, weights, capacity
