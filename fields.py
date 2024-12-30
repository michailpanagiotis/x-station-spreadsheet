#!/usr/bin/env python3
import re
import string
from bitstring import Bits

class RawBytes():
    DEFAULTS = {
        "name": None,
        "stuffed": None,
        "aliases": (),
        "valid_values": (),
    }

    @classmethod
    def get_name(cls):
        if cls.DEFAULTS['stuffed']:
            name = '|'.join((x[0] for x in cls.DEFAULTS["stuffed"]))
            return name
        return cls.DEFAULTS['name']

    @classmethod
    def get_length(cls):
        return cls.NUM_BYTES

    @classmethod
    def _pop_from(cls, other_bytes, *args, **kwargs):
        num_bytes = cls.NUM_BYTES

        instance = cls(other_bytes[:num_bytes], *args, **kwargs)

        if isinstance(other_bytes, bytearray):
            for _ in range(len(instance)):
                other_bytes.pop(0)

        return instance

    @classmethod
    def parse_string(cls, string):
        raise Exception('not implemented for %s' % cls.__name__)

    def __init__(self, value, name=None, *args, **kwargs):
        if value is None:
            raise Exception('value is required')
        if isinstance(value, bytearray) or isinstance(value, bytes):
            if len(value) != type(self).NUM_BYTES:
                raise Exception('bad number of bytes')
            self.bytes = bytearray(value)
        else:
            self.bytes = type(self).parse_string(value)
            if not isinstance(self.bytes, bytearray):
                raise Exception('parsing should return a bytearray but got %s %s' % (self.bytes, type(self.bytes)))

        self.name = name if name is not None else type(self).DEFAULTS['name']
        for argname in ['stuffed', 'valid_values', 'aliases']:
            setattr(self, argname, kwargs[argname] if argname in kwargs else type(self).DEFAULTS[argname])

        if self.stuffed:
            self.name = '|'.join((x[0] for x in self.stuffed))

        if len(self.valid_values) > 0:
            for byte in self.bytes:
               if byte not in self.valid_values:
                    raise Exception('unsupported option for %s (%s)' % (type(self), byte))


    def __str__(self):
        return ''.join([hex(x) for x in self.bytes])

    def __len__(self):
        return len(self.bytes)

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        for idx, byte in enumerate(self.bytes):
            if byte != other.bytes[idx]:
                return False
        return True


class SingleByte(RawBytes):
    NUM_BYTES = 1

    @classmethod
    def parse_string(cls, string):
        return bytearray([int(string)])

class NumericValue(SingleByte):
    def __str__(self):
        return str(self.bytes[0])

class NumericArray(RawBytes):
    @classmethod
    def parse_string(cls, string):
        return bytearray(bytes.fromhex(string))

    def __str__(self):
        return self.bytes.hex()


class SelectValue(NumericValue):
    def __init__(self, *args, **kwargs):
        if len(type(self).DEFAULTS["valid_values"]) == 0:
            raise Exception("select with no valid values")
        super().__init__(*args, **kwargs)

class StringValue(RawBytes):
    @classmethod
    def parse_string(cls, string):
        return bytearray(string.encode('ascii').ljust(cls.NUM_BYTES, b' '))

    def __str__(self):
        return ''.join([chr(x) for x in self.bytes if chr(x) in string.printable]).rstrip()

class ZeroPadding(RawBytes):
    DEFAULTS = {
        **RawBytes.DEFAULTS,
        "valid_values": (0,),
    }

    @classmethod
    def parse_string(cls, string):
        return bytearray(b'\x00') * cls.NUM_BYTES

    def __str__(self):
        return str(len(self))

class BitMap(SingleByte):
    @classmethod
    def parse_string(cls, string):
        return bytearray(Bits(bin=string).bytes)

    def __repr__(self):
        formatted = "{:08b}".format(self.bytes[0])
        return '<%s:%s|%s:%s>' % (self.ms_name, formatted[:4], self.ls_name, formatted[4:])

    def __str__(self):
        return Bits(uint=self.bytes[0], length=8).bin

def define_field(base_cls, num_bytes=None, **defaults):
    name = defaults["name"] if "name" in defaults else ""
    return type(name, (base_cls,), {
        "NUM_BYTES": num_bytes if num_bytes is not None else base_cls.NUM_BYTES,
        "DEFAULTS": {**base_cls.DEFAULTS, **defaults},
    })


class FieldSet():
    @classmethod
    def from_values(cls, definition, values, *args, **kwargs):
        fields = []
        for idx, ct in enumerate(definition):
            fields.append(ct(values[idx] if values[idx] is not None else "") )
        return cls(fields, *args, **kwargs)

    @classmethod
    def from_csv(cls, definition, string, *args, **kwargs):
        values = string.split(',')
        return cls.from_values(definition, values, *args, **kwargs)

    @classmethod
    def from_bytes(cls, definition, sysex, *args, **kwargs):
        # important to be bytearray (mutable)
        if not isinstance(sysex, bytearray):
            raise Exception('expecting a bytearray instance')
        if len(sysex) != sum(j.get_length() for j in definition):
            raise Exception('bad length')

        fields = [ct._pop_from(sysex) for ct in definition]

        if len(sysex) != 0:
            raise Exception('non parsed fields')
        return cls(fields, *args, **kwargs)

    def __init__(self, fields, name=None):
        self._name = name
        self.fields = fields

    @property
    def name(self):
        name = next((str(x) for x in self.fields if x.name == 'Name'), None)
        return name if name else self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def bytes(self):
        bytes = bytearray()
        for field in self.fields:
            bytes.extend(field.bytes)
        return bytes

    @property
    def csv(self):
        return ','.join([str(x) for x in self.fields])

    def __len__(self):
        return len(self.bytes)

    def __str__(self):
        return '<%s: %s>' % (self.name, self.csv)

    def __getitem__(self, key):
        field = next((x for x in self.fields if x.name == key), None)
        if field is None:
            raise KeyError
        return field

    def __eq__(self, other):
        return self.bytes == other.bytes

    def get_field_names(self):
        return [field.name for field in self.fields]

    def find_index(self, field_name):
        for idx, field in enumerate(self.fields):
            if field.name == field_name:
                return idx
        return None

    def get_values(self):
        values = ([str(f) for f in self.fields])
        return values

    def get_subset(self, subset_definitions):
        values = []
        for definition in subset_definitions:
            name = definition.get_name()
            values.append(str(self[name]))

        return FieldSet.from_values(subset_definitions, values)

    def to_spreadsheet(self, ws, row_number):
        ws.cell(row=row_number, column=1, value=self.name.strip())
        for idx, field in enumerate(self.fields):
            value = str(field)
            if value is None:
                raise Exception('value is required')
            ws.cell(row=row_number, column=idx + 2, value=value)
        ws.cell(row=row_number, column=len(self.fields) + 2, value=self.bytes.hex())

    def dereference(self, values):
        flat_values = []
        for value in values:
            if value is None:
                flat_values.append("")
            elif value.startswith("="):
                match = re.search('\$[A-Z]\$\d+:\$[A-Z]\$\d+,\s*(?P<index>\d+),', value)
                if not match:
                    print(self, value)
                field_index = int(match.group('index')) - 2
                flat_values.append(str(self.fields[field_index]))
            else:
                flat_values.append(value)
        return flat_values


class ControlSet():
    def __init__(self, fieldset_array):
        self.controls = fieldset_array

class Reference():
    def __init__(self, index):
        self.index = index

    def to_spreadsheet(self, row_number):
        return '=IFERROR(VLOOKUP($B%s,Templates!$A$2:$P$1001,%s,0), "")' % (row_number, self.index)

    def __repr__(self):
        return 'r#%s' % self.index
