
import random


def create_witness(problem, solution):
    coinflip = 1 - 2 * random.randint(0, 1)
    rand = random.randint(0, 2 ** 32)
    witness = [0]
    for i in range(0, len(problem)):
        witness += [witness[i] + solution[i] * coinflip * problem[i]]
    witness = [x + rand for x in witness]
    return witness


def test():
    create_witness([2, 1, 1], [1, -1, -1])
