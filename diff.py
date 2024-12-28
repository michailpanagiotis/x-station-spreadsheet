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

if path1.suffix != ".syx":
    raise Exception("expecting first file to be a '.syx' file")

if path2.suffix != ".syx":
    raise Exception("expecting second file to be a '.syx' file")

template1 = Template.from_sysex(path1)
template2 = Template.from_sysex(path2)

template1.diff(template2)
