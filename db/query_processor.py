from typing import List

from db.operators.cross_product import cross_product
from db.operators.csv_dump import csv_dump
from db.operators.csv_scan import csv_scan
from db.operators.join import join
from db.operators.project import project
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
            print('Usage: select <input_filename> <output_filename> <attribute> <constraint (attribute or constant)>')
            return

        # get the file names
        input_filename, output_filename = args[0], args[1]
        attr = args[2]
        constraint = args[3]
        # Convert constraint to int if it looks like an int
        if constraint.isnumeric():
            constraint = int(constraint)
        # select the requested attribute
        csv_dump(
            select(csv_scan(input_filename), attr, constraint),
            output_filename
        ).print()

    elif cmd == 'PROJECT':
        # check arg length
        args = query[1:]
        if len(args) < 2:
            print('Usage: project <input_filename> optional: <output_filename> <attributes>')
            return

        input_file, output_file = args[0], args[1]
        attributes = args[2:]
        csv_dump(
            project(csv_scan(input_file), attributes),
            output_file
        ).print()

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
        csv_dump(
            cross_product(csv_scan(in1), csv_scan(in2)),
            out
        ).print()

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
        csv_dump(
            join(csv_scan(in1), csv_scan(in2)),
            out
        ).print()
    else:
        print('Invalid operator: ' + cmd)


def btree(args: List[str]):
    if len(args) != 1:
        print('Usage: btree <filename.btree>')
        return
    BPlusTree.load(args[0]).print()