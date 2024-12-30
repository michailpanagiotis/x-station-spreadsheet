#!/usr/bin/env python3
import os.path
import argparse
from pathlib import Path
from xstation_parser import Template

parser = argparse.ArgumentParser(
    prog='control_variations',
    description='Lists all variations of a control in a set of .syx templates',
)
parser.add_argument('directory')
parser.add_argument('field_index', type=int, nargs='+')
args = parser.parse_args()
field_index = args.field_index


filenames = []
for root,_,files in os.walk(args.directory):
    for file in [Path(os.path.join(root, x)).absolute() for x in files]:
        if file.suffix == '.syx':
            template = Template.from_sysex(file)
            filenames.append([file, template])

def to_descriptor(header_fields):
    return ' '.join([str(header_fields[index]) for index in field_index])

descriptors = [(filename, to_descriptor(template.header_fields)) for (filename, template) in filenames]

variations = list({'%s' % (descriptor) for _, descriptor in descriptors})
variations.sort()

for variation in variations:
    print('%s' % variation)
    for filename, template in filenames:
        if (to_descriptor(template.header_fields) == variation):
            print('\t', str(filename))
