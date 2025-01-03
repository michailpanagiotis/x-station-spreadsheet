#!/usr/bin/env python3
import os.path
import argparse
from pathlib import Path
from xstation_parser import Template, extract_templates, CONTROL_TEMPLATE_PHYSICAL_FIELDS, get_control_legend

parser = argparse.ArgumentParser(
    prog='control_variations',
    description='Lists all variations of a control in a set of .syx templates',
)
parser.add_argument('directory')
args = parser.parse_args()
template_definition = CONTROL_TEMPLATE_PHYSICAL_FIELDS

def to_descriptor(control_template):
    return str(control_template)

filenames = []
for root,_,files in os.walk(args.directory):
    for file in [Path(os.path.join(root, x)).absolute() for x in files]:
        if file.suffix == '.syx':
            template = Template.from_sysex(file)
            filenames.append([file, template])

variations = list({to_descriptor(control_template) for (_, template) in filenames for control_template in extract_templates(template.controls, definition=template_definition) })
variations.sort()

for variation in variations:
    print('%s' % variation)
    for filename, template in filenames:
        for idx, control in enumerate(template.controls):
            if (to_descriptor(control.get_subset(template_definition)) == variation):
                print('\t', get_control_legend(idx), str(filename))
                break
