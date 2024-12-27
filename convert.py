#!/usr/bin/env python3
import argparse
from pathlib import Path
from xstation_parser import Template

parser = argparse.ArgumentParser(
    prog='x-station-sheet',
    description='Converts from Novation X-station Sysex to Excel files and back',
)

parser.add_argument('command', choices=['xlsx', 'syx', 'json'])
parser.add_argument('filename')
parser.add_argument("--output", help="output")
args = parser.parse_args()

path = Path(args.filename).absolute()

if args.command == 'xlsx':
    if path.suffix != '.syx':
        raise Exception('expecting a \'*.syx\' file as input')
    output = args.output if args.output else path.with_suffix('.xlsx')
    template = Template.from_sysex(path)
    template.to_spreadsheet(output)
elif args.command == 'syx':
    if path.suffix != '.xlsx':
        raise Exception('expecting a \'*.xlsx\' file as input')
    output = args.output if args.output else path.with_suffix('.syx')
    template = Template.from_spreadsheet(path)
    template.to_sysex(output)
elif args.command == 'json':
    if path.suffix != '.xlsx':
        raise Exception('expecting a \'*.xlsx\' file as input')
    output = args.output if args.output else path.with_suffix('.json')
    template = Template.from_spreadsheet(path)
    template.to_json(output)
else:
    raise Exception('unknown command')
