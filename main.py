from db.operators import *


def main():
    relation = project(csv_scan('my_table.csv'), ['D'])
    for r in relation.rows():
        print(r)

if __name__ == '__main__':
    main()
