#!/usr/bin/env python3
import sys

indices = [
    { 'section': 'OSCS - MIXER', 'legend': 'PORTAMENTO' },
    { 'section': 'OSCS - MIXER', 'legend': 'UNISON' },
    { 'section': 'OSCS - MIXER', 'legend': 'WAVEFORM', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'SEMITONE', 'selector': 'Osc 1', },
    { 'section': 'OSCS - MIXER', 'legend': 'DETUNE', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'LEVEL', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'PWM', 'selector': 'Osc 1' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': 'OSCS - MIXER', 'legend': 'OCTAVE', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'ENV DEPTH', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'LFO DEPTH', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'SYNC', 'selector': 'Osc 1' },
    { 'section': 'OSCS - MIXER', 'legend': 'WAVEFORM', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'SEMITONE', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'DETUNE', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'LEVEL', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'PWM', 'selector': 'Osc 2' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': 'OSCS - MIXER', 'legend': 'OCTAVE', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'ENV DEPTH', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'LFO DEPTH', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'SYNC', 'selector': 'Osc 2' },
    { 'section': 'OSCS - MIXER', 'legend': 'WAVEFORM', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'SEMITONE', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'DETUNE', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'LEVEL', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'PWM', 'selector': 'Osc 3' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': 'OSCS - MIXER', 'legend': 'OCTAVE', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'ENV DEPTH', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'LFO DEPTH', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'SYNC', 'selector': 'Osc 3' },
    { 'section': 'OSCS - MIXER', 'legend': 'WAVEFORM', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'SEMITONE', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'DETUNE', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'LEVEL', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'PWM', 'selector': 'Noise' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': 'OSCS - MIXER', 'legend': 'OCTAVE', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'ENV DEPTH', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'LFO DEPTH', 'selector': 'Noise' },
    { 'section': 'OSCS - MIXER', 'legend': 'SYNC', 'selector': 'Noise' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
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
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
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
    { 'section': '', 'legend': '???', 'selector': 'Amp' },
    { 'section': 'VELOCITY', 'legend': 'TRIGGER', 'selector': 'Mod' },
    { 'section': 'VELOCITY', 'legend': 'REPEAT', 'selector': 'Mod' },
    { 'section': '', 'legend': '???', 'selector': 'Mod' },
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
    { 'section': '', 'legend': '???' },
    { 'section': '', 'legend': '???' },
    { 'section': 'TRANSPORT', 'legend': 'STOP' },
    { 'section': 'TRANSPORT', 'legend': 'PLAY' },
    { 'section': 'TRANSPORT', 'legend': 'REC' },
    { 'section': 'TRANSPORT', 'legend': 'FF' },
    { 'section': 'TRANSPORT', 'legend': 'RW' },
    { 'section': '', 'legend': '???' },
]

class Field():
    def __init__(self, name, bytes, hidden=False, aliases=[]):
        self.name = name
        self.bytes = bytes
        self.aliases = aliases
        self.hidden = hidden

    def __len__(self):
        return len(self.bytes)

class NumericValue(Field):
    @classmethod
    def pop_from(cls, other_bytes, name, *args, **kwargs):
        return cls(name, other_bytes.pop(0), *args, **kwargs)

    def __init__(self, name, byte, *args, **kwargs):
        super().__init__(name, bytes([byte]), *args, **kwargs)

    def __repr__(self):
        return '<%s:%s>' % (self.name, self.bytes[0])

class SelectValue(Field):
    @classmethod
    def pop_from(cls, other_bytes, name, options, *args, **kwargs):
        return cls(name, other_bytes.pop(0), options, *args, **kwargs)

    def __init__(self, name, byte, options=[], *args, **kwargs):
        if byte not in options:
            raise Exception('unsupported option %s' % byte)
        super().__init__(name, bytes([byte]), *args, **kwargs)

    def __repr__(self):
        return '<%s:%s>' % (self.name, self.bytes[0])

class ZeroPadding(Field):
    @classmethod
    def pop_from(cls, other_bytes, name, num_zeros, *args, **kwargs):
        bytes = bytearray()
        for i in range(num_zeros):
            bytes.append(other_bytes.pop(0))
        return cls(name, bytes, *args, **kwargs)

    def __init__(self, name, value, *args, **kwargs):
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
        return '<%s:%s|%s:%s>' % (self._ms_name, formatted[:4], self._ls_name, formatted[4:])

class SysexValue(Field):
    def __init__(self, name, value, *args, **kwargs):
        if len(value) != 18:
            raise Exception('bad length')
        super().__init__(name, bytes(value), *args, **kwargs)

    def __repr__(self):
        return '<%s:%s>' % (self.name, ''.join([hex(x) for x in self.bytes]))

class StringValue(Field):
    @classmethod
    def pop_from(cls, other_bytes, name, size=16, *args, **kwargs):
        bytes = bytearray()
        for i in range(size):
            bytes.append(other_bytes.pop(0))
        return cls(name, bytes, size, *args, **kwargs)

    def __init__(self, name, value, size=16, *args, **kwargs):
        if len(value) != size:
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
        fields.append(NumericValue('N/A 1', cmd.pop(0)))
        fields.append(NumericValue('N/A 2', cmd.pop(0)))
        fields.append(NumericValue('N/A 3', cmd.pop(0)))

        sysex = bytes(cmd[:sysex_length])
        fields.append(SysexValue('Sysex', sysex, hidden=True))
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
    def section(self):
        return indices[self.index]['section']

    @property
    def legend(self):
        selector = '(%s)' % indices[self.index]['selector'] if 'selector' in indices[self.index] else ''
        legend = '%s%s>%s\t' % (indices[self.index]['section'], selector, indices[self.index]['legend'])
        return legend.rjust(30, ' ')

    def __getitem__(self, key):
        field = next((x for x in self._fields if x.name == key), None)
        if field is None:
            raise KeyError
        return field

    def __len__(self):
        return len(self.bytes)

class Template():
    MESSAGE_START=b'\xf0\x00 )\x02\x00\x7f\x00\x00'
    MESSAGE_END=b'\x124\xf7'

    def parse_header(self):
        if len(self.full_header) != 396:
            raise Exception('bad header bytes length')

        fields = []
        fields.append(SelectValue.pop_from(self.full_header, 'N/A 1', [8, 17, 19, 24, 25]))
        fields.append(SelectValue.pop_from(self.full_header, 'N/A 2', [1, 2, 3, 10]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 1))
        fields.append(NumericValue.pop_from(self.full_header, 'N/A 3'))
        fields.append(StringValue.pop_from(self.full_header, 'Name', 30))
        fields.append(SelectValue.pop_from(self.full_header, 'Channel', [0, 16]))
        fields.append(SelectValue.pop_from(self.full_header, 'Midi port', [0, 16, 48, 112]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 2))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 1', [0, 2]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 2', [4, 5]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 3', [0, 2]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 1))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 4', [0, 2]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 5', [0, 2]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 2))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 6', [48, 64, 79]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 7', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 2))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 8', [64, 78]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 9', [64, 127]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 2))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 10', [64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 11', [127]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 3))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 12', [0,1]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 13', [0,49]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 14', [64,68]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 15', [43,64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 16', [127]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 6))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 17', [0,18]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 18', [3,5]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [90]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0,64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 7))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0,1]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [20]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 5))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 1))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 32]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 1))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [127]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 1))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 3))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [100]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 3))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [52, 64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64, 78]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64, 72]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 6))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 4))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [127]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 2))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64, 78]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 4))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [3, 4]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [90]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 8))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [20]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64, 74]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 1))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 2))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 127]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [6, 44, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 1))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64, 127]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0,32]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 1))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [96, 127]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 1))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 2))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 36]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [100]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64, 65]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 2))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64, 98]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64, 74]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 6))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 3))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 1]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 1]))
        fields.append(SelectValue.pop_from(self.full_header, 'Midi port', [0, 112]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 2]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 56]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 60, 127]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 7]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 4))
        fields.append(SelectValue.pop_from(self.full_header, 'Midi port', [0, 112]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 2]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 69]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 72, 127]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 7]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 5))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 2]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 1))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 127]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 7]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 5))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 2]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 1))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 127]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 64]))
        fields.append(SelectValue.pop_from(self.full_header, 'Select 19', [0, 7]))
        fields.append(ZeroPadding.pop_from(self.full_header, 'Zeros', 170))

    def __init__(self, file):
        line_size = 52
        with open(file, "rb") as f:
            file_contents = f.read()

        self.controls = []

        if file_contents[:len(Template.MESSAGE_START)] != Template.MESSAGE_START:
            raise Exception('bad header')

        if file_contents[-len(Template.MESSAGE_END):] != Template.MESSAGE_END:
            raise Exception('bad footer')

        body = file_contents[len(Template.MESSAGE_START):-len(Template.MESSAGE_END)]
        offset = 405 - len(Template.MESSAGE_START)

        self.full_header = bytearray(body[:offset])
        controls = body[len(self.full_header):]

        self.parse_header()

        for byte_index in range(0, len(controls), line_size):
            bytes = controls[byte_index : byte_index + line_size]
            control = SingleControl(len(self.controls), byte_index, bytes)
            self.controls.append(control)

    def write(self, file):
        with open(file, "wb") as f:
            f.write(self.bytes)

    def __str__(self):
       return '\n'.join([str(x) for x in self.controls])

    def print_all(self, only_unknown=False):
        for control in self.controls:
            if only_unknown and control.section != '':
                continue
            # print('---- %s | %s | %s'  % (control.legend, control.full_name, control.byte_index, ))
            print(control.index, control.legend, control)
            # print('')

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
# template.print_all(only_unknown=True)
# template.print_fields('unknown3')
# template.print_distinct('unknown3')
# print(template.bytes)
# template.write(sys.argv[2])
print(len(template.full_header), template.full_header[:4], sys.argv[1])
