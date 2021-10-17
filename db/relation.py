from typing import List, Dict, Optional, Generator

from db.page import Page


class Relation:
    next_id: int = 0
    relations: Dict[int, 'Relation'] = dict()

    def __init__(self, col_names: List[str], pages: Generator):
        self.id: int = Relation.next_id
        Relation.next_id += 1
        Relation.relations[self.id] = self

        self.col_names = col_names
        self.pages = pages

    def pages(self) -> Generator:
        return self.pages

    def rows(self):
        for pg in self.pages:
            for r in pg.rows:
                yield r

    @staticmethod
    def by_id(id: int):
        return Relation.relations[id]