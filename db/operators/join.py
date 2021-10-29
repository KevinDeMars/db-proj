import pickle

from typing import Generator, List

from db.operators import csv_scan
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

def _pages(r1, r2, attrs, f1, f2) -> Generator:
    print("entering")
    # get cross product
    rel = cross_product(r1, r2, f1[:-3], f2[:-3])
    print(rel.col_names)
    # TODO store cross in a file
    fname = "cross_temp.csv"
    #rel.save(fname)
    # select where join attrs are equal
    for attr in attrs:
        a = list()
        a.append(str(f1[:-3] + attr))
        a.append(str(f2[:-3] + attr))
        rel = select(rel,a,fname)
        #sel.save(fname)

    for r in rel.rows():
       print(r)
    # TODO store intermediate results of each select in file
    #TODO use project once to get rid of duplicate cols between f1 and f2
    proj = project(rel, [])
    for p in proj.pages:
        yield p
