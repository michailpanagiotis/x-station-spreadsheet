#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path
from xstation_parser import Template

parser = ArgumentParser(
    prog='x-station-sheet',
    description='Converts from Novation X-station Sysex to Excel files and back',
)

parser.add_argument('filename1')
parser.add_argument('filename2')
args = parser.parse_args()

path1 = Path(args.filename1).absolute()
path2 = Path(args.filename2).absolute()

if path1.suffix == '.syx':
    if path2.suffix != ".syx":
        raise Exception("expecting second file to be a '.syx' file")
    template1 = Template.from_sysex(path1)
    template2 = Template.from_sysex(path2)
elif path1.suffix == '.xlsx':
    if path2.suffix != ".xlsx":
        raise Exception("expecting second file to be a '.xlsx' file")
    template1 = Template.from_spreadsheet(path1)
    template2 = Template.from_spreadsheet(path2)
else:
    raise Exception("expecting first file to be a '.syx' or '.xlsx' file")

template1.diff(template2)
