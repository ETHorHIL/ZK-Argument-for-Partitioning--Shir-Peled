import getandcheckproof
import merkletree
import partitioning
import random


def get_proof(problem, num_queries, witness):
    proof = []
    randomness_seed = problem[:]
    for i in range(num_queries):
        random.seed(str(randomness_seed))
        query_idx = random.randint(0, len(problem))
        if query_idx < len(problem):
            witness[query_idx + 1] = problem[query_idx] + witness[query_idx]
        else:
            witness[0] = 0
            witness[len(witness) - 1] = 0
        tree = merkletree.MerkleTree(witness)
        query_and_response = [tree.get_root()]
        query_and_response += [query_idx]
        query_and_response += tree.get_val_and_path(query_idx)
        query_and_response += tree.get_val_and_path((query_idx + 1) % len(witness))
        proof += [query_and_response]
        randomness_seed += [query_and_response]
    return proof


def verify_proof(problem, proof):
    proof_checks_out = True
    randomness_seed = problem[:]
    for query in proof:
        random.seed(str(randomness_seed))
        query_idx = random.randint(0, len(problem))
        merkle_root = query[0]
        proof_checks_out &= query_idx == query[1]
        if query_idx < len(problem):
            proof_checks_out &= abs(query[2]-query[4]) == abs(problem[query_idx])
        else:
            proof_checks_out &= query[2] == query[4]
        proof_checks_out &= \
            merkletree.verify_zk_merkle_path(merkle_root, len(problem) + 1, \
            query_idx, query[2], query[3])
        proof_checks_out &= \
            merkletree.verify_zk_merkle_path(merkle_root, len(problem) + 1, \
                (query_idx + 1) % (len(problem) +1), query[4], query[5])
        randomness_seed +=[query]
    return proof_checks_out

def test(q):
    problem = [1, 2, 3, 4]
    witness = [1, 2, 3, 4]
    witness += [0]
    proof = get_proof(problem, q, witness)
    return verify_proof(problem, proof)

print("result: " + str(test(5)))
# witness = partitioning.get_witness([4, 11, 8, 1], [1, -1, 1, -1])
# tree = merkletree.MerkleTree(witness)
