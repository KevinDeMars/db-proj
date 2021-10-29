from os import path
from typing import List, Dict, Optional, Generator

from ds.bptree import BPlusTree


class Relation:
    next_id: int = 0
    relations: Dict[int, 'Relation'] = dict()

    def __init__(self, col_names: List[str], pages: Generator, filename: Optional[str] = None):
        self.id: int = Relation.next_id
        Relation.next_id += 1
        Relation.relations[self.id] = self

        self.col_names = col_names
        self.pages = pages

        if filename is not None:
            self.filename = filename
        else:
            self.filename = 'TEMP_' + str(id(self))

    def rows(self):
        for pg in self.pages:
            for r in pg.rows:
                yield r

    def create_index(self, attribute: str) -> BPlusTree:
        tree_filename = self.filename + '.' + attribute + '.btree'
        if path.exists(tree_filename):
            return BPlusTree.load(tree_filename)

        tree = BPlusTree()
        atr_idx = self.col_names.index(attribute)
        for r in self.rows():
            tree.insert(r[atr_idx], r)
        tree.save(tree_filename)
        return tree

    def print(self):
        output_lines: List[List[str]] = list()
        # header row
        output_lines.append(self.col_names)
        # Print each row
        for row in self.rows():
            row = [str(x) for x in row]  # convert ints to strs
            output_lines.append(row)
        num_cols = len(output_lines[0])
        num_rows = len(output_lines)
        col_lengths = list()
        for col in range(num_cols):
            max_len = max(
                [len(output_lines[row][col]) for row in range(num_rows)]
            )
            col_lengths.append(max_len)

        for line in output_lines:
            print('| ', end='')
            for i, col_str in enumerate(line):
                width = col_lengths[i]
                print(f' {col_str:>{width}} |', end='')
            print()

    @staticmethod
    def by_id(id: int):
        return Relation.relations[id]