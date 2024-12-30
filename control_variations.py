#!/usr/bin/env python3
import os.path
import argparse
from pathlib import Path
from xstation_parser import Template
filenames = []
for root,_,files in os.walk('./'):
    for file in [Path(os.path.join(root, x)).absolute() for x in files]:
        if file.suffix == '.syx':
            print(file)
            template = Template.from_sysex(file)
            filenames.append([file, template])

parser = argparse.ArgumentParser(
    prog='control_variations',
    description='Lists all variations of a control in a set of .syx templates',
)
parser.add_argument('control_index', type=int)
args = parser.parse_args()

controls = [(filename, template.controls[args.control_index]) for (filename, template) in filenames]
variations = {str(control) for _, control in controls}

for variation in variations:
    print(variation)
    for filename, template in filenames:
        if (str(template.controls[args.control_index]) == variation):
            print('\t', filename)
