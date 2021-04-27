from collections import namedtuple, UserDict
import csv
import os
import re


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

    def __repr__(self):
        return f"<FileSet containing {len(self)} assets, {self.bytes} bytes>"

    def partition_by(self, pattern):
        for asset in self.values():
            m = re.match(pattern, asset.filename)
            if m:
                print(m.group(1), m.group(2), asset)
            else:
                print("No match", asset)


