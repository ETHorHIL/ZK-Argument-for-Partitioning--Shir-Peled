import merkle_tree
import create_witness
import random


class prover(object):
    def __init__(self, problem, solution):
        self.witness = create_witness.create_witness(problem, solution)
        self.tree = merkle_tree.merkle_tree(self.witness)

    def give_root(self):
        return self.tree.give_root()

    def answer_query(self, query):
        if query == problem_lenght:
            return self.tree.give_value_n_path(0), \
                   self.tree.give_value_n_path(problem_lenght)
        else:
            return self.tree.give_value_n_path(query), \
                   self.tree.give_value_n_path(query + 1)


class verifier(object):
    def __init__(self, problem):
        self.problem = problem
        self.tree = merkle_tree.merkle_tree(self.problem)

    def give_query(self, root, seed):
        random.seed(seed)
        self.root = root
        self.query = random.randint(0, problem_lenght)
        return self.query

    def verify(self, answer, query, root):
        if query == problem_lenght:
            verify_1 = self.tree.verify_proof(root, 0, answer[0][0],
                                          answer[0][1], len(self.tree.data))
            verify_2 = self.tree.verify_proof(root, query, answer[1][0],
                                          answer[1][1], len(self.tree.data))
        else:
            verify_1 = self.tree.verify_proof(root, query, answer[0][0],
                                      answer[0][1], len(self.tree.data))

            verify_2 = self.tree.verify_proof(root, query + 1, answer[1][0],
                                          answer[1][1], len(self.tree.data))
        verify_3 = True
        if query == (int(problem_lenght)):
            verify_3 = answer[0][0] == answer[1][0]
        else:
            verify_3 = abs(p_problem[query]) == abs(answer[1][0] - answer[0][0])
        return verify_1 & verify_2 & verify_3


# public values
prob = [1, 1, 2, 4]
p_problem = prob  # [1, 2, 3, 4, 1, 1]
problem_lenght = len(p_problem)
num_queries = 10

# private values
solution = [-1, -1, -1, 1]


answer = []
P = prover(p_problem, solution)
V = verifier([[0] for x in p_problem])
root = P.give_root()
query = V.give_query(root, str(p_problem))
proof = P.answer_query(query)
print(answer)
answer += [query, root, proof]
print(answer)

for i in range(0, num_queries):
    P = prover(p_problem, solution)
    root = P.give_root()
    query = V.give_query(root, str(answer[3 * i]) + str(answer[3 * i + 1]) + str(answer[3 * i + 2]))
    proof = P.answer_query(query)
    answer += [query, root, proof]
# [query, root, proof, query root, proof]
for i in range(0, len(answer)):
    print("round: " + str(i))
    print("answer[" + str(i) + "]: " + str(answer[i]))

passed = True
passed &= answer[0] == V.give_query(answer[1], str(p_problem))
passed &= V.verify(answer[2], answer[0], answer[1])


for i in range(0, num_queries - 1):
    querycheck = answer[3 * i + 3] == V.give_query(answer[1 + 3 * i], str(answer[3 * i]) + str(answer[1 + 3 * i]) + str(answer[2 + 3 * i]))
    passed &= querycheck
    verify = V.verify(answer[2 + 3 * i], answer[3 * i], answer[1 + 3 * i])
    passed &= verify

print(passed)


"""
querycheck2 = answer[0 + 3] == V.give_query(answer[0 + 4], str(answer[0]) + str(answer[1]) + str(answer[2]))
print(querycheck2)
verify2 = V.verify(answer[2 + 3], answer[0 + 3], answer[1 + 3])
print(verify2)
"""

# ok check that first query (answer[0]) = givequery(answer[1], problem)
# ok verify(answer3, query, root) add query and root
# ok check that next query (answer 3,7) = giverquery(answer[1+4], )
