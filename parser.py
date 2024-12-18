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

class Field():
    def __init__(self, name, bytes, aliases=[]):
        self.name = name
        self.bytes = bytes
        self.aliases = aliases

    def __len__(self):
        return len(self.bytes)

class NumericValue(Field):
    def __init__(self, name, byte, *args, **kwargs):
        super().__init__(name, bytes([byte]), *args, **kwargs)

    def __repr__(self):
        return '<%s>%s' % (self.name, self.bytes[0])

class ZeroPadding(Field):
    def __init__(self, name, value, *args, **kwargs):
        if len(value) != 4:
            raise Exception('bad length')
        for b in value:
            if b !=0 :
                raise Exception('non-zero padding')
        super().__init__(name, value, *args, **kwargs)

    def __repr__(self):
        return ''

class BitMap(Field):
    def __init__(self, ms_name, ls_name, byte, *args, **kwargs):
        self._ms_name = ms_name
        self._ls_name = ls_name
        super().__init__('%s|%s' % (ms_name, ls_name), bytes([byte]), *args, **kwargs)

    def __repr__(self):
        formatted = "{:08b}".format(self.bytes[0])
        return '<%s|%s>%s|%s' % (self._ms_name, self._ls_name, formatted[:4], formatted[4:])

class SysexValue(Field):
    def __init__(self, name, value, *args, **kwargs):
        if len(value) != 18:
            raise Exception('bad length')
        super().__init__(name, bytes(value), *args, **kwargs)

    def __repr__(self):
        return '<%s>%s...' % (self.name, hex(self.bytes[0]))

class StringValue(Field):
    def __init__(self, name, value, *args, **kwargs):
        if len(value) != 16:
            raise Exception('bad length')
        super().__init__(name, bytes(value), *args, **kwargs)

    def __repr__(self):
        return '<%s>%s' % (self.name, ''.join([chr(x) for x in self.bytes]).strip())

class SingleControl(dict):
    def __init__(self, idx, byte_index, cmd, name_length=16, sysex_length=18):
        if len(cmd) != 52:
            raise Exception('bad length')

        cmd = [x for x in cmd]

        fields = []
        name = bytes(cmd[:name_length])
        fields.append(StringValue('Name', bytes(cmd[:name_length]), aliases=['Control name']))
        cmd = cmd[name_length:]

        fields.append(NumericValue('Type', cmd.pop(0), aliases=['Control Type']))
        fields.append(NumericValue('Low', cmd.pop(0), aliases=['Template', 'Velocity', 'MMC Command']))
        fields.append(NumericValue('High', cmd.pop(0)))
        fields.append(BitMap('Ports', 'Button', cmd.pop(0)))
        fields.append(NumericValue('Pot', cmd.pop(0), aliases=['Pot / Slider Control Type']))
        fields.append(NumericValue('Display', cmd.pop(0), aliases=['Display type']))
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

        padding = bytes(cmd[:4])
        fields.append(ZeroPadding('Zeros', padding))

        cmd = cmd[4:]

        if len(cmd) != 0:
            raise Exception('non parsed fields')

        self.index = idx
        self.byte_index = byte_index
        self.full_name = ''.join([chr(x) for x in name])
        self.name = self.full_name.strip()
        self._fields = fields
        for field in fields:
            self[field.name] = field.bytes

    def __str__(self):
        return '%s' % (' '.join([str(x) for x in self._fields if x.name != 'Name']))

    @property
    def bytes(self):
        bytes = bytearray()
        for field in self._fields:
            bytes.extend(field.bytes)
        return bytes

    @property
    def legend(self):
        if self.index < len(indices):
            selector = '(%s)' % indices[self.index]['selector'] if 'selector' in indices[self.index] else ''
            return '%s %s > %s\t' % (indices[self.index]['section'], selector, indices[self.index]['legend'])
        return ''

    def __getitem__(self, key):
        field = next((x for x in self._fields if x.name == key), None)
        if field is None:
            raise KeyError
        return field

    def __len__(self):
        return len(self.bytes)

class Template():
    def __init__(self, file):
        offset = 405
        line_size = 52
        self.controls = []
        self.footer = []
        with open(file, "rb") as f:
            file_contents = f.read()

        self.header = file_contents[:offset]
        for x in range(offset, len(file_contents), line_size):
            if x + 52 > len(file_contents):
                self.footer = file_contents[x:]
                break;

            line = file_contents[x : x + line_size]
            control = SingleControl(len(self.controls), x, line)
            self.controls.append(control)

    def write(self, file):
        with open(file, "wb") as f:
            f.write(self.bytes)

    def __str__(self):
       return '\n'.join([str(x) for x in self.controls])

    def print_all(self):
        for control in self.controls:
            print('')
            print('%s %s\t: %s' % (control.byte_index, control.full_name, control))

    def print_distinct(self, fieldName):
        print(set([c[fieldName] for c in self.controls]), sys.argv[1])

    def print_fields(self, fieldName):
        for line in self.controls:
            print('%s %s %s %s' % (line.legend, line['name'], line['CC|Note'], line[fieldName]))

    @property
    def bytes(self):
        bytes = bytearray(self.header)
        for control in self.controls:
            bytes.extend(control.bytes)
        bytes.extend(self.footer)
        return bytes

template = Template(sys.argv[1])
template.print_all()
# template.print_fields('unknown3')
# template.print_distinct('unknown3')
# print(template.bytes)
# template.write(sys.argv[2])

len(indices)
