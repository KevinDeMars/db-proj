from enum import Enum
from typing import *
from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self):
        self.keys: List = list()
        self.pointers: List = list()

    @abstractmethod
    def copy(self) -> 'Node':
        pass

    #def __repr__(self):
    #    return ', '.join([f'{k}->{v}' for k, v in zip(self.keys, self.pointers)])

    def __repr__(self):
        return '#' + str(id(self))[-3:]

class InternalNode(Node):
    pointers: List[Node]

    def copy(self) -> 'InternalNode':
        n = InternalNode()
        n.pointers = self.pointers[:]
        n.keys = self.keys[:]
        return n

    def follow_child(self, key: int):
        for i, Ki in enumerate(self.keys):
            if Ki == key:
                return self.pointers[i + 1]
            elif Ki > key:
                return self.pointers[i]
        # Return last non-null pointer
        return self.pointers[-1]

    def insert(self, node_to_insert_after: Node, key, pointer: Node):
        for i, ptr in enumerate(self.pointers):
            if ptr is node_to_insert_after:
                self.keys.insert(i, key)
                self.pointers.insert(i+1, pointer)
                return
        raise Exception("Ooops")


class LeafNode(Node):
    pointers: List[List[Any]]

    def __init__(self):
        super().__init__()
        self.next: Optional[LeafNode] = None

    def copy(self) -> 'LeafNode':
        n = LeafNode()
        n.pointers = self.pointers[:]
        n.keys = self.keys[:]
        n.next = self.next
        return n

    def insert_index(self, key) -> int:
        for i, Ki in enumerate(self.keys):
            if key <= Ki:
                return i
        return len(self.keys)

    def insert(self, key, val, dest_idx=None):
        if dest_idx is None:
            dest_idx = self.insert_index(key)

        if self.has_key(key, dest_idx):
            # if already have bucket with key, add to that bucket
            self.pointers[dest_idx].append(val)
        else:
            '''
            # expand list
            old_len = len(self.keys)
            self.keys.append(None)
            self.pointers.append(list())
            # Shift over everything from dest_idx to the right
            for i in range(old_len, dest_idx, -1):
                self.keys[i] = self.keys[i - 1]
                self.pointers[i] = self.pointers[i - 1]
            self.keys[dest_idx] = key
            self.pointers[dest_idx] = [val]
            '''
            self.keys.insert(dest_idx, key)
            self.pointers.insert(dest_idx, [val])

    def has_key(self, key, hint: int = None) -> bool:
        if hint is None:
            hint = self.insert_index(key)
        return hint < len(self.keys) and self.keys[hint] == key