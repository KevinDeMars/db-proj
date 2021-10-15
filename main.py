from db.operators import *


def main():
    it = CsvScan(Table("my_table.csv"))
    for row in it.rows():
        print(row)


if __name__ == '__main__':
    main()
