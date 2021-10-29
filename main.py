import sys

from db import query_processor


def main():
    if len(sys.argv) == 1:
        query = input('Query: ').split(' ')
    else:
        query = sys.argv[1:]
    query_processor.execute(query)

if __name__ == '__main__':
    main()
