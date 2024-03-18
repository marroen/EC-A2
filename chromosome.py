from bitarray import bitarray
from bitarray.util import urandom
from util import count_ones
import random

class Chromosome:

    def __init__(self, data = None):
        if data is None:
            data = urandom(500)
        self.data = data

    # TODO equality constraint uniform crossover
    def uniform(self, second_p):
        
        # for each bit, randomly (!)flip
        first_p = self.data
        n = len(first_p)
        
        first_c = bitarray()
        second_c = bitarray()

        # crossover
        for i in range(0, n):
            rnd = random.random()
            if round(rnd) == 1:
                first_c.append(first_p[i])
                second_c.append(second_p[i])
            else:
                first_c.append(second_p[i])
                second_c.append(first_p[i])

        return [[first_p, second_p], [first_c, second_c]]
