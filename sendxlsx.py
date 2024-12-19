#!/usr/bin/env python3
import subprocess
import sys
from parser import Template

template = Template.from_spreadsheet(sys.argv[1])
filename = 'last_sent.syx'
template.write(filename)
subprocess.run(["amidi", "-s", filename, "-p", "hw:1,0,0"])
