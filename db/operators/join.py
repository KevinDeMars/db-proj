from typing import Generator, List

from db.page import Page
from db.relation import Relation

def join(r1: Relation, r2: Relation) -> Relation:
    attrs = _attributes(r1, r2)
    return Relation(attrs, _pages(r1, r2, attrs))

def _attributes(r1, r2) -> List:
    attrs = list()
    for c1 in r1.col_names:
        for c2 in r2.col_names:
            if c1 == c2:
                attrs.append(c1)
    return attrs


def _pages(r1, r2) -> Generator:
    pass
