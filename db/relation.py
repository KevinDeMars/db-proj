from os import path
from typing import List, Dict, Optional, Generator
import pickle

from db.page import Page
from ds.bptree import BPlusTree


class Relation:
    next_id: int = 0
    relations: Dict[int, 'Relation'] = dict()

    def __init__(self, col_names: List[str], pages: Generator):
        self.id: int = Relation.next_id
        Relation.next_id += 1
        Relation.relations[self.id] = self

        self.col_names = col_names
        self.pages = pages

    def pages(self) -> Generator:
        return self.pages

    def rows(self):
        for pg in self.pages:
            for r in pg.rows:
                yield r

    def create_index(self, attribute: str, filename: str) -> BPlusTree:
        if path.exists(filename):
            return BPlusTree.load(filename)

        tree = BPlusTree()
        atr_idx = self.col_names.index(attribute)
        for r in self.rows():
            tree.insert(r[atr_idx], r)
        tree.save(filename)
        return tree

    @staticmethod
    def by_id(id: int):
        return Relation.relations[id]

    def save(self, fname: str):
        with open(fname, 'wb') as f:
            pickle.dump(self, f)