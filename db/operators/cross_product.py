from typing import Generator, List

from db.page import Page
from db.relation import Relation

def cross_product(rel1: Relation, rel2: Relation) -> Relation:
    attrs = list()
    attrs.append(rel1.col_names).append(rel2.col_names)
    return Relation(attrs, _pages(rel1, rel2))

def _pages(rel1, rel2) -> Generator:
    for p1 in rel1:
        out_page = Page()
        for r1 in p1:
            for p2 in rel2:
                for r2 in p2:
                    new_row = list()
                    new_row.append(r1)
                    new_row.append(r2)
                    out_page.append(new_row)
        yield out_page
