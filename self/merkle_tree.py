import random
import hashlib
from math import log2, ceil


def hash_string(input):
    return hashlib.sha256(input.encode()).hexdigest()


class merkle_tree(object):
    """docstring for merkle_tree."""

    def __init__(self, data_input):
        self.data = data_input
        print("creating tree...")
        print("original data: " + str(self.data))
        next_power = 2 ** ceil(log2(len(self.data)))
        self.data += [0] * (next_power - len(self.data))
        print("data added to next power: " + str(self.data))
        self.random_vector = [random.randint(0, 2**32) for x in self.data]
        self.tree = []
        self.tree += \
            [x for tup in zip(self.data, self.random_vector) for x in tup]
        print("data: " + str(self.data))
        print("random_vector: " + str(self.random_vector))
        print("tree lvl0" + str(self.tree))
        for i in range(0, len(self.data)*2 - 1):
            print("i: " + str(i))
            print("len data*2-1: " + str(len(self.data)*2 - 1))
            self.tree += [hash_string(str(self.tree[i * 2]) +
                          str(self.tree[i * 2 + 1]))]
            print("hashing tree items: " + str(self.tree[i]) +
                  ", " + str(self.tree[i+1]))
            print("hash result: " + hash_string(str(self.tree[i]) +
                  str(self.tree[i+1])))
        print("tree lvl 0 and 1: " + str(self.tree))

    def give_root(self):
        return self.tree[len(self.tree) - 1]

    def find_sibling_id(self, id):
        sibling = id - 2 * (id % 2) + 1
        return sibling

    def find_sibling_of_parent_id(self, id):
        print("id before sibling:" + str(id))
        sibling = self.find_sibling_id(id)
        print("sibling: " + str(sibling))
        parent = int(max(id, sibling)/2) + len(self.data) * 2
        print("parent: " + str(parent))
        sibling_of_parent = self.find_sibling_id(parent)
        print("sibling_of_parent: " + str(sibling_of_parent))
        return sibling_of_parent
    # def give_value_n_path(self, id):

    def give_value_n_path(self, id):
        value = self.data[id]
        path = []
        path += [self.tree[self.find_sibling_id(id * 2)]]
        # for i in range(0, int(log2(len(self.data))-1)):
        id = id * 2
        while id < len(self.data) * 4 - 5:
            print("id: " + str(id))
            sibling_of_parent = self.find_sibling_of_parent_id(id)
            print("sibling_of_parent " + str(sibling_of_parent))
            path += [self.tree[sibling_of_parent]]
            id = sibling_of_parent
            print("id: " + str(id) + " < " + " data * 4 - 4: " +
                  str(len(self.data) * 4 - 4))
        path += [self.give_root()]
        return value, path


tree = merkle_tree([1, 2, 3])
# print(tree.find_sibling_id(9))
valuenpath = tree.give_value_n_path(3)
print(valuenpath)
print(len(valuenpath[1]))
