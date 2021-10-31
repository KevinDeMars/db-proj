Run the program with: python main.py
All testing was performed with python 3.9.6.
The query can be provided with command line arguments or from console input after running.

Notes:
- Column names are case-sensitive.
- Output is to both the console (in tabular format) and the specified output file (in csv format).
- The tables used in these examples are provided in the project root.
- On a natural join, if t1 and t2 have columns with the same name X, then t1.X will be retained and t2.X will be removed.
- The b+ tree view is output as follows:
    Pointers to nodes are represented as #XXX, where XXX is the last 3 digits of the memory address of the node.
    Each value in a leaf node is a list of all rows with a matching key.

    Root: #XXX
    for each node:
        #XXX:
        if internal node:
            ptr | key | ptr | ... | ptr
        if leaf node:
            val | key | val | key | ... | ptr

    Full example (with n=4 for readability):
    This is an index on t1.B, so B is the second value in each row.
    Root: #680
    #680:
     #632 | 30 | #488
    #632:
     [[4, 1, -5]] | 1 | [[6, 6, 7]] | 6 | [[1, 10, 20], [7, 10, 99]] | 10 | #488
    #488:
     [[2, 30, 10]] | 30 | [[5, 200, 13]] | 200 | None

Example queries + output:

    Selecting based on two equal columns:
        Query: select t1 out A B
        | A | B | C |
        | 6 | 6 | 7 |

    Selecting based on equalling a constant:
    (the file t1.B.btree should be created.)
        Query: select t1 out B 10
        | A |  B |  C |
        | 1 | 10 | 20 |
        | 7 | 10 | 99 |

    Project (column names given):
        Query: project t1 out A B
        | A |   B |
        | 1 |  10 |
        | 2 |  30 |
        | 4 |   1 |
        | 5 | 200 |
        | 6 |   6 |
        | 7 |  10 |

    Project (all columns):
        Query: project t1 out
        | A |   B |  C |
        | 1 |  10 | 20 |
        | 2 |  30 | 10 |
        | 4 |   1 | -5 |
        | 5 | 200 | 13 |
        | 6 |   6 |  7 |
        | 7 |  10 | 99 |

    Cross product:
        Query: cross t1 t2 out
        | t1.A | t1.B | t1.C | t2.B | t2.D | t2.E |
        |    1 |   10 |   20 |   10 |   -5 |    6 |
        |    1 |   10 |   20 |    1 |    7 |   11 |
        |    1 |   10 |   20 |  200 |  500 | 1000 |
        (more rows omitted)

    Natural join:
        Query: join t1 t2 out
        | t1.A | t1.B | t1.C | t2.D | t2.E |
        |    1 |   10 |   20 |   -5 |    6 |
        |    4 |    1 |   -5 |    7 |   11 |
        |    5 |  200 |   13 |  500 | 1000 |
        |    6 |    6 |    7 |    8 |    7 |
        |    7 |   10 |   99 |   -5 |    6 |

    Manual natural join with cross+select:
        Query: cross t1 t2 out1
        | t1.A | t1.B | t1.C | t2.B | t2.D | t2.E |
        |    1 |   10 |   20 |   10 |   -5 |    6 |
        |    1 |   10 |   20 |    1 |    7 |   11 |
        |    1 |   10 |   20 |  200 |  500 | 1000 |
        |    1 |   10 |   20 |    6 |    8 |    7 |
        (more rows omitted)

        Query: select out1 out2 t1.B t2.B
        | t1.A | t1.B | t1.C | t2.B | t2.D | t2.E |
        |    1 |   10 |   20 |   10 |   -5 |    6 |
        |    4 |    1 |   -5 |    1 |    7 |   11 |
        |    5 |  200 |   13 |  200 |  500 | 1000 |
        |    6 |    6 |    7 |    6 |    8 |    7 |
        |    7 |   10 |   99 |   10 |   -5 |    6 |

    btree view:
        Query: btree t1.B.btree
        Root: #248
        #248:
         [[4, 1, -5]] | 1 | [[6, 6, 7]] | 6 | [[1, 10, 20], [7, 10, 99]] | 10 | [[2, 30, 10]] | 30 | [[5, 200, 13]] | 200 | None