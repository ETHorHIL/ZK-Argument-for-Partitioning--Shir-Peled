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
        # print("id before sibling:" + str(id))
        sibling = self.find_sibling_id(id)
        # print("sibling: " + str(sibling))
        parent = int(max(id, sibling)/2) + len(self.data) * 2
        # print("parent: " + str(parent))
        sibling_of_parent = self.find_sibling_id(parent)
        # print("sibling_of_parent: " + str(sibling_of_parent))
        return sibling_of_parent
    # def give_value_n_path(self, id):

    def give_value_n_path(self, id):
        value = self.data[id]
        path = []
        id = id * 2
        path += [self.tree[self.find_sibling_id(id)]]
        while id < len(self.data) * 4 - 4:
            # print("id: " + str(id))
            sibling_of_parent = self.find_sibling_of_parent_id(id)
            # print("sibling_of_parent " + str(sibling_of_parent))
            path += [self.tree[sibling_of_parent]]
            id = sibling_of_parent
            # print("id: " + str(id) + " < " + " data * 4 - 4: " +
            #   	str(len(self.data) * 4 - 4))
        path += [self.give_root()]
        return value, path

    def parent_hash(self, id, value, sibling):
        parent_value = []
        if int(id) % 2 == 0:
            parent_value = hash_string(str(value) + str(sibling))
            # print("iamtherigt: " + str(id % 2 == 0))
        else:
            # print("iamin: " + str(id % 2 == 0))
            parent_value = hash_string(str(sibling) + str(value))
        """
        print("id. " + str(id) + "mod2: " + str(id % 2))
        print("value:" + str(value))
        print("sibling:" + str(sibling))
        print("even: " + str([hash_string(str(value) + str(sibling))]))
        print("uneven: " + str(hash_string(str(sibling) + str(value))))
        print("took: " + parent_value)
        """
        return parent_value

    def verify_proof(self, root, id, value, path, data_size):
        id = id * 2
        value = value
        sibling = path[0]
        # print("verify proof0: id, value, sibling: " + str(id) + ", " + str(value) + ", " + str(sibling))
        value = self.parent_hash(id, value, sibling)
        # print("parent_hash: " + str(value))
        for i in range(1, len(path) - 1):
            sibling = path[i]
            id = int(max(id, self.find_sibling_id(id))/2) + data_size * 2
            # print("verify proof0: id, value, sibling: " + str(id) + ", " + str(value) + ", " + str(sibling))
            value = self.parent_hash(id, value, sibling)
            # print("parent_hash: " + str(value))
        return value == root


treesize = 4
tree = merkle_tree([1, 2, 3, 4])
# print(tree.find_sibling_id(9))

for i in range(0, treesize):
    id = i
    value = tree.give_value_n_path(id)[0]
    path = tree.give_value_n_path(id)[1]
    root = tree.give_root()
    data_size = len(tree.data)
    # print("id, value, root" + str(id) + ", " + str(value) + ", " + str(root))
    print(i)
    print(str(tree.verify_proof(root, id, value, path, data_size)))
