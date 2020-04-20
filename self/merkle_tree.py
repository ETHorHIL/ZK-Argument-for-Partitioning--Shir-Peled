import random
import hashlib
from math import log2, ceil


def hash_string(input):
    return hashlib.sha256(input.encode()).hexdigest()


class merkle_tree(object):
    """docstring for merkle_tree."""

    def __init__(self, data_input):
        self.data = data_input
        next_power = 2 ** ceil(log2(len(self.data)))
        self.data += [0] * (next_power - len(self.data))
        self.random_vector = [random.randint(0, 2**32) for x in self.data]
        self.tree = []
        self.tree += \
            [x for tup in zip(self.data, self.random_vector) for x in tup]
        for i in range(0, len(self.data)*2 - 1):
            self.tree += [hash_string(str(self.tree[i * 2]) +
                          str(self.tree[i * 2 + 1]))]

    def give_root(self):
        return self.tree[len(self.tree) - 1]

    def find_sibling_id(self, id):
        sibling = id - 2 * (id % 2) + 1
        return sibling

    def find_sibling_of_parent_id(self, id):
        sibling = self.find_sibling_id(id)
        parent = int(max(id, sibling)/2) + len(self.data) * 2
        sibling_of_parent = self.find_sibling_id(parent)
        return sibling_of_parent

    def give_value_n_path(self, id):
        value = self.data[id]
        path = []
        id = id * 2
        path += [self.tree[self.find_sibling_id(id)]]
        while id < len(self.data) * 4 - 4:
            sibling_of_parent = self.find_sibling_of_parent_id(id)
            path += [self.tree[sibling_of_parent]]
            id = sibling_of_parent

        path += [self.give_root()]
        return value, path

    def parent_hash(self, id, value, sibling):
        parent_value = []
        if int(id) % 2 == 0:
            parent_value = hash_string(str(value) + str(sibling))
        else:
            parent_value = hash_string(str(sibling) + str(value))
        return parent_value

    def verify_proof(self, root, id, value, path, data_size):
        id = id * 2
        value = value
        sibling = path[0]
        value = self.parent_hash(id, value, sibling)
        for i in range(1, len(path) - 1):
            sibling = path[i]
            id = int(max(id, self.find_sibling_id(id))/2) + data_size * 2
            value = self.parent_hash(id, value, sibling)
        return value == root


def test():
    treesize = 4
    tree = merkle_tree([1, 2, 3, 4])
    for i in range(0, treesize):
        id = i
        value = tree.give_value_n_path(id)[0]
        path = tree.give_value_n_path(id)[1]
        root = tree.give_root()
        data_size = len(tree.data)
        print(i)
        print(str(tree.verify_proof(root, id, value, path, data_size)))


test()
