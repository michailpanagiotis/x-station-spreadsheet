#!/usr/bin/env python3
import os.path
import argparse
from pathlib import Path
from xstation_parser import Template, extract_templates
from operator import itemgetter

filenames = []
for root,_,files in os.walk('./additional_templates'):
    for file in [Path(os.path.join(root, x)).absolute() for x in files]:
        if file.suffix == '.syx':
            template = Template.from_sysex(file)
            filenames.append([file, template])


parser = argparse.ArgumentParser(
    prog='x-station-sheet',
    description='Lists all permutations of a field in a set of .syx templates',
)

parser.add_argument('field', choices=['Type'])

controls = [(filename, control) for (filename, template) in filenames for control in template.controls if str(control["Type"]) == "10"]

per_template = {str(x): { "template": x, "files": [] } for x in extract_templates([x[1] for x in controls])}

for (filename, control) in controls:
    for template in [x["template"] for x in per_template.values()]:
        if control.get_template() == template:
            per_template[str(template)]["files"].append(filename)


for _, value in per_template.items():
    template, files = itemgetter('template', 'files')(value)
    print(template)
    for file in files:
        print('\t', file)
