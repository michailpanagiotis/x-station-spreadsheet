#!/usr/bin/env python3
import string
import sys
from openpyxl import Workbook, load_workbook

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

class RawBytes():
    @classmethod
    def _pop_from(cls, other_bytes, name="", *args, **kwargs):
        num_bytes = cls.NUM_BYTES

        instance = cls(other_bytes[:num_bytes], name, *args, **kwargs)

        if isinstance(other_bytes, bytearray):
            for _ in range(len(instance)):
                other_bytes.pop(0)

        return instance

    def __init__(self, bytes, name, valid_values=(), hidden=False, aliases=(), **kwargs):
        if not isinstance(bytes, bytearray):
            raise Exception('expecting a bytearray')

        self.name = name
        self.bytes = bytearray(bytes)

        if len(self.bytes) != type(self).NUM_BYTES:
            raise Exception('bad number of bytes')

        if len(valid_values) > 0:
            for byte in bytes:
               if byte not in valid_values:
                    raise Exception('unsupported option %s' % byte)

        self.hidden = hidden
        self.aliases = aliases

    def __str__(self):
        return ''.join([hex(x) for x in self.bytes])

    def __len__(self):
        return len(self.bytes)

class SingleByte(RawBytes):
    NUM_BYTES = 1

class NumericValue(SingleByte):
    def __str__(self):
        return str(self.bytes[0])

class SelectValue(NumericValue):
    def __init__(self, *args, **kwargs):
        valid_values = kwargs.pop('valid_values')
        super().__init__(*args, **kwargs, valid_values=valid_values)

class StringValue(RawBytes):
    def __str__(self):
        return ''.join([chr(x) for x in self.bytes if chr(x) in string.printable]).strip()

class ZeroPadding(RawBytes):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_values=(0,))

    def __str__(self):
        return str(len(self))

Sysex = type("Sysex", (RawBytes,), { "NUM_BYTES": 18 })
ControlName = type("ControlName", (StringValue,), { "NUM_BYTES": 16 })
TemplateName = type("TemplateName", (StringValue,), { "NUM_BYTES": 30 })
Pad1 = type("Pad1", (ZeroPadding,), { "NUM_BYTES": 1 })
Pad2 = type("Pad1", (ZeroPadding,), { "NUM_BYTES": 2 })
Pad3 = type("Pad1", (ZeroPadding,), { "NUM_BYTES": 3 })
Pad4 = type("Pad4", (ZeroPadding,), { "NUM_BYTES": 4 })
Pad5 = type("Pad5", (ZeroPadding,), { "NUM_BYTES": 5 })
Pad6 = type("Pad5", (ZeroPadding,), { "NUM_BYTES": 6 })
Pad7 = type("Pad5", (ZeroPadding,), { "NUM_BYTES": 7 })
Pad8 = type("Pad5", (ZeroPadding,), { "NUM_BYTES": 8 })
Pad170 = type("Pad5", (ZeroPadding,), { "NUM_BYTES": 170 })

class BitMap(SingleByte):
    def __init__(self, bytes, name, *args, **kwargs):
        self._ms_name = kwargs.pop('ms_name')
        self._ls_name = kwargs.pop('ls_name')
        super().__init__(bytes, '%s|%s' % (self._ms_name, self._ls_name), *args, **kwargs)

    def __repr__(self):
        formatted = "{:08b}".format(self.bytes[0])
        return '<%s:%s|%s:%s>' % (self._ms_name, formatted[:4], self._ls_name, formatted[4:])

    def __str__(self):
        return hex(self.bytes[0])

class SingleControl(dict):
    @classmethod
    def from_spreadsheet(self, row):
        values = [c.value for c in row]
        print('LEN', len(values))

    @classmethod
    def from_bytes(cls, idx, cmd, byte_index=None):
        if isinstance(cmd, bytes):
            if len(cmd) != 52:
                raise Exception('bad length')

            cmd = bytearray(cmd)

        fields = []
        fields.append(ControlName._pop_from(cmd, 'Name', aliases=['Control name']))
        fields.append(NumericValue._pop_from(cmd, 'Type', aliases=['Control Type']))
        fields.append(NumericValue._pop_from(cmd, 'Low', aliases=['Template', 'Velocity', 'MMC Command']))
        fields.append(NumericValue._pop_from(cmd, 'High'))
        fields.append(BitMap._pop_from(cmd, ms_name='Ports', ls_name='Button'))
        fields.append(NumericValue._pop_from(cmd, 'Pot', aliases=['Pot / Slider Control Type']))
        fields.append(NumericValue._pop_from(cmd, 'Display', aliases=['Display type']))
        fields.append(NumericValue._pop_from(cmd, 'MSBank', aliases=['NRPN MSBank Num']))
        fields.append(NumericValue._pop_from(cmd, 'CC', aliases=['Note']))
        fields.append(NumericValue._pop_from(cmd, 'Ch', aliases=['Channel', 'Device id']))
        fields.append(NumericValue._pop_from(cmd, 'Template', aliases=['Template', 'Velocity', 'MMC Command']))
        fields.append(NumericValue._pop_from(cmd, 'N/A 1'))
        fields.append(NumericValue._pop_from(cmd, 'N/A 2'))
        fields.append(NumericValue._pop_from(cmd, 'N/A 3'))
        fields.append(Sysex._pop_from(cmd, 'Sysex', hidden=True))
        fields.append(NumericValue._pop_from(cmd, 'Step'))
        fields.append(Pad4._pop_from(cmd, 'Zeros'))

        if len(cmd) != 0:
            raise Exception('non parsed fields')

        return cls(idx, fields, byte_index)

    def __init__(self, idx, fields, byte_index=None):
        name = next(x.bytes for x in fields if x.name == 'Name')
        self.index = idx
        self.byte_index = byte_index
        self.full_name = ''.join([chr(x) for x in name])
        self.name = self.full_name.strip()
        self.fields = fields
        for field in fields:
            self[field.name] = field.bytes

    def __str__(self):
        return '%s' % (' '.join([str(x) for x in self.fields if x.name != 'Name']))

    def dict(self):
        j = { "legend": self.legend.strip() }
        for f in self.fields:
            j[f.name] = str(f)
        return j

    def csv(self):
        return '%s,%s' % (self.legend.strip(), ','.join([str(x) for x in self.fields]))

    def write_to_sheet(self, ws, row_number):
        ws.cell(row=row_number, column=1, value=self.legend.strip())
        for idx, field in enumerate(self.fields):
            ws.cell(row=row_number, column=idx + 2, value=str(field))

    @property
    def bytes(self):
        bytes = bytearray()
        for field in self.fields:
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
        field = next((x for x in self.fields if x.name == key), None)
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
        fields.append(SelectValue._pop_from(self.full_header, 'N/A 1', valid_values=[8, 17, 19, 24, 25]))
        fields.append(SelectValue._pop_from(self.full_header, 'N/A 2', valid_values=[1, 2, 3, 10]))
        fields.append(Pad1._pop_from(self.full_header, 'Zeros'))
        fields.append(NumericValue._pop_from(self.full_header, 'N/A 3'))
        fields.append(TemplateName._pop_from(self.full_header, 'Name'))
        fields.append(SelectValue._pop_from(self.full_header, 'Channel', valid_values=[0, 16]))
        fields.append(SelectValue._pop_from(self.full_header, 'Midi port | Keyb MIDI Chan', valid_values=[0, 16, 48, 53, 54, 112]))
        fields.append(Pad2._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Velocity curve', valid_values=[0, 1, 2, 3]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 2', valid_values=[4, 5]))
        fields.append(SelectValue._pop_from(self.full_header, 'Aftertouch | Auto Snapshot | Not Synth', valid_values=[0, 2, 3, 4, 5, 6, 7]))
        fields.append(NumericValue._pop_from(self.full_header, 'Override MIDI Ch'))
        fields.append(SelectValue._pop_from(self.full_header, 'Touchpad X Type', valid_values=[0, 1, 2]))
        fields.append(SelectValue._pop_from(self.full_header, 'Touchpad Y Type', valid_values=[0, 1, 2]))
        fields.append(Pad2._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 6', valid_values=[48, 64, 79]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 7', valid_values=[0, 64]))
        fields.append(Pad2._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 8', valid_values=[64, 78]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 9', valid_values=[64, 127]))
        fields.append(Pad2._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 10', valid_values=[64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 11', valid_values=[127]))
        fields.append(Pad3._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 12', valid_values=[0,1]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 13', valid_values=[0,49]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 14', valid_values=[64,68]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 15', valid_values=[43,64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 16', valid_values=[127]))
        fields.append(Pad6._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 17', valid_values=[0,18]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 18', valid_values=[3,5]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[90]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0,64]))
        fields.append(Pad7._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0,1]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[20]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(Pad5._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64]))
        fields.append(Pad1._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 32]))
        fields.append(Pad1._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[127]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(Pad1._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(Pad3._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[100]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64]))
        fields.append(Pad3._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[52, 64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64, 78]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64, 72]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(Pad6._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(Pad4._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[127]))
        fields.append(Pad2._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64, 78]))
        fields.append(Pad4._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[3, 4]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[90]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(Pad8._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[20]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64, 74]))
        fields.append(Pad1._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(Pad2._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 127]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[6, 44, 64]))
        fields.append(Pad1._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64, 127]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0,32]))
        fields.append(Pad1._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[96, 127]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(Pad1._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(Pad2._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 36]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[100]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64, 65]))
        fields.append(Pad2._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64, 98]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64, 74]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(Pad6._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(Pad3._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 1]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 1]))
        fields.append(SelectValue._pop_from(self.full_header, 'Midi port', valid_values=[0, 112]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 2]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 56]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 60, 127]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 7]))
        fields.append(Pad4._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Midi port', valid_values=[0, 112]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 2]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 69]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 72, 127]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 7]))
        fields.append(Pad5._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 2]))
        fields.append(Pad1._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 127]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 7]))
        fields.append(Pad5._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 2]))
        fields.append(Pad1._pop_from(self.full_header, 'Zeros'))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 127]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 64]))
        fields.append(SelectValue._pop_from(self.full_header, 'Select 19', valid_values=[0, 7]))
        fields.append(Pad170._pop_from(self.full_header, 'Zeros'))

        self.header_fields = fields

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
            control = SingleControl.from_bytes(len(self.controls), bytes, byte_index)
            self.controls.append(control)

        bytes = self.bytes

        for idx, byte in enumerate(file_contents):
            if byte != bytes[idx]:
                raise Exception('bad serializing')

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

    def print_controls(self):
        headers = 'Legend,%s' % (','.join([field.name for field in self.controls[0].fields]))
        print(headers)
        for control in self.controls:
            print(control.csv())

    @classmethod
    def from_spreadsheet(cls, filename):
        wb = load_workbook(filename=filename)
        ws = wb['Controls']
        for row in ws.rows:
            control = SingleControl.from_spreadsheet(row)
            for cell in row:
                print(cell.column)

    def to_spreadsheet(self, filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "Template configuration"

        for idx, field in enumerate(self.header_fields):
            ws.cell(row=idx+1, column=1, value=field.name)
            ws.cell(row=idx+1, column=2, value=str(field))

        wb.create_sheet("Controls")
        ws = wb['Controls']
        ws.cell(row=1, column=1, value='Legend')
        for idx, field in enumerate(self.controls[0].fields):
            ws.cell(row=1, column=idx + 2, value=field.name)
        for idx, control in enumerate(self.controls):
            control.write_to_sheet(ws, idx + 2)

        wb.create_sheet("Control Order")
        ws = wb["Control Order"]

        ws.cell(row=1, column=1, value='section')
        ws.cell(row=1, column=2, value='legend')
        ws.cell(row=1, column=3, value='selector')

        for idx, field in enumerate(indices):
            ws.cell(row=idx+2, column=1, value=field['section'])
            ws.cell(row=idx+2, column=2, value=field['legend'])
            ws.cell(row=idx+2, column=3, value=field['selector'] if 'selector' in field else '')

        wb.save(filename)

    @property
    def bytes(self):
        bytes = bytearray(Template.MESSAGE_START)
        for field in self.header_fields:
            bytes.extend(field.bytes)
        for control in self.controls:
            bytes.extend(control.bytes)
        bytes.extend(Template.MESSAGE_END)
        return bytes

template = Template(sys.argv[1])
# template.print_all(only_unknown=True)
# template.print_fields('unknown3')
# template.print_distinct('unknown3')
# print(template.bytes)
# template.write(sys.argv[2])
template.print_controls()

template.to_spreadsheet('test.xlsx')

template2 = Template.from_spreadsheet('test.xlsx')
