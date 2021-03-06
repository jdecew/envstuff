#! /usr/bin/env python

import argparse
import csv
import os
import sys

#SPACE_CHAR = "\xB7" # dot
SPACE_CHAR = "\x97" # wide dash

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='file', nargs='+', type=checkFile, help='csv file to mess with')
    parser.add_argument('-x', action='store_true', help='back to minified')
    args = parser.parse_args()

    for file in args.files:
        process_csv(file, args.x)

def process_csv(file, minify):
    with open(file, 'rbU') as csvfile:
        rows = [row for row in csv.reader(csvfile)]
    cols = max(len(row) for row in rows)
    lens = [0] * cols
    for r in range(len(rows)):
        for c in range(min(cols, len(rows[r]))):
            lens[c] = max(lens[c], cell_len(rows[r][c]))

    newrows = []
    for r in range(len(rows)):
        newrow = []
        for c in range(cols):
            if c >= len(rows[r]):
                value = ""
            else:
                value = rows[r][c].rstrip(SPACE_CHAR)
            newrow.append(cell_clean(value) if minify else value.ljust(lens[c] - cell_quotes(value), SPACE_CHAR))
        newrows.append(newrow)

    with open(file, 'wb') as csvfile:
        csv.writer(csvfile, lineterminator="\n").writerows(newrows)

def cell_clean(text):
    return text.rstrip(SPACE_CHAR)

def cell_quotes(text):
    quotes = 0
    if ',' in text:
        quotes = 2
    if '"' in text:
        quotes = 2
        quotes += text.count('"')
    return quotes

def cell_len(text):
    return len(cell_clean(text)) + cell_quotes(text)


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
