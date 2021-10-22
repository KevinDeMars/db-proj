import sys

from db import query_processor
from db.operators import *


def main():
    if len(sys.argv) == 1:
        query = input('Query: ').split(' ')
    else:
        query = sys.argv[1:]
    res = query_processor.execute(query)
    for r in res.rows():
        print(r)

if __name__ == '__main__':
    main()
