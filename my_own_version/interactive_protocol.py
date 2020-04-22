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
        self.tree = merkle_tree.merkle_tree(problem)

    def give_query(self, root):
        self.root = root
        self.query = random.randint(0, problem_lenght)
        return self.query

    def verify(self, answer):
        if self.query == problem_lenght:
            verify_1 = self.tree.verify_proof(self.root, 0, answer[0][0],
                                          answer[0][1], len(self.tree.data))
            verify_2 = self.tree.verify_proof(self.root, self.query, answer[1][0],
                                          answer[1][1], len(self.tree.data))
        else:
            verify_1 = self.tree.verify_proof(self.root, self.query, answer[0][0],
                                      answer[0][1], len(self.tree.data))

            verify_2 = self.tree.verify_proof(self.root, self.query + 1, answer[1][0],
                                          answer[1][1], len(self.tree.data))
        verify_3 = True
        if self.query == (int(problem_lenght)):
            verify_3 = answer[0][0] == answer[1][0]
        else:
            verify_3 = abs(p_problem[self.query]) == abs(answer[1][0] - answer[0][0])
        return verify_1 & verify_2 & verify_3


# public values
p_problem = [1, 1]  # [1, 2, 3, 4, 1, 1]
problem_lenght = len(p_problem)
# private values
solution = [-1, 1]

P = prover(p_problem, solution)
V = verifier([[0] for i in p_problem])
root = P.give_root()
query = V.give_query(root)
answer = P.answer_query(query)
verification = V.verify(answer)
print("V verification: " + str(verification))
