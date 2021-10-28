from typing import Generator, List

from db.page import Page
from db.relation import Relation

# get the cross product of two relations
def cross_product(rel1: Relation, rel2: Relation, fname1: List[str], fname2: str) -> Relation:
    # create new column name list
    attrs = _column_names(rel1, fname1) + _column_names(rel2, fname2)
    # return the cross product relation
    return Relation(attrs, _pages(rel1, rel2))

# get the crossed column names prefixed by relation name
def _column_names(rel, f):
    # get the relation column names
    r = rel.col_names
    r[-1] = r[-1].strip()
    # prefix the column names
    idx = 0
    for i in r:
        r[idx] = f + i
        idx = idx + 1
    # return the prefixed column names
    return r

# get the crossed pages of the two relations
def _pages(rel1, rel2) -> Generator:
    for p1 in rel1.pages:
        for p2 in rel2.pages:
            out_page = Page()
            for r1 in p1.rows:
                for r2 in p2.rows:
                    new_row = r1 + r2
                    out_page.rows.append(new_row)
            yield out_page
