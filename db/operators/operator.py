from abc import ABC, abstractmethod
from typing import Generator

from db.page import Page


class Operator(ABC):
    @abstractmethod
    def pages(self) -> Generator:
        pass

    def rows(self):
        for pg in self.pages():
            for r in pg.rows:
                yield r
