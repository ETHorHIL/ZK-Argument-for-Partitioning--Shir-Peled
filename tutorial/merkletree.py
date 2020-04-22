
import random
import hashlib
from math import log2, ceil


def hash_string(input):
    return hashlib.sha256(input.encode()).hexdigest()


class MerkleTree:

    def __init__(self, data):
        self.data = data
        data_length_next_power_2 = int(2**(ceil(log2(len(data)))))
        self.data.extend([0] * (data_length_next_power_2 - len(data)))
        rand_list = [random.randint(0, 1 << 32) for x in self.data]
        self.data = [x for tup in zip(self.data, rand_list) for x in tup]
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
