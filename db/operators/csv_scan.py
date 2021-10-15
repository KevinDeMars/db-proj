from typing import Generator, List

from .operator import Operator
from ..page import Page
from ..table import Table


class CsvScan(Operator):
    def __init__(self, table: Table):
        self.table = table

    def pages(self) -> Generator:
        with open(self.table.file_name) as f:
            yield Page(self.table.id, [self.parse_line(line) for line in f.readlines()[1:]])

    def parse_line(self, line: str) -> List[int]:
        split = line.split(',')
        if len(split) != len(self.table.column_names):
            raise Exception("Bad line: " + line)
        return [int(x) for x in split]