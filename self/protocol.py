import merkle_tree
import create_witness
import random

# public values
problem = [2, 1, 1]

# private values
solution = [1, -1, -1]
witness = []


class prover(object):
    def __init__(self, problem, solution):
        self.witness = create_witness.create_witness(problem, solution)
        self.tree = merkle_tree.merkle_tree(witness)


class verifier(object):
    def __init__(self, problem):
        self.tree = merkle_tree.merkle_tree(problem)





def p_step_one(problem, solution):
    return prover.tree.give_root()

def v_step_two():
    return random.randint(0, len(problem))


def v_step_three(query, tree):
    print(str(tree.data))
    if query == len(tree.data) - 1:
        return tree.give_value_n_path(0), \
               tree.give_value_n_path(len(tree.data) - 1)
    else:
        return tree.give_value_n_path(query - 2), \
               tree.give_value_n_path(query - 1)


p_one = p_step_one(problem, solution)
v_two = v_step_two()
p_three = v_step_three(v_two, tree)

print(p_one)
print(v_two)
print(p_three)
