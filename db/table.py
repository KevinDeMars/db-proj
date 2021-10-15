from typing import List, Dict


class Table:
    next_id: int = 0
    tables: Dict[int, 'Table'] = dict()

    def __init__(self, fname: str):
        self.id: int = Table.next_id
        Table.next_id += 1
        Table.tables[self.id] = self

        self.file_name: str = fname
        with open(fname, 'r') as f:
            header = f.readline()
        self.column_names: List[str] = header.split(',')

    @staticmethod
    def by_id(id: int):
        return Table.tables[id]