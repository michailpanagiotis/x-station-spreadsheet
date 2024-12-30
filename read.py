#!/usr/bin/env python3
import argparse
import signal
import subprocess
import time
from pathlib import Path


parser = argparse.ArgumentParser(
    prog='read',
    description='Reads a SYSEX template from X-Station'
)

parser.add_argument('filename')
args = parser.parse_args()

filename = args.filename
Path(filename).touch()

p = subprocess.Popen(['amidi', '-r', filename, '-p', 'hw:1,0,0'])
f = subprocess.Popen(['tail','-F',filename], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

print('On your X-Station, select a template, then \'GLOBAL>Dump: Current Template\'')

echoed = False
while True:
    byte = f.stdout.read(1)
    if not echoed:
        print('receiving sysex in \'%s\'...' % filename)
        echoed = True
    if byte == b'\xf7':
        break

print('receiving sysex in \'%s\'...done!' % filename)

f.send_signal(signal.SIGINT)
f.wait()
p.send_signal(signal.SIGINT)
p.wait()
