# ZK-Argument-for-Partitioning
Following the ZK tutorial for Partitioning by Shir-Peled
https://www.shirpeled.com/2018/10/a-hands-on-tutorial-for-zero-knowledge.html

Protocol Summary:

To summarize the theory, the protocol by which the prover proves knowledge of a satisfying assignment to the Partition Problem is:  
1. The prover generates a witness (using get_witness from the first post in this series).
2. The prover creates a ZK Merkle Tree from the witness, and sends its root-hash to the verifier.
3. The verifier sends a random number $i$ to the prover.
4. If $i < n$ then the prover sends to the verifier:
5. The elements in places $i$ and $i + 1$ in the witness.
6. The authentication paths proving that these answers are consistent with the root sent in step (2).
7. If $i == n$ then the prover sends the first and the last elements in the witness, with the authentication paths etc.
8. The verifier checks the authentication paths against the root, and the returned numbers against the problem instance, to verify properties (1) and (2) of the witness as they are described in the first post.
9. The verifier returns true iff everything checks out.
