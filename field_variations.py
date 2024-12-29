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
    prog='field_variations',
    description='Lists all variations of a field in a set of .syx templates',
)
parser.add_argument('field')
args = parser.parse_args()

fields = [(filename, control[args.field]) for (filename, template) in filenames for control in template.controls]
variations = {str(field) for _, field in fields}

for variation in variations:
    print(variation)
