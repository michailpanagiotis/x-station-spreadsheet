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
    def __init__(self, cmd, init_length=3, zeros_length=24, name_length=16, rest_length=8):
        if rest_length == 8 and len(cmd) == 51:
            return self.__init__(cmd, rest_length=7)

        if name_length == 16 and len(cmd) == 1 + init_length + zeros_length + 2:
            return self.__init__(cmd, name_length=2, rest_length=0)

        if len(cmd) != 1 + init_length + zeros_length + name_length + rest_length:
            raise Exception('cmd bad length %s %s' % (len(cmd), cmd))

        init_offset = 1
        zeros_offset = init_offset + init_length
        name_offset = zeros_offset + zeros_length
        rest_offset = name_offset + name_length

        fields = [NumericValue('ch', cmd[0])]
        fields.extend([NumericValue('unknown', x) for x in cmd[init_offset:zeros_offset]])

        zeros = cmd[zeros_offset:name_offset]
        # for z in zeros:
        #     if z != 0:
        #         print(cmd)
        #         print(len(cmd))
        #         raise Exception('bad zeros')

        # fields.append(NumericValue('zeros', len(zeros)))

        fields.append(NumericValue('unknown', cmd[zeros_offset]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 1]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 2]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 3]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 4]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 5]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 6]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 7]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 8]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 9]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 10]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 11]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 12]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 13]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 14]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 15]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 16]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 17]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 18]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 19]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 20]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 21]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 22]))
        fields.append(NumericValue('unknown', cmd[zeros_offset + 23]))


        name = cmd[name_offset:rest_offset].decode('ascii')
        fields.append(StringValue('name', name, hidden=True))

        if rest_length >= 7:
            fields.append(NumericValue('Ct', cmd[rest_offset]))
            fields.append(NumericValue('Low', cmd[rest_offset+1]))
            fields.append(NumericValue('Hi', cmd[rest_offset+2]))
            fields.append(BitMap('Ports', 'Button type', cmd[rest_offset+3]))
            fields.append(NumericValue('PotCtrl', cmd[rest_offset+4], hidden=True))
            fields.append(NumericValue('unknown', cmd[rest_offset+5]))
            fields.append(NumericValue('NRPN MSBank Num', cmd[rest_offset+6], hidden=True))

        if rest_length == 8:
            fields.append(NumericValue('CC', cmd[-1]))
        self._name = name
        self._fields = fields

    def __str__(self):
        return '<%s> %s' % (self._name, ' '.join([str(x) for x in self._fields]))

def parseSingle(cmd):
    control = SingleControl(cmd)
    print(control)
    return (control._name, control._fields)

def parseMulti(data):
    step = 52
    cmds = [data[x:x+step] for x in range(0, len(data), step)]
    fields = [parseSingle(cmd) for cmd in cmds if len(cmd) > 0]
    return {name:fields for (name, fields) in fields}


with open(sys.argv[1], "rb") as f:
    all_bytes = f.read()


# remove first and last byte (SysEx bytes)
matches = re.findall(b'\x0f[^\x0f]+', all_bytes[1:-1])
# print(len(matches))
for match in matches:
    dd = parseMulti(match)
