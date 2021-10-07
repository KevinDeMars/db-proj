import random

from ds.bptree import BPlusTree
from ds.bptreenode import InternalNode, LeafNode, Node


def check(tree: BPlusTree):
    # Check that all nodes' keys are in increasing order
    check_node_asc(tree.root)
    # Check that first key in left pointer < first key in right pointer
    check_pointers_in_order(tree.root)


def check_node_asc(N: Node):
    for i in range(len(N.keys) - 1):
        assert N.keys[i] < N.keys[i + 1]
    if isinstance(N, InternalNode):
        for child in N.pointers:
            check_node_asc(child)


def check_pointers_in_order(N: Node):
    if isinstance(N, InternalNode):
        for i in range(len(N.pointers) - 1):
            assert N.pointers[i].keys[0] < N.pointers[i + 1].keys[0]
        for child in N.pointers:
            check_pointers_in_order(child)
    elif isinstance(N, LeafNode) and N.next:
        assert N.keys[0] < N.next.keys[0]


nums = [random.randint(0, 1000) for i in range(10000)]
ref_dict = dict()

tree = BPlusTree(100)
for n in nums:
    tree.insert(n, n)
    if n in ref_dict:
        ref_dict[n] += 1
    else:
        ref_dict[n] = 1
    check(tree)

for num, occurrences in ref_dict.items():
    in_tree = tree.get(num)
    assert len(in_tree) == occurrences

tree.print()