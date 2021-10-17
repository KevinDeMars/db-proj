from typing import Generator, List

from ..page import Page
from ..relation import Relation


def csv_scan(filename: str) -> Relation:
    with open(filename, 'r') as f:
        col_names = f.readline().split(',')
    return Relation(col_names, _pages(filename, col_names))


def _pages(filename, col_names) -> Generator:
    with open(filename) as f:
        yield Page([parse_line(line, col_names) for line in f.readlines()[1:]])


def parse_line(line: str, col_names) -> List[int]:
    split = line.split(',')
    if len(split) != len(col_names):
        raise Exception("Bad line: " + line)
    return [int(x) for x in split]
