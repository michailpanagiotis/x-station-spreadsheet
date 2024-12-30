#!/usr/bin/env python3
import os.path
import argparse
from pathlib import Path
from xstation_parser import Template
filenames = []
for root,_,files in os.walk('.'):
    for file in [Path(os.path.join(root, x)).absolute() for x in files]:
        if file.suffix == '.syx':
            template = Template.from_sysex(file)
            filenames.append([file, template])

parser = argparse.ArgumentParser(
    prog='control_variations',
    description='Lists all variations of a control in a set of .syx templates',
)
parser.add_argument('field_index', type=int)
args = parser.parse_args()
field_index = args.field_index

headers = [(filename, template.header_fields[field_index]) for (filename, template) in filenames]

index = field_index + 99
name = next((header.name for _, header in headers))

variations = list({'%s' % (str(header)) for _, header in headers})

variations.sort(key=lambda x: int(x))

for variation in variations:
    print('%s,' % variation)
    # print('%s: %s %s' % (index, name, variation))
    for filename, template in filenames:
        if (str(template.header_fields[field_index]) == variation):
            print('\t', str(filename))
