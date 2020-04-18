import getandcheckproof

def test(q):
    problem = [1, 2, 3, 6, 6, 6, 12]
    assignment = [1, 1, 1, -1, -1, -1, 1]
    proof = getandcheckproof.get_proof(problem, assignment, q)
    print("proof: " + str(proof))
    return getandcheckproof.verify_proof(problem, proof)


print("result: " + str(test(4)))
# witness = partitioning.get_witness([4, 11, 8, 1], [1, -1, 1, -1])
# tree = merkletree.MerkleTree(witness)
