from abc import ABC
from typing import List

from db.relation import Relation


class JoinPredicate(ABC):
    def test(self, R: Relation, row: List[int]) -> bool:
        pass


class AttrEqAttr(JoinPredicate):
    def __init__(self, attr1: str, attr2: str):
        self.attr1 = attr1
        self.attr2 = attr2

    def test(self, R: Relation, row: List[int]) -> bool:
        idx1 = R.col_names.index(self.attr1)
        idx2 = R.col_names.index(self.attr2)
        return row[idx1] == row[idx2]


class AttrEqConstant(JoinPredicate):
    def __init__(self, attr: str, constant: int):
        self.attr = attr
        self.constant = constant

    def test(self, R: Relation, row: List[int]) -> bool:
        idx = R.col_names.index(self.attr)
        return row[idx] == self.constant
