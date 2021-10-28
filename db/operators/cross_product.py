from typing import Generator, List

from db.page import Page
from db.relation import Relation

# get the cross product of two relations
def cross_product(rel1: Relation, rel2: Relation) -> Relation:
    return Relation(_column_names(rel1, rel2), _pages(rel1, rel2))

# get the crossed column names prefixed by relation name
def _column_names(rel1, rel2):
    # get the relation column names
    r1 = rel1.col_names
    r1[-1] = r1[-1].strip()
    # prefix the column names
    idx = 0
    for i in r1:
        r1[idx] = "r1." + i
        idx = idx + 1
    # get the relation column names
    r2 = rel2.col_names
    r2[-1] = r2[-1].strip()
    # prefix the column names
    idx = 0
    for i in r2:
        r2[idx] = "r2." + i
        idx = idx + 1
    attrs = r1 + r2
    return attrs

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
