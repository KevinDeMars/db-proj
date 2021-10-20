import pickle
from typing import Optional, TypeVar, Generic, List

from .bptreenode import Node, LeafNode, InternalNode

K = TypeVar("K")
V = TypeVar("V")


class BPlusTree(Generic[K, V]):
    def __init__(self, n: int = 100):
        self.n = n
        self.root: Optional[Node] = None

    def get(self, key: K) -> List[V]:
        n = self._find_node(key)
        if n is None:
            return []
        idx = n.insert_index(key)
        if n.has_key(key, idx):
            return n.pointers[idx]
        return []

    def _find_node(self, key: K) -> Optional[LeafNode]:
        """Gets the node that should return key if it is in this tree"""
        if self.root is None:
            return None
        n = self.root
        while isinstance(n, InternalNode):
            n = n.follow_child(key)
        return n

    def insert(self, key: K, val: V):
        if self.is_empty():
            self.root = LeafNode()
            self.root.pointers = [[val]]
            self.root.keys = [key]
            return
        L = self._find_node(key)
        if L.has_key(key) or len(L.keys) < self.n - 1:
            L.insert(key, val)
        else:
            # L has n-1 keys already, split it
            L2 = LeafNode()
            T = L.copy()
            T.insert(key, val)
            # save pointer to next block
            L2.next = L.next
            L.next = L2
            # erase L.P1 through L.K_n-1 from L
            L.keys.clear()
            L.pointers.clear()
            # copy T.P1 through T.K_n/2 from T into L starting at L.P1
            mid = (self.n + 1) // 2
            L.keys = T.keys[0:mid]
            L.pointers = T.pointers[0:mid]
            # copy T.P_n/2+1 through T.K_n from T into L' starting at L'.P1
            L2.keys = T.keys[mid:]
            L2.pointers = T.pointers[mid:]
            self._insert_in_parent(L, L2.keys[0], L2)

    def _insert_in_parent(self, N: Node, key: K, N2: Node):
        if N is self.root:
            R = InternalNode()
            R.keys = [key]
            R.pointers = [N, N2]
            self.root = R
            return
        P = self._find_parent(N, self.root)
        if len(P.pointers) < self.n:
            P.insert(N, key, N2)  # Insert (firstKey, rightNode) just after leftNode
        else:
            # Split P
            T = P.copy()
            T.insert(N, key, N2)
            P.keys.clear()
            P.pointers.clear()
            P2 = InternalNode()
            mid = self.n // 2 + 1
            P.pointers = T.pointers[0:mid]
            P2.pointers = T.pointers[mid:]
            P.keys = T.keys[0:mid - 1]
            weird_key = T.keys[mid - 1]
            P2.keys = T.keys[mid:]
            self._insert_in_parent(P, weird_key, P2)

    def _find_parent(self, N: Node, subtree) -> Optional[InternalNode]:
        if N is self.root:
            return None
        for child in subtree.pointers:
            if child is N:
                return subtree
        for child in subtree.pointers:
            if isinstance(child, InternalNode):
                x = self._find_parent(N, child)
                if x is not None:
                    return x
        return None

    def is_empty(self):
        return self.root is None

    def print(self, node=None):
        if node is None:
            node = self.root
            print('Root:', node)
        print(node, ':', sep='')
        if isinstance(node, InternalNode):
            for p, k in zip(node.pointers, node.keys):
                print(f'{p}|{k}|', end='')
            print(f'{node.pointers[-1]}')

            for p in node.pointers:
                self.print(p)
        elif isinstance(node, LeafNode):
            for p, k in zip(node.pointers, node.keys):
                # print(f'({len(p)} rows)|{k}')
                print(f'{p}|{k}|', end='')
            print(node.next)
            print()

    @staticmethod
    def load(fname: str) -> 'BPlusTree':
        with open(fname, 'rb') as f:
            return pickle.load(f)

    def save(self, fname: str):
        with open(fname, 'wb') as f:
            pickle.dump(self, f)