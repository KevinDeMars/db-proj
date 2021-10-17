from typing import List


class Page:
    def __init__(self, rows: List[List[int]] = None):
        if rows is not None:
            self.rows = rows
        else:
            self.rows = list()