#!/usr/bin/env python3

import argparse
from collections import namedtuple
from collections import UserDict
import csv
import os
import re
import sys


Asset = namedtuple('Asset', 'filename md5 bytes')


class FileSet(UserDict):

    def __init__(self, data):
        super().__init__(data)

    @classmethod
    def from_csv(cls, csvfile):
        data = dict()
        with open(csvfile) as handle:
            for row in csv.DictReader(handle):
                data[row['PATH']] = Asset(row['FILENAME'], row['MD5'], int(row['BYTES']))
        return cls(data)

    @classmethod
    def from_filesystem(cls, root):
        data = dict()
        for directory, subdirs, files in os.walk(root):
            for filename in files:
                filepath = os.path.join(directory, filename)
                if filepath in data:
                    raise Exception
                bytes = os.path.getsize(filepath)
                asset = Asset(filename, None, bytes)
                data[filepath] = asset
        return cls(data)

    @property
    def bytes(self):
        return sum([asset.bytes for asset in self.data.values()])


def partition(fileset):
    pattern = r"^([a-z]+?)-(\d+?)-\d+?\.\w+?$"
    for asset in fileset.values():
        m = re.match(pattern, asset.filename)
        if m:
            print(m.group(1), m.group(2), asset)
        else:
            print("No match", asset)


def main():
    '''Parse args and run the partitioner with those options.'''

    parser = argparse.ArgumentParser(
        description='Partition a tree of files based on various schemes'
        )
    parser.add_argument(
        '-v', '--version', 
        action='version', 
        help='Print version number and exit',
        version='%(prog)s 0.1'
        )
    parser.add_argument(
        '-s', '--source', 
        help='Root of files to be partitioned', 
        action='store',
        required=True
        )
    parser.add_argument(
        '-d', '--destination', 
        help='Destination for partitioned files', 
        action='store',
        required=True
        )
    parser.add_argument(
        '-c', '--copy', 
        help='Copy files, leaving originals in place', 
        action='store_true'
        )

    args = parser.parse_args()
    print(args)
    source = args.source
    if os.path.isfile(source):
        fileset = FileSet.from_csv(source)
    elif os.path.isdir(source):
        fileset = FileSet.from_filesystem(source)
    print(f"Fileset with {len(fileset)} assets, {fileset.bytes} bytes")
    partition(fileset)


if __name__ == "__main__":
    main()
