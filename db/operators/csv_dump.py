from typing import Generator

from db.relation import Relation


def csv_dump(R: Relation, filename: str) -> Relation:
    return Relation(R.col_names, _dump(R, filename))


def _dump(R: Relation, filename: str) -> Generator:
    """Dumps the pages to a file, but also yields the pages back again"""
    with open(filename, 'w') as f:
        f.write(','.join(R.col_names) + '\n')
        for page in R.pages:
            for row in page.rows:
                row = [str(x) for x in row]  # convert to string
                f.write(','.join(row) + '\n')
            yield page