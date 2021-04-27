#!/usr/bin/env python3

from .classes import FileSet
from .exceptions import ConfigError
import argparse
import os
import sys


def parse_args():
    ''' Parse command line arguments '''

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
        help='Output directory (if exists, must be empty)', 
        action='store'
        )

    parser.add_argument(
        '-d', '--dryrun', 
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


def check_args(args):
    ''' Validate the provided arguments '''

    if not os.path.isdir(args.source):
        raise ConfigError("Source directory not found")

    if os.path.isdir(args.destination) and len(os.listdir(args.destination)) > 0:
        raise ConfigError("Destination directory is not empty")


def main():

    try:
        """ (1) Parse args """
        args = parse_args()

        """ (2) Validate the provided arguments """
        check_args(args)

        """ (3) Create FileSet """
        fileset = FileSet.from_filesystem(args.source)

        """ (4) Create partition map """
        pattern = r"^([a-z]+?)-(\d+?)-\d+?\.\w+?$"
        #fileset.partition_by(pattern)

        """ (5) Move, copy, or print """
        if args.dryrun:
            print("Displaying map but not moving files...")
        elif args.copy:
            print("Copying files to desination and leaving originals in place...")
        else:
            print("Moving files to new location...")

        """ (6) Summarize results """
        print("Summarizing what happened")

    except Exception as msg:
        print(f"ERROR: {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
