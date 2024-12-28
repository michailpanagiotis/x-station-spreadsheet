#!/usr/bin/env python3
import argparse
from pathlib import Path
from xstation_parser import Template
from shutil import copyfile

parser = argparse.ArgumentParser(
    prog='x-station-sheet',
    description='Converts from Novation X-station Sysex to Excel files and back',
)

parser.add_argument('command', choices=['xlsx', 'syx', 'json'])
parser.add_argument('filename')
parser.add_argument("--output", help="output")
args = parser.parse_args()

path = Path(args.filename).absolute()
extension = path.suffix

if extension == ".%s" % args.command:
    if args.output:
        output = Path(args.output).absolute()
        if path != output:
            print('copying %s to %s' % (path, args.output))
            copyfile(path, args.output)
elif args.command == 'xlsx':
    if extension != '.syx':
        raise Exception('expecting a \'*.syx\' file as input')
    output = args.output if args.output else path.with_suffix('.xlsx')
    template = Template.from_sysex(path)
    template.to_spreadsheet(output)
elif args.command == 'syx':
    if extension != '.xlsx':
        raise Exception('expecting a \'*.xlsx\' file as input')
    output = args.output if args.output else path.with_suffix('.syx')
    template = Template.from_spreadsheet(path)
    template.to_sysex(output)
elif args.command == 'json':
    if extension != '.xlsx':
        raise Exception('expecting a \'*.xlsx\' file as input')
    output = args.output if args.output else path.with_suffix('.json')
    template = Template.from_spreadsheet(path)
    template.to_json(output)
else:
    raise Exception('unknown command')
