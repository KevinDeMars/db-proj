from typing import List

from db.operators import csv_scan, project, csv_dump
from db.operators.cross_product import cross_product
from db.operators.join import join
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
            print('Usage: project <input_filename> <output_filename> <attribute> <constraint (attribute or constant)>')
            return

        # get the file names
        input_filename, output_filename = args[0], args[1]
        attr = args[2]
        constraint = args[3]
        # Convert constraint to int if it looks like an int
        if constraint.isnumeric():
            constraint = int(constraint)
        # select the requested attribute
        res = csv_dump(
            select(csv_scan(input_filename), attr, constraint),
            output_filename
        )

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
            cross_product(csv_scan(in1), csv_scan(in2)),
            out
        )

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
            join(csv_scan(in1), csv_scan(in2)),
            out
        )

        for r in result.rows():
            print(r)
    else:
        print('Invalid operator: ' + cmd)


def btree(args: List[str]):
    if len(args) != 1:
        print('Usage: btree <filename.btree>')
        return
    BPlusTree.load(args[0]).print()