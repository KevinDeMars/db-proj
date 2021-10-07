from typing import Generator

from db.buffer_manager import BufferManager
from db.operator import Operator
from db.page import Page


class TableScan(Operator):
    def __init__(self, file):
        self.file = file

    def pages(self) -> Generator:
        bm = BufferManager.instance()
        with bm.pin(self.file) as x:
            print(x)
