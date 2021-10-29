from typing import Generator, List

from db.operators.join_predicate import JoinPredicate, AttrEqConstant
from db.page import Page
from db.relation import Relation


def select(rel: Relation, theta: JoinPredicate) -> Relation:
    cols = rel.col_names
    if isinstance(theta, AttrEqConstant):
        pages = _pagesUsingTree(rel, theta)
    else:
        pages = _pagesLinearSearch(rel, theta)
    return Relation(cols, pages)


def _pagesUsingTree(R: Relation, theta: AttrEqConstant):
    tree = R.create_index(theta.attr)
    rows = tree.get(theta.constant)
    yield Page(rows)


def _pagesLinearSearch(R: Relation, theta: JoinPredicate):
    for page in R.pages:
        new_page = Page()
        for row in page.rows:
            if theta.test(R, row):
                new_page.rows.append(row)
        yield new_page