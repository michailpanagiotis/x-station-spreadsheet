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

indices = [{
    'section': 'OSCS - MIXER', 'label': 'PORTAMENTO'
}, {
    'section': 'OSCS - MIXER', 'label': 'UNISON'
}, {
    'section': 'OSCS - MIXER', 'label': 'WAVEFORM', 'predicate': 'Osc 1',
}, {
    'section': 'OSCS - MIXER', 'label': 'SEMITONE', 'predicate': 'Osc 1',
}, {
    'section': 'OSCS - MIXER', 'label': 'DETUNE', 'predicate': 'Osc 1',
}, {
    'section': 'OSCS - MIXER', 'label': 'LEVEL', 'predicate': 'Osc 1',
}, {
    'section': 'OSCS - MIXER', 'label': 'PWM', 'predicate': 'Osc 1',
}, {
    'section': '???? OSCS - MIXER', 'label': '????'
}, {
    'section': '???? OSCS - MIXER', 'label': '????'
}, {
    'section': 'OSCS - MIXER', 'label': 'OCTAVE'
}, {
    'section': 'OSCS - MIXER', 'label': 'ENV DEPTH'
}, {
    'section': 'OSCS - MIXER', 'label': 'LFO DEPTH'
}, {
    'section': 'OSCS - MIXER', 'label': 'SYNC'
}, {
    'section': 'OSCS - MIXER', 'label': 'WAVEFORM', 'predicate': 'Osc 2',
}, {
    'section': 'OSCS - MIXER', 'label': 'SEMITONE', 'predicate': 'Osc 2',
}, {
    'section': 'OSCS - MIXER', 'label': 'DETUNE', 'predicate': 'Osc 2',
}, {
    'section': 'OSCS - MIXER', 'label': 'LEVEL', 'predicate': 'Osc 2',
}, {
    'section': 'OSCS - MIXER', 'label': 'PWM', 'predicate': 'Osc 2',
}, {
    'section': '???? OSCS - MIXER', 'label': '????'
}, {
    'section': '???? OSCS - MIXER', 'label': '????'
}]

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

    def __len__(self):
        return self._num_bytes

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
    def __init__(self, idx, position, cmd, name_length=16):
        if len(cmd) != 52:
            raise Exception('bad length')

        cmd = [x for x in cmd]

        fields = []
        name = bytes(cmd[:name_length])
        fields.append(StringValue('name', name))

        cmd = cmd[name_length:]

        fields.append(NumericValue('Control Type', cmd.pop(0)))
        fields.append(NumericValue('Low|Template|Velocity|MMC Command', cmd.pop(0)))
        fields.append(NumericValue('Hi', cmd.pop(0)))
        fields.append(BitMap('Ports', 'Button type', cmd.pop(0)))
        fields.append(NumericValue('PotCtrl', cmd.pop(0)))
        fields.append(NumericValue('DisplayType', cmd.pop(0)))
        fields.append(NumericValue('NRPN|RPN MSBank Num', cmd.pop(0)))
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
        fields.append(ZeroPadding('Padding', 4))

        cmd = cmd[4:]

        if len(cmd) != 0:
            raise Exception('non parsed fields')

        self._idx = idx
        self._position = position
        self._name = name
        self._fields = fields
        for field in fields:
            self[field._name] = bytes(field._bytes)

    def __str__(self):
        return '%s' % (' '.join([str(x) for x in self._fields]))

    @property
    def _bytes(self):
        _bytes = bytearray()
        for field in self._fields:
            _bytes.extend(field._bytes)
        return _bytes

    @property
    def label(self):
        if self._idx < len(indices):
            return '%s > %s\t' % (indices[self._idx]['section'], indices[self._idx]['label'])
        return ''

    def __len__(self):
        return len(self._bytes)

class Template():
    def __init__(self, file):
        offset = 405
        line_size = 52
        self.controls = []
        self.footer = []
        with open(file, "rb") as f:
            all_bytes = f.read()

        self.header = all_bytes[:offset]
        for x in range(offset, len(all_bytes), line_size):
            if x + 52 > len(all_bytes):
                self.footer = all_bytes[x:]
                break;

            line = all_bytes[x : x + line_size]
            control = SingleControl(len(self.controls), x, line)
            self.controls.append(control)

    def write(self, file):
        with open(file, "wb") as f:
            f.write(self._bytes)

    def __str__(self):
       return '\n'.join([str(x) for x in self.controls])

    def print_all(self):
        for control in self.controls:
            print(control._position, control._position + len(control), control['name'], control)

    def print_distinct(self, fieldName):
        print(set([c[fieldName] for c in self.controls]), sys.argv[1])

    def print_field(self, fieldName):
        for line in self.controls:
            print('%s %s CC%s %s' % (line.label, line['name'], ord(line['CC|Note']), ord(line[fieldName])))

    @property
    def _bytes(self):
        _bytes = bytearray(self.header)
        for control in self.controls:
            _bytes.extend(control._bytes)
        _bytes.extend(self.footer)
        return _bytes

template = Template(sys.argv[1])
# template.print_all()
template.print_field('unknown3')
# template.print_distinct('unknown3')
# print(template._bytes)
# template.write(sys.argv[2])
