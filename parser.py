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
        self._bytes = [byte]
        self._hidden = hidden
        dict.__init__(self, name=name, byte=byte)

    def __repr__(self):
        if self._name == 'unknown':
            if self._byte:
                return '<N>%s' % (self._byte)
            else:
                return '?<%s>' % (self._byte)
        if self._hidden:
            return '_'
        return '<%s>%s' % (self._name, self._byte)

    def __len__(self):
        return 1

class SysexValue(NumericValue):
    def __repr__(self):
        return 'sx'

class ZeroPadding():
    def __init__(self, name, num_bytes):
        self._name = name
        self._num_bytes = num_bytes
        self._bytes = b''.join([b'\x00'] * num_bytes)

    def __repr__(self):
        return '<zeros>%s' % self._num_bytes


class BitMap(dict):
    def __init__(self, ms_name, ls_name, byte):
        self._ms_name = ms_name
        self._ls_name = ls_name
        self._byte = byte
        self._bytes = bytes([byte])
        self._name = '%s|%s' % (ms_name, ls_name)
        dict.__init__(self, ms_name=ms_name, ls_name=ls_name, byte=byte)

    def __repr__(self):
        formatted = "{:08b}".format(self._byte)
        return '<%s>%s|<%s>%s' % (self._ms_name, formatted[:4], self._ls_name, formatted[4:])

    def __len__(self):
        return 1

class StringValue(dict):
    def __init__(self, name, value, hidden=False):
        self._name = name
        self._bytes = bytes(value)
        self._hidden = hidden
        dict.__init__(self, name=name, bytes=value)

    def __repr__(self):
        if self._hidden:
            return ''
        if self._name == 'unknown':
            return '<S>%s' % (ascii(self._bytes))
        return '<%s>%s' % (self._name, ascii(self._bytes))

    def __len__(self):
        return len(self._bytes)

class SingleControl(dict):
    def __init__(self, cmd, name_length=16):
        if len(cmd) != 52:
            raise Exception('bad length')

        cmd = [x for x in cmd]

        fields = []
        name = bytes(cmd[:name_length])
        fields.append(StringValue('name', name))

        cmd = cmd[name_length:]

        fields.append(NumericValue('Ct', cmd.pop(0)))
        fields.append(NumericValue('Low|Template|Velocity|MMC Command', cmd.pop(0)))
        fields.append(NumericValue('Hi', cmd.pop(0)))
        fields.append(BitMap('Ports', 'Button type', cmd.pop(0)))
        fields.append(NumericValue('PotCtrl', cmd.pop(0)))
        fields.append(NumericValue('DisplayType', cmd.pop(0)))
        fields.append(NumericValue('NRPN MSBank Num', cmd.pop(0)))
        fields.append(NumericValue('CC|Note', cmd.pop(0)))

        fields.append(NumericValue('Channel|Device id', cmd.pop(0)))
        fields.append(NumericValue('Template|Velocity|MMC Command', cmd.pop(0)))
        fields.append(NumericValue('unknown1', cmd.pop(0)))
        fields.append(NumericValue('unknown2', cmd.pop(0)))
        fields.append(NumericValue('unknown3', cmd.pop(0)))

        fields.append(SysexValue('sx1', cmd.pop(0)))
        fields.append(SysexValue('sx2', cmd.pop(0)))
        fields.append(SysexValue('sx3', cmd.pop(0)))
        fields.append(SysexValue('sx4', cmd.pop(0)))
        fields.append(SysexValue('sx5', cmd.pop(0)))
        fields.append(SysexValue('sx6', cmd.pop(0)))
        fields.append(SysexValue('sx7', cmd.pop(0)))
        fields.append(SysexValue('sx8', cmd.pop(0)))
        fields.append(SysexValue('sx9', cmd.pop(0)))
        fields.append(SysexValue('sx10', cmd.pop(0)))
        fields.append(SysexValue('sx11', cmd.pop(0)))
        fields.append(SysexValue('sx12', cmd.pop(0)))
        fields.append(SysexValue('sx13', cmd.pop(0)))
        fields.append(SysexValue('sx14', cmd.pop(0)))
        fields.append(SysexValue('sx15', cmd.pop(0)))
        fields.append(SysexValue('sx16', cmd.pop(0)))
        fields.append(SysexValue('sx17', cmd.pop(0)))
        fields.append(SysexValue('sx18', cmd.pop(0)))

        fields.append(NumericValue('Step', cmd.pop(0)))

        fields.append(ZeroPadding('zeros', 4))
        cmd = cmd[4:]

        if len(cmd) != 0:
            raise Exception('non parsed fields')

        self._name = name
        self._fields = fields
        for field in fields:
            self[field._name] = bytes(field._bytes)

    def __str__(self):
        return '%s' % (' '.join([str(x) for x in self._fields]))

class Template():
    def __init__(self, file):
        offset = 405
        line_size = 52
        self.lines = []
        self.footer = []
        with open(sys.argv[1], "rb") as f:
            all_bytes = f.read()

        self.header = all_bytes[:offset]
        for x in range(offset, len(all_bytes), line_size):
            if x + 52 > len(all_bytes):
                self.footer = all_bytes[x:]
                break;

            # if x != 6801:
            #     continue

            line = all_bytes[x : x + line_size]
            control = SingleControl(line)
            print(x, x + 52, control['name'], control)
            # print(line)
            self.lines.append(control)

    def __str__(self):
       return '\n'.join([str(x) for x in self.lines])

template = Template(sys.argv[1])
print(set([c['unknown3'] for c in template.lines]), sys.argv[1])
