from typing import Generator

from db.page import Page

class Operator:

    def pages(self) -> Generator:
        pass

    def rows(self):
        for pg in self.pages():
            for r in pg.rows():
                yield r
