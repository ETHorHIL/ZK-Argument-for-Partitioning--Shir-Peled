import merkletree
import partitioning
import random


def get_proof(problem, solution, num_queries):
    proof = []
    randomness_seed = problem[:]
    for i in range(num_queries):
        witness = partitioning.get_witness(problem, solution)
        tree = merkletree.MerkleTree(witness)
        random.seed(str(randomness_seed))
        query_idx = random.randint(0, len(problem))
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
        #print("query_idx == query (same query)" + str(proof_checks_out))
        #Test witness properties
        if query_idx < len(problem):
            proof_checks_out &= abs(query[2]-query[4]) == abs(problem[query_idx])
        else:
            proof_checks_out &= query[2] == query[4]
        # authenticate path
        #print("p(n+1) - p(n) = l(n): " + str(proof_checks_out))
        proof_checks_out &= \
            merkletree.verify_zk_merkle_path(merkle_root, len(problem) + 1, \
            query_idx, query[2], query[3])
        #print("path1 authentic" + str(proof_checks_out))
        proof_checks_out &= \
            merkletree.verify_zk_merkle_path(merkle_root, len(problem) + 1, \
                (query_idx + 1) % (len(problem) +1), query[4], query[5])
        #print("path2 authentic" + str(proof_checks_out))
        randomness_seed +=[query]
    return proof_checks_out
