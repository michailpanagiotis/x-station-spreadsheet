#!/usr/bin/env python3
import sys
from parser import Template
from pathlib import Path

path = Path(sys.argv[1]).absolute()
output = path.with_suffix('.xlsx')

print(sys.argv[1], 'to', output)
template = Template.from_syx_file(path)
template.to_spreadsheet(output)
