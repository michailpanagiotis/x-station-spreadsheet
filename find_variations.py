#!/usr/bin/env python3

import os.path
import argparse
from pathlib import Path
from xstation_parser import Template
filenames = []
for root,_,files in os.walk('./additional_templates'):
    for file in [Path(os.path.join(root, x)).absolute() for x in files]:
        if file.suffix == '.syx':
            template = Template.from_sysex(file)
            filenames.append([file, template])

parser = argparse.ArgumentParser(
    prog='variations',
    description='Lists all variations of a field in a set of .syx templates',
)
parser.add_argument('field')
parser.add_argument('value')
args = parser.parse_args()

for filename, template in filenames:
    matches = [control for control in template.controls if str(control[args.field]) == args.value]
    if len(matches) > 0:
        print(filename)
        for match in matches:
            print('\t', match.name)
