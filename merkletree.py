"""
P claims to know a solution to a partitioning problem


1. V sends a random i
2. P samples a coinflip and a random r
   P calculates the sumproduct of the partitioning problem and the solution
   vector. He changes the sign on the solution and adds up the random r to each
   entry of the vector
   If i = n then P sends p[0] and p[n], otherwise p sends p[i] and p[i+1]
# 3. V checks that |l[i]| =|p[i+1]-p[i]|

If P acts according to the protocol all is fine. But if P is a cheater and
doesnt know the solution, he could just pretend to know it. He sends values
that satisfy V.

In order to fix this we need to let the V commit to his values of p first.
That way he can not just make them up. We use a merkle tree as commitment.

"""

import random
import hashlib
from math import log2, ceil


def hash_string(input):
    return hashlib.sha256(input.encode()).hexdigest()


class MerkleTree:

    """
    A naive implementation of a Merkle Tree using SHA256
    """

    def __init__(self, data):
        self.data = data
        # the tree has a power of 2 leaves and needs to be extended
        # if the data is not filling the tree
        data_length_next_power_2 = int(2**(ceil(log2(len(data)))))
        # print("len: " + str(len(self.data)))
        # print("log2: " + str(log2(len(self.data))))
        # print("ceil: " + str(ceil(log2(len(self.data)))))
        # print("2**x: " + str(int(2**(ceil(log2(len(self.data)))))))
        self.data.extend([0] * (data_length_next_power_2 - len(data)))
        # Intertwine with randomness to obtain ZK
        # randint between 1 and 2^32
        rand_list = [random.randint(0, 1 << 32) for x in self.data]
        self.data = [x for tup in zip(self.data, rand_list) for x in tup]
        # Create bottom level of the tree (i.e. leaves)
        self.tree = ["" for x in self.data] + \
            [hash_string(str(x)) for x in self.data]
        for i in range(len(self.data)-1, 0, -1):
            self.tree[i] = hash_string(self.tree[2*i]+self.tree[2*i+1])

    def get_root(self):
        return self.tree[1]

    def get_val_and_path(self, id):
        id = id * 2
        value = self.data[id]
        auth_path = []
        id = id + len(self.data)
        while id > 1:
            # add the sibling one to the right
            auth_path += [self.tree[id ^ 1]]
            # go one layer up, round down
            id = id // 2
        return value, auth_path


def verify_zk_merkle_path(root, data_size, value_id, value, path):
    # hashvalue of data in leafe you want to verify
    cur = hash_string(str(value))
    # assign id of value_id + length of data
    tree_node_id = value_id * 2 + int(2**ceil(log2(data_size * 2)))
    for sibling in path:
        # print("tree_node_id: " + str(tree_node_id))
        assert tree_node_id > 1
        # print("sibling: " + sibling)
        if tree_node_id % 2 == 0:
            cur = hash_string(cur + sibling)
        else:
            cur = hash_string(sibling + cur)
        # print("cur: " + cur)
        tree_node_id = tree_node_id // 2
    assert tree_node_id == 1
    return root == cur


"""
tree = MerkleTree([1, 2, 3])

value_path = str(tree.get_val_and_path(2))

print(tree.get_root())
print(value_path[1][0])

tree.verify_merkle_path(tree.get_root(), 4, 2, 3, value_path[1])
"""
