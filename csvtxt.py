#! /usr/bin/env python

import argparse
import csv
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=checkFile, help='csv file to mess with')
    parser.add_argument('-x', action='store_true', help='back to minified')
    args = parser.parse_args()

    with open(args.file, 'rb') as csvfile:
        rows = [row for row in csv.reader(csvfile)]
    cols = max(len(row) for row in rows)
    lens = [0] * cols
    for r in range(len(rows)):
        for c in range(min(cols, len(rows[r]))):
            lens[c] = max(lens[c], len(rows[r][c]))

    newrows = []
    for r in range(len(rows)):
        newrow = []
        for c in range(cols):
            if c >= len(rows[r]):
                value = ""
            else:
                value = rows[r][c]
            newrow.append(value.rstrip() if args.x else value.ljust(lens[c], " "))
        newrows.append(newrow)

    with open(args.file, 'wb') as csvfile:
        csv.writer(csvfile, lineterminator="\n").writerows(newrows)

def checkFile(file):
    if not os.path.exists(file):
        raise ValueError("File does not exist: %s" % file)
    if not os.path.isfile(file):
        raise ValueError("Path is not a file: %s" % file)
    if not (os.access(file, os.W_OK) and os.access(file, os.R_OK)):
        raise ValueError("File is not read/writable: %s" % file)
    return file

if __name__ == "__main__":
    sys.exit(main())
