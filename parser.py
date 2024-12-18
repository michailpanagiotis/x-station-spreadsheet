#!/usr/bin/env python3
import json
import pprint
import re
import sys

indices = [
    { 'section': 'OSCS - MIXER', 'legend': 'PORTAMENTO' },
    { 'section': 'OSCS - MIXER', 'legend': 'UNISON' },
    { 'section': 'OSCS - MIXER', 'legend': 'WAVEFORM', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'SEMITONE', 'selector': 'Osc 1', },
    { 'section': 'OSCS - MIXER', 'legend': 'DETUNE', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'LEVEL', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'PWM', 'selector': 'Osc 1' },
    { 'section': '???? OSCS - MIXER', 'legend': '????' },
    { 'section': '???? OSCS - MIXER', 'legend': '????' },
    { 'section': 'OSCS - MIXER', 'legend': 'OCTAVE', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'ENV DEPTH', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'LFO DEPTH', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'SYNC', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'WAVEFORM', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'SEMITONE', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'DETUNE', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'LEVEL', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'PWM', 'selector': 'Osc 2' },
    { 'section': '???? OSCS - MIXER', 'legend': '????' },
    { 'section': '???? OSCS - MIXER', 'legend': '????' },
    { 'section': 'OSCS - MIXER', 'legend': 'OCTAVE', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'ENV DEPTH', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'LFO DEPTH', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'SYNC', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'WAVEFORM', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'SEMITONE', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'DETUNE', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'LEVEL', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'PWM', 'selector': 'Osc 3' },
    { 'section': '???? OSCS - MIXER', 'legend': '????' },
    { 'section': '???? OSCS - MIXER', 'legend': '????' },
    { 'section': 'OSCS - MIXER', 'legend': 'OCTAVE', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'ENV DEPTH', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'LFO DEPTH', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'SYNC', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'WAVEFORM', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'SEMITONE', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'DETUNE', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'LEVEL', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'PWM', 'selector': 'Noise' },
    { 'section': '???? OSCS - MIXER', 'legend': '????' },
    { 'section': '???? OSCS - MIXER', 'legend': '????' },
    { 'section': 'OSCS - MIXER', 'legend': 'OCTAVE', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'ENV DEPTH', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'LFO DEPTH', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'SYNC', 'selector': 'Noise' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': 'FILTERS', 'legend': 'FREQUENCY', 'selector': '1' },
    { 'section': 'FILTERS', 'legend': 'RESONANCE', 'selector': '1' },
    { 'section': 'FILTERS', 'legend': 'KEY TRACK', 'selector': '1' },
    { 'section': 'FILTERS', 'legend': 'ENV DEPTH', 'selector': '1' },
    { 'section': 'FILTERS', 'legend': 'LFO DEPTH', 'selector': '1' },
    { 'section': 'FILTERS', 'legend': 'OVERDRIVE', 'selector': '1' },
    { 'section': 'FILTERS', 'legend': 'SLOPE', 'selector': '1' },
    { 'section': 'FILTERS', 'legend': 'TYPE', 'selector': '1' },
    { 'section': 'FILTERS', 'legend': 'HPF ON', 'selector': '1' },
    { 'section': 'FILTERS', 'legend': 'FREQUENCY', 'selector': '2' },
    { 'section': 'FILTERS', 'legend': 'RESONANCE', 'selector': '2' },
    { 'section': 'FILTERS', 'legend': 'KEY TRACK', 'selector': '2' },
    { 'section': 'FILTERS', 'legend': 'ENV DEPTH', 'selector': '2' },
    { 'section': 'FILTERS', 'legend': 'LFO DEPTH', 'selector': '2' },
    { 'section': 'FILTERS', 'legend': 'OVERDRIVE', 'selector': '2' },
    { 'section': 'FILTERS', 'legend': 'SLOPE', 'selector': '2' },
    { 'section': 'FILTERS', 'legend': 'TYPE', 'selector': '2' },
    { 'section': 'FILTERS', 'legend': 'HPF ON', 'selector': '2' },
    { 'section': 'LFOS', 'legend': 'SPEED', 'selector': '1' },
    { 'section': 'LFOS', 'legend': 'DELAY/AMOUNT', 'selector': '1' },
    { 'section': 'LFOS', 'legend': 'WAVEFORM', 'selector': '1' },
    { 'section': 'LFOS', 'legend': 'DEST', 'selector': '1' },
    { 'section': 'LFOS', 'legend': 'SPEED', 'selector': '2' },
    { 'section': 'LFOS', 'legend': 'DELAY/AMOUNT', 'selector': '2' },
    { 'section': 'LFOS', 'legend': 'WAVEFORM', 'selector': '2' },
    { 'section': 'LFOS', 'legend': 'DEST', 'selector': '2' },
    { 'section': 'LFOS', 'legend': 'SPEED', 'selector': '3' },
    { 'section': 'LFOS', 'legend': 'DELAY/AMOUNT', 'selector': '3' },
    { 'section': 'LFOS', 'legend': 'WAVEFORM', 'selector': '3' },
    { 'section': 'LFOS', 'legend': 'DEST', 'selector': '3' },
    { 'section': 'AMP ENV', 'legend': 'ATTACK' },
    { 'section': 'AMP ENV', 'legend': 'DECAY' },
    { 'section': 'AMP ENV', 'legend': 'SUSTAIN' },
    { 'section': 'AMP ENV', 'legend': 'RELEASE' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'ATTACK' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'DECAY' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'SUSTAIN' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'RELEASE' },
    { 'section': 'AMP ENV', 'legend': 'MONO / POLY', 'selector': 'Mod' },
    { 'section': 'AMP ENV', 'legend': 'GATE', 'selector': 'Mod' },
    { 'section': 'AMP ENV', 'legend': 'HOLD', 'selector': 'Mod' },
    { 'section': 'AMP ENV', 'legend': 'ON / OFF', 'selector': 'Mod' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'DEST', 'selector': 'Mod' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'GATE', 'selector': 'Mod' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'F1', 'selector': 'Mod' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'F2', 'selector': 'Mod' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'F3', 'selector': 'Mod' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': 'AMP ENV', 'legend': 'MONO / POLY', 'selector': 'Env 3' },
    { 'section': 'AMP ENV', 'legend': 'GATE', 'selector': 'Env 3' },
    { 'section': 'AMP ENV', 'legend': 'HOLD', 'selector': 'Env 3' },
    { 'section': 'AMP ENV', 'legend': 'ON / OFF', 'selector': 'Env 3' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'DEST', 'selector': 'Env 3' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'GATE', 'selector': 'Env 3' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'F1', 'selector': 'Env 3' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'F2', 'selector': 'Env 3' },
    { 'section': 'MOD ENV / ENV 3', 'legend': 'F3', 'selector': 'Env 3' },
    { 'section': 'VELOCITY', 'legend': 'VELOCITY' },
    { 'section': 'VELOCITY', 'legend': 'TRIGGER', 'selector': 'Amp' },
    { 'section': 'VELOCITY', 'legend': 'REPEAT', 'selector': 'Amp' },
    { 'section': '??? VELOCITY', 'legend': '???', 'selector': 'Amp' },
    { 'section': 'VELOCITY', 'legend': 'TRIGGER', 'selector': 'Mod' },
    { 'section': 'VELOCITY', 'legend': 'REPEAT', 'selector': 'Mod' },
    { 'section': '??? VELOCITY', 'legend': '???', 'selector': 'Mod' },
    { 'section': 'VELOCITY', 'legend': 'TRIGGER', 'selector': 'Env 3' },
    { 'section': 'VELOCITY', 'legend': 'REPEAT', 'selector': 'Env 3' },
    { 'section': 'ARP', 'legend': 'TEMPO' },
    { 'section': 'ARP', 'legend': 'ON' },
    { 'section': 'ARP', 'legend': 'LATCH' },
    { 'section': 'EFFECTS', 'legend': 'LEVEL' },
    { 'section': 'EFFECTS', 'legend': 'SELECT' },
    { 'section': 'EFFECTS', 'legend': 'CONTROL' },
    { 'section': 'EXTERNAL', 'legend': 'SUSTAIN' },
    { 'section': 'EXTERNAL', 'legend': 'EXPRESSION' },
    { 'section': 'PITCH/MOD', 'legend': 'PITCH BEND' },
    { 'section': 'PITCH/MOD', 'legend': 'MOD WHEEL' },
    { 'section': 'TOUCHPAD', 'legend': 'X' },
    { 'section': 'TOUCHPAD', 'legend': 'Y' },
    { 'section': '???', 'legend': '???' },
    { 'section': '???', 'legend': '???' },
    { 'section': 'TRANSPORT', 'legend': 'STOP' },
    { 'section': 'TRANSPORT', 'legend': 'PLAY' },
    { 'section': 'TRANSPORT', 'legend': 'REC' },
    { 'section': 'TRANSPORT', 'legend': 'FF' },
    { 'section': 'TRANSPORT', 'legend': 'RW' },
    { 'section': '???', 'legend': '???' },
]

class NumericValue(dict):
    def __init__(self, name, byte, aliases=[]):
        self.name = name
        self._byte = byte
        self._bytes = [byte]
        self._aliases = aliases
        dict.__init__(self, name=name, byte=byte)

    def __repr__(self):
        return '<%s>%s' % (self.name, self._byte)

    def __len__(self):
        return 1

class ZeroPadding():
    def __init__(self, name, num_bytes):
        self.name = name
        self._num_bytes = num_bytes
        self._bytes = b''.join([b'\x00'] * num_bytes)

    def __repr__(self):
        return '<zeros>%s' % self._num_bytes

    def __len__(self):
        return self._num_bytes

class BitMap():
    def __init__(self, ms_name, ls_name, byte):
        self._ms_name = ms_name
        self._ls_name = ls_name
        self._bytes = bytes([byte])
        self.name = '%s|%s' % (ms_name, ls_name)

    def __repr__(self):
        formatted = "{:08b}".format(self._bytes[0])
        return '<%s>%s|<%s>%s' % (self._ms_name, formatted[:4], self._ls_name, formatted[4:])

    def __len__(self):
        return 1

class SysexValue():
    def __init__(self, name, value):
        self.name = name
        if len(value) != 18:
            raise Exception('bad length')
        self._bytes = bytes(value)

    def __repr__(self):
        return '<%s>%s' % (self.name, ''.join([hex(x) for x in self._bytes]))

class StringValue():
    def __init__(self, name, value):
        self.name = name
        if len(value) != 16:
            raise Exception('bad length')
        self._bytes = bytes(value)

    def __repr__(self):
        return '<%s>%s' % (self.name, ''.join([chr(x) for x in self._bytes]).strip())

    def __len__(self):
        return len(self._bytes)

class SingleControl(dict):
    def __init__(self, idx, position, cmd, name_length=16, sysex_length=18):
        if len(cmd) != 52:
            raise Exception('bad length')

        cmd = [x for x in cmd]

        fields = []
        name = bytes(cmd[:name_length])
        fields.append(StringValue('Control name', name))
        cmd = cmd[name_length:]

        fields.append(NumericValue('Type', cmd.pop(0), aliases=['Control Type']))
        fields.append(NumericValue('Low', cmd.pop(0), aliases=['Template', 'Velocity', 'MMC Command']))
        fields.append(NumericValue('High', cmd.pop(0)))
        fields.append(BitMap('Ports', 'Button type', cmd.pop(0)))
        fields.append(NumericValue('Pot Type', cmd.pop(0)))
        fields.append(NumericValue('Display Type', cmd.pop(0)))
        fields.append(NumericValue('MSBank', cmd.pop(0), aliases=['NRPN MSBank Num']))
        fields.append(NumericValue('CC', cmd.pop(0), aliases=['Note']))
        fields.append(NumericValue('Ch', cmd.pop(0), aliases=['Channel', 'Device id']))
        fields.append(NumericValue('Template', cmd.pop(0), aliases=['Template', 'Velocity', 'MMC Command']))
        fields.append(NumericValue('unknown1', cmd.pop(0)))
        fields.append(NumericValue('unknown2', cmd.pop(0)))
        fields.append(NumericValue('unknown3', cmd.pop(0)))

        sysex = bytes(cmd[:sysex_length])
        fields.append(SysexValue('Sysex', sysex))
        cmd = cmd[sysex_length:]

        fields.append(NumericValue('Step', cmd.pop(0)))
        fields.append(ZeroPadding('Padding', 4))

        cmd = cmd[4:]

        if len(cmd) != 0:
            raise Exception('non parsed fields')

        self._idx = idx
        self.position = position
        self.name = name
        self._fields = fields
        for field in fields:
            self[field.name] = bytes(field._bytes)

    def __str__(self):
        return '%s' % (' '.join([str(x) for x in self._fields]))

    @property
    def _bytes(self):
        _bytes = bytearray()
        for field in self._fields:
            _bytes.extend(field._bytes)
        return _bytes

    @property
    def legend(self):
        if self._idx < len(indices):
            selector = '(%s)' % indices[self._idx]['selector'] if 'selector' in indices[self._idx] else ''
            return '%s %s > %s\t' % (indices[self._idx]['section'], selector, indices[self._idx]['legend'])
        return ''

    def __getitem__(self, key):
        field = next((x for x in self._fields if x.name == key), None)
        if field is None:
            raise KeyError
        return field

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
            print(control.position, control.position + len(control), control.name, control)

    def print_distinct(self, fieldName):
        print(set([c[fieldName] for c in self.controls]), sys.argv[1])

    def print_fields(self, fieldName):
        for line in self.controls:
            print('%s %s %s %s' % (line.legend, line['name'], line['CC|Note'], line[fieldName]))

    @property
    def _bytes(self):
        _bytes = bytearray(self.header)
        for control in self.controls:
            _bytes.extend(control._bytes)
        _bytes.extend(self.footer)
        return _bytes

template = Template(sys.argv[1])
template.print_all()
# template.print_fields('unknown3')
# template.print_distinct('unknown3')
# print(template._bytes)
# template.write(sys.argv[2])

len(indices)
