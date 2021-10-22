from typing import Generator

from db.page import Page
from db.relation import Relation

def cross_product(rel1: Relation, rel2: Relation) -> Relation:
    r1 = rel1.col_names
    r1[-1] = r1[-1].strip()
    r2 = rel2.col_names
    r2[-1] = r2[-1].strip()
    attrs = r1 + r2
    return Relation(attrs, _pages(rel1, rel2))

def _pages(rel1, rel2) -> Generator:
    for p1 in rel1.pages:
        for p2 in rel2.pages:
            out_page = Page()
            for r1 in p1.rows:
                for r2 in p2.rows:
                    new_row = r1 + r2
                    out_page.rows.append(new_row)
            yield out_page
