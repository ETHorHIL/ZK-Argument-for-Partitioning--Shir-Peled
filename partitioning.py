# The partitioning problem:
# You have a list of lenght l and want to divide it into two seperate lists
# of lenght m and k that add up to the same value. l=m+k
# We say that m is a satisfying assignment if
# 1. len(m)==len(l)
# 2. all of the elements in m are either -1 or 1 (this defines on which side of
# the equation they are on)
# 3. The dot product of l and m is zero
# example l=[2,2,4,8] => m = [1,1,1,-1]
# Given l we can prove that we have a solution by revealing m but thats not ZK
# define p_i as the dot product of m and l up to the ith position
# then p has two interesting properties:
# 1. p starts with 0
# 2. l[i] = |p[i+1]-p[i]|

# Draft for ZK protocol:
# p claims to know a partition p of the common input l
# 1. V chooses random i and sends to p
# 2. if i = n then P sends p[0] and p[n], otherwise p sends p[i] and p[i+1]
# 3. V checks that |l[i]| =|p[i+1]-p[i]|

# Observations:
# -P is honest, follows the protocol, so its not a POK
# -We will repeat the protocol sequentially to reduce soundness error
# -This is not ZK because V learns something about m. We will fix that.

# Fixing ZK
# 1. P flips a coin. If its heads we leave m as it is, otherwise we multiply
# all elements in m with -1. This does not change the dot product of p
# 2. We choose a random number r and add it to all elements of p. p will now
# start and end with r

# below the code that takes l and m and constructs a witness p

import random


def get_witness(problem, solution):
    """
    Given an instance of the problem via a list of numbers and a solution which
    is a list of -1 and 1, we say a solution satisfies the problem if the dot
    product is 0
    """
    sumproduct = 0
    maximum_value = 0
    coinflip = 1 - 2 * random.randint(0, 1)
    witness = [sumproduct]
    assert len(problem) == len(solution)
    for problem_i, solution_i in zip(problem, solution):
        assert coinflip == 1 or coinflip == -1
        sumproduct += problem_i * solution_i * coinflip
        witness += [sumproduct]
        maximum_value = max(maximum_value, problem_i)
    random_r = random.randint(0, maximum_value)
    witness = [x + random_r for x in witness]
    print("problem= " + str(problem))
    print("solution= " + str(solution))
    print("coinflip= " + str(coinflip))
    print("random_r= " + str(random_r))
    print("maximum_value= " + str(maximum_value))
    print("witness= " + str(witness))
    return witness
