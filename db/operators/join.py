import pickle

from typing import Generator, List

from db.operators import csv_scan
from db.operators.join_predicate import AttrEqAttr
from db.operators.project import project
from db.operators.select import select
from db.operators.cross_product import cross_product
from db.page import Page
from db.relation import Relation

def join(r1: Relation, r2: Relation, f1: str, f2: str) -> Relation:
    attrs = _same_attributes(r1, r2)
    return Relation(attrs, _pages(r1, r2, attrs, f1, f2))

# gets the columns the tables will join on
def _same_attributes(r1, r2) -> List:
    attrs = list()
    for c1 in r1.col_names:
        for c2 in r2.col_names:
            if c1 == c2:
                attrs.append(c1)
    return attrs

def _pages(r1, r2, join_attrs, f1, f2) -> Generator:
    print("entering")
    # get cross product
    rel = cross_product(r1, r2, f1, f2)
    print(rel.col_names)
    # select where join attrs are equal
    for attr in join_attrs:
        a1 = f1 + '.' + attr
        a2 = f2 + '.' + attr
        rel = select(rel, AttrEqAttr(a1, a2))

    for r in rel.rows():
       print(r)
    # TODO store intermediate results of each select in file
    #TODO use project once to get rid of duplicate cols between f1 and f2
    proj = project(rel, [])
    for p in proj.pages:
        yield p
