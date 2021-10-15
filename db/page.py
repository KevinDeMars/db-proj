from typing import List


class Page:
    def __init__(self, table_id: int, rows: List[List[int]]):
        self.table_id = table_id
        self.rows = rows