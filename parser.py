#!/usr/bin/env python3
import json
import pprint
import re
import sys

all_bytes = []
ccs = []
cursor = 0
prev_cc = False

packet_size = 52
packet_offset = 40
buffer = []

class NumericValue(dict):
    def __init__(self, name, byte, hidden=False):
        self._name = name
        self._byte = byte
        self._hidden = hidden
        dict.__init__(self, name=name, byte=byte)

    def __repr__(self):
        if self._name == 'unknown':
            if self._byte:
                return '<N>%s' % (self._byte)
            else:
                return '?'
        if self._hidden:
            return '_'
        return '<%s>%s' % (self._name, self._byte)

    def __len__(self):
        return 1

class BitMap(dict):
    def __init__(self, ms_name, ls_name, byte):
        self._ms_name = ms_name
        self._ls_name = ls_name
        self._byte = byte
        dict.__init__(self, ms_name=ms_name, ls_name=ls_name, byte=byte)

    def __repr__(self):
        formatted = "{:08b}".format(self._byte)
        return '<%s>%s|<%s>%s' % (self._ms_name, formatted[:4], self._ls_name, formatted[4:])

    def __len__(self):
        return 1

class StringValue(dict):
    def __init__(self, name, value, hidden=False):
        self._name = name
        self._bytes = value
        self._hidden = hidden
        dict.__init__(self, name=name, bytes=value)

    def __repr__(self):
        if self._hidden:
            return ''
        if self._name == 'unknown':
            return '<S>%s' % (ascii(self._bytes))
        return '<S: %s>%s' % (self._name, ascii(self._bytes))

    def __len__(self):
        return len(self._bytes)

class ChannelValue(NumericValue):
    def __init__(self, byte):
        super().__init__(name='ch', byte=byte)

class SingleControl(dict):
    def __init__(self, cmd, name_length=16):
        if len(cmd) != 52:
            raise Exception('bad length')

        self._length = len(cmd)
        print(' ')
        print(cmd)

        cmd = [x for x in cmd]

        fields = []

        fields.append(NumericValue('ch', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('Step', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))

        name = bytes(cmd[:name_length]).decode('ascii')
        fields.append(StringValue('name', name))

        cmd = cmd[name_length:]

        fields.append(NumericValue('Ct', cmd.pop(0)))
        fields.append(NumericValue('Low', cmd.pop(0)))
        fields.append(NumericValue('Hi', cmd.pop(0)))
        fields.append(BitMap('Ports', 'Button type', cmd.pop(0)))
        fields.append(NumericValue('PotCtrl', cmd.pop(0)))
        fields.append(NumericValue('unknown', cmd.pop(0)))
        fields.append(NumericValue('NRPN MSBank Num', cmd.pop(0)))
        fields.append(NumericValue('CC', cmd.pop(0)))

        self._name = name
        self._fields = fields

    def __str__(self):
        return '%s' % (' '.join([str(x) for x in self._fields]))

    def __len__(self):
        return self._length

def parseSingle(cmd):
    control = SingleControl(cmd)
    if len(control) != 52:
        print(' --------------XXXXX', control._name)
        # raise Exception('Wrong length %s' % len(control))
    return control

def parseMulti(data):
    step = 52
    cmds = [data[x:x+step] for x in range(0, len(data), step)]
    return [parseSingle(cmd) for cmd in cmds if len(cmd) > 0]


with open(sys.argv[1], "rb") as f:
    all_bytes = f.read()


lines = []
footer = []
offset = 429
header = all_bytes[:offset]
line_size = 52

for x in range(offset, len(all_bytes), line_size):
    if x + 52 > len(all_bytes):
        footer = all_bytes[x:]
        break;

    # if x != 6773:
    #     continue

    line = all_bytes[x : x + line_size]
    control = parseSingle(line)
    print(x, x + 52, control)
    # print(line)
    lines.append([(x, x + line_size)])

print('FOOTER', footer)

# print(lines)
# body_length = len(all_bytes) - 2
# offset = body_length % 52
#
# first = all_bytes.index(b'\x0f')
# last = len(all_bytes) - all_bytes[::-1].index(b'\x0f') - 1
#
# old_idx = 0
# for idx, byte in enumerate(all_bytes):
#     if byte == 15:
#         print(idx, idx-old_idx, (idx-old_idx) % 52)
#         old_idx = idx
#
# print('LIMITS', first, last)
# print(all_bytes[old_idx:])

# matches = re.findall(b'\x0f[^\x0f]+', all_bytes[1:-1])
# for match in matches:
#     controls = parseMulti(match)
#     for idx, control in enumerate(controls):
#         if idx == 0:
#             print(len(control), control)
#         else:
#             print('\t', len(control), control)

# lines = all_bytes[-107:-3]
# controls = parseMulti(lines)
# for idx, control in enumerate(controls):
#     print(len(control), control)
