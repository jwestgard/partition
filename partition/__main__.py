#!/usr/bin/env python3

from .classes import FileSet
import argparse


def parse_args():
    '''Parse command line arguments'''

    parser = argparse.ArgumentParser(
        description='Partition a tree of files based on various schemes'
        )

    parser.add_argument(
        'source', 
        help='Root directory to be partitioned', 
        action='store'
        )

    parser.add_argument(
        'destination', 
        help='Output directory (cannot exist)', 
        action='store'
        )

    parser.add_argument(
        '-d', '--dry-run', 
        help='Display resulting layout without moving files', 
        action='store_true',
        )

    parser.add_argument(
        '-c', '--copy', 
        help='Copy files, leaving originals in place', 
        action='store_true'
        )

    parser.add_argument(
        '-v', '--version', 
        action='version', 
        help='Print version number and exit',
        version='%(prog)s 0.1'
        )

    return parser.parse_args()


def main():
    args = parse_args()
    fileset = FileSet.from_filesystem(args.source)
    print(fileset)
    pattern = r"^([a-z]+?)-(\d+?)-\d+?\.\w+?$"
    fileset.partition_by(pattern)


if __name__ == "__main__":
    main()
