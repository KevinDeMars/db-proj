from typing import Generator, List

from db.page import Page
from db.relation import Relation


def select(rel: Relation, attrs: List[str], filename: str) -> Relation:
    cols = rel.col_names
    cols[-1] = cols[-1].split()
    return Relation(cols, _pages(rel, attrs, filename))

def get_attr_index(col_names, attr):
    # get the index of the attribute
    idx = 0
    for c in col_names:
        if c == attr:
            return idx
        idx = idx + 1
    return -1

def get_constraint_index(col_names, constr):
    # get the index of the constraint variable
    idx = 0
    for c in col_names:
        if c == constr:
            return idx
        idx = idx + 1
    return -1

def _pages(rel, attrs: List[str], filename) -> Generator:
    if attrs[1].isdigit():
        # create b+ tree implementation
        tree = rel.create_index(attrs[0], filename + '.' + attrs[0] + '.btree')
        out_page = Page()
        # get rows in range
        rows = tree.get(int(attrs[1]))
        for row in rows:
            out_page.rows.append(row)
        yield out_page
    else:
        # comparing to other attribute
        a_idx = get_attr_index(rel.col_names, attrs[0])
        c_idx = get_constraint_index(rel.col_names, attrs[1])
        if a_idx == -1 or c_idx == -1:
            # TODO finish error situation
            print("ERROR: attribute or constraint name not in table")
            return
        for p in rel.pages:
            out_page = Page()
            for r in p.rows:
                if r[a_idx] == r[c_idx]:
                    out_page.rows.append(r)
            yield out_page
