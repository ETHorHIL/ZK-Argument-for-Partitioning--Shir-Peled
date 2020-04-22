import merkle_tree
import create_witness
import random
import math

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

    def fiat_shamir_proof(self, num_queries, p_problem, solution, seed):
        answer = []
        for i in range(0, num_queries):
            P = prover(p_problem, solution)
            root = P.give_root()
            query = V.give_query(root, seed)
            proof = P.answer_query(query)
            answer += [query, root, proof]
            seed = str(answer[3 * i]) + str(answer[3 * i + 1]) + str(answer[3 * i + 2])
        return answer


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

    def fiat_shamir_verification(self, answer, problem, num_queries):
        passed = True
        passed &= answer[0] == V.give_query(answer[1], str(p_problem))
        passed &= V.verify(answer[2], answer[0], answer[1])
        for i in range(0, num_queries - 1):
            passed &= answer[3 * i + 3] \
                                 == V.give_query(answer[1 + 3 * i],
                                                 str(answer[3 * i]) +
                                                 str(answer[1 + 3 * i]) +
                                                 str(answer[2 + 3 * i]))
            passed &= V.verify(answer[2 + 3 * i], answer[3 * i],
                               answer[1 + 3 * i])
        return passed


# public values
p_problem = [1, 1, 2, 4]
problem_lenght = len(p_problem)
num_queries = int(math.log(0.0000001, 1/problem_lenght))
# private values
solution = [-1, -1, -1, 1]

P = prover(p_problem, solution)
V = verifier([[0] for x in p_problem])


def test():
    root = ""
    seed = V.give_query(root, str(p_problem))
    answer = P.fiat_shamir_proof(num_queries, p_problem, solution, seed)
    verification = V.fiat_shamir_verification(answer, p_problem, num_queries)
    print(verification)


test()
