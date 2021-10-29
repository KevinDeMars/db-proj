from typing import List

from db.operators import csv_scan, project, csv_dump
from db.operators.cross_product import cross_product
from db.operators.join import join
from db.operators.join_predicate import AttrEqConstant, AttrEqAttr
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
            print('Usage: project <input_filename> <output_filename> <attribute> <constant or other attribute>')
            return

        # get the file names
        input_filename, output_filename = args[0], args[1]
        attr1 = args[2]
        attr_or_const = args[3]

        if attr_or_const.isnumeric():
            theta = AttrEqConstant(attr1, int(attr_or_const))
        else:
            theta = AttrEqAttr(attr1, attr_or_const)

        # select the requested attribute
        res = csv_dump(
            select(csv_scan(input_filename), theta),
            output_filename
        )

        # for testing purposes, print right now
        for r in res.rows():
            print(r)

    elif cmd == 'PROJECT':
        # check arg length
        args = query[1:]
        if len(args) < 2:
            print('Usage: project <input_filename> optional: <output_filename> <attributes>')
            return

        input_file, output_file = args[0], args[1]
        attributes = args[2:]
        result = csv_dump(
            project(csv_scan(input_file), attributes),
            output_file
        )

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

        # the file names
        in1, in2, out = args[0], args[1], args[2]

        # get the cross product of the two relations
        result = csv_dump(
            cross_product(csv_scan(in1), csv_scan(in2), in1, in2),
            out
        )

        # for testing purposes, print right now
        print(result.col_names)
        for r in result.rows():
            print(r)

    elif cmd == 'JOIN':
        # check arg length
        args = query[1:]

        # check for all three params
        if len(args) < 3:
            print('Usage: join <input1_filename> <input2_filename> <output_file>')
            return

        # the file names
        in1, in2, out = args[0], args[1], args[2]

        # get the cross product of the two relations
        result = csv_dump(
            join(csv_scan(in1), csv_scan(in2), in1, in2),
            out
        )

        # for testing purposes, print right now
        print(result.col_names)
        for r in result.rows():
            print(r)
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
    R.create_index(attribute)
