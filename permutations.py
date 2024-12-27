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
    prog='x-station-sheet',
    description='Lists all permutations of a field in a set of .syx templates',
)

parser.add_argument('field', choices=['Type'])

for [filename, template] in filenames:
    sql = template.to_sql()
    for q in sql:
        print(q)
