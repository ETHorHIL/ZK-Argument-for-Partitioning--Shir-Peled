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
        print("len " + str(len(self.data)))
        print("log2 " + str(log2(len(self.data))))
        print("ceil " + str(ceil(log2(len(self.data)))))
        print("2**x " + str(int(2**(ceil(log2(len(self.data)))))))
        self.data.extend([0] * (data_length_next_power_2 - len(data)))
        print(self.data)
        self.tree = ["" for x in self.data] + \
            [hash_string(str(x)) for x in self.data]
        for i in range(len(self.data)-1, 0, -1):
            self.tree[i] = hash_string(self.tree[2*i]+self.tree[2*i+1])
        print(self.tree)

    def get_root(self):
        return self.tree[1]

    def get_val_and_path(self, id):
        value = self.data[id]
        auth_path = []
        id = id + len(self.data)
        while id > 1:
            # add the sibling one to the right
            auth_path += self.tree[id ^ 1]
            # go one layer up, round down
            id = id // 2
        return value, auth_path


tree = MerkleTree([1, 2, 3])
print(tree.get_val_and_path(2))
