from typing import List

from db.operators import csv_scan, project
from db.operators.cross_product import cross_product
from db.operators.select import select
from ds.bptree import BPlusTree


def execute(query: List[str]):
    cmd = query[0].upper()
    if cmd == 'BTREE':
        btree(query[1:])
    elif cmd == 'SELECT':
        # check arg length
        args = query[1:]
        if len(args) < 4:
            print('Usage: project <input_filename> <output_filename> <attribute> <constraint>')
            return
        input_filename, output_filename = args[0], args[1]

        res = select(csv_scan(input_filename), query[3:])

        # TODO write to output file if there is one

        # for testing purposes, print right now
        for r in res.rows():
            print(r)

    elif cmd == 'PROJECT':
        # check arg length
        args = query[1:]
        if len(args) < 1:
            print('Usage: project <input_filename> optional: <output_filename> <attributes>')
            return

        if len(args) == 1:
            # TODO return whole row
            pass
        else:
            # TODO check for output file
            # get attributes
            filename, attributes = args[0], args[1:]

            # call project operator
            result = project(csv_scan(filename), attributes)

            # TODO write to output file if there is one

            # for testing purposes, print right now
            for r in result.rows():
                print(r)

    elif cmd == 'CROSS':
        # check arg length
        args = query[1:]

        # check for all three params
        if len(args) < 3:
            print('Usage: cross <input1_filename> <input2_filename> <output_file>')
            return

        input1_filename, input2_filename = args[0], args[1]

        result = cross_product(csv_scan(input1_filename), csv_scan(input2_filename))

        # TODO write to output file

        # for testing purposes, print right now
        for r in result.rows():
            print(r)

    elif cmd == 'JOIN':
        # TODO
        pass
    # For testing
    elif cmd == 'CREATE_INDEX':
        create_index(query[1:])
    else:
        print('Invalid operator: ' + cmd)


def btree(args: List[str]):
    if len(args) != 1:
        print('Usage: btree <filename.btree>')
        return
    BPlusTree.load(args[0]).print()

def create_index(args: List[str]):
    if len(args) != 2:
        print('Usage: make_btree <filename> <attribute>')
        return
    filename, attribute = args[0], args[1]
    R = csv_scan(filename)
    R.create_index(attribute, filename + '.' + attribute + '.btree')
