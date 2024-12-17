#!/usr/bin/env python3
import sys

with open(sys.argv[1], "rb") as f:
    bytes_1 = f.read()

with open(sys.argv[2], "rb") as f:
    bytes_2 = f.read()

for idx, x in enumerate(bytes_1):
    if bytes_2[idx] != x:
        print('difference at', idx, bytes_1[idx], bytes_2[idx])
        exit()
