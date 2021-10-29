from typing import Generator, List

from db.page import Page
from db.relation import Relation


def project(R: Relation, attrs: List[str]) -> Relation:
    if len(attrs) == 0:
        return R
    else:
        return Relation(attrs, _pages(R, attrs))


def _pages(R, attrs: List[str]) -> Generator:
    for pg in R.pages:
        out_page = Page()

        r: List[int]
        for r in pg.rows:
            new_row = list()
            for i, col_name in enumerate(R.col_names):
                if col_name in attrs:
                    new_row.append(r[i])
            out_page.rows.append(new_row)
        yield out_page
