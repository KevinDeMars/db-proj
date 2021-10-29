from typing import List

from db.operators.csv_dump import csv_dump
from db.operators.cross_product import cross_product
from db.operators.project import project
from db.operators.select import select
from db.relation import Relation


def join(r1: Relation, r2: Relation) -> Relation:
    common_attributes = _same_attributes(r1, r2)
    # get cross product and dump intermediate result
    result = csv_dump(
        cross_product(r1, r2),
        "join_" + r1.filename + "_" + r2.filename + ".csv"
    )
    # select where join attrs are equal
    for attr in common_attributes:
        a1 = r1.filename + '.' + attr
        a2 = r2.filename + '.' + attr
        result = select(result, a1, a2)

    # For common attribute A, remove table2.A from result but keep table1.A
    col_names_to_remove = [r2.filename + '.' + col for col in common_attributes]
    col_names = [col for col in result.col_names if col not in col_names_to_remove]
    proj = project(result, col_names)
    return proj


# gets the columns the tables will join on
def _same_attributes(r1, r2) -> List:
    attrs = list()
    for c1 in r1.col_names:
        for c2 in r2.col_names:
            if c1 == c2:
                attrs.append(c1)
    return attrs