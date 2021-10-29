from typing import Generator, List

from db.page import Page
from db.relation import Relation

# get the cross product of two relations
def cross_product(rel1: Relation, rel2: Relation) -> Relation:
    # create new column name list
    attrs = _column_names(rel1) + _column_names(rel2)
    # return the cross product relation
    return Relation(attrs, _pages(rel1, rel2))


# get the crossed column names prefixed by relation name
def _column_names(rel):
    return [rel.filename + '.' + col_name for col_name in rel.col_names]

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
