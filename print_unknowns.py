#!/usr/bin/env python3
import sys
from parser import Template

template = Template.from_spreadsheet(sys.argv[1])
template2 = Template.from_spreadsheet(sys.argv[2])

print('HEADERS DIFF')
template.diff_headers(template2)

print('CONTROLS DIFF')
template.compare_unknowns(template2)
