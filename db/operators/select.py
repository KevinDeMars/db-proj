from typing import Generator, Union

from db.page import Page
from db.relation import Relation


def select(rel: Relation, a1: str, a2: Union[str, int]) -> Relation:
    return Relation(rel.col_names, _pages(rel, a1, a2))


def get_index(col_names, attr):
    # get the index of the attribute
    idx = 0
    for c in col_names:
        if c == attr:
            return idx
        idx = idx + 1
    return -1


def _pages(rel, a1: str, a2: Union[str, int]) -> Generator:
    if isinstance(a2, int):
        # create b+ tree implementation
        tree = rel.create_index(a1)
        out_page = Page()
        # get rows in range
        rows = tree.get(a2)
        for row in rows:
            out_page.rows.append(row)
        yield out_page
    else:
        # comparing to other attribute
        a_idx = get_index(rel.col_names, a1)
        c_idx = get_index(rel.col_names, a2)
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
