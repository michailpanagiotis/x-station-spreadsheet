#!/usr/bin/env python3
import argparse
import json
import sys
from openpyxl import Workbook, load_workbook
from pathlib import Path
from fields import CONTROL_FIELDS, TEMPLATE_FIELDS

with open('x-station-indices.json', 'r') as f:
    indices = json.loads(f.read())

REALEARN_TARGET_DUMMY = {
    "type": 53,
    "fxAnchor": "id",
    "useSelectionGanging": False,
    "useTrackGrouping": False,
    "seekBehavior": "Immediate",
    "useProject": False,
    "moveView": False,
    "seekPlay": False,
    "oscArgIndex": 0,
    "mouseAction": { "kind": "MoveTo", "axis": "X" },
    "takeMappingSnapshot": { "kind": "LastLoaded" }
}

REALEARN_BUTTON_DESIGN = {
    "background": { "kind": "Color" },
    "foreground": { "kind": "None" },
    "static_text": ""
}

REALEARN_CONTROL_SOURCE_COMMON = {
    "isRegistered": False,
    "is14Bit": False,
    "oscArgIndex": 0,
    "buttonIndex": 0,
    "buttonDesign": REALEARN_BUTTON_DESIGN,
}

REALEARN_CONTROL_TARGET_COMMON = {
    "category": "virtual",
    "fxAnchor": "id",
    "useSelectionGanging": False,
    "useTrackGrouping": False,
    "seekBehavior": "Immediate",
    "learnable": False,
    "mouseAction": {
      "kind": "MoveTo",
      "axis": "X"
    },
    "pollForFeedback": False,
    "takeMappingSnapshot": {
      "kind": "ById",
      "id": ""
    }
}

KNOWN_TEMPLATES = {
    "Trigger": bytearray.fromhex("017f00700440000000000000000000000000000000000000000000000000000000"),
    "Toggle": bytearray.fromhex("01007f780440000000000000000000000000000000000000000000000000000000"),
    "Continuous": bytearray.fromhex("01007f700040000000000000000000000000000000000000000000000000000000"),
    "Unary": bytearray.fromhex("013f40700041000000000000000000000000000000000000000000000000000000"),
    "Jog": bytearray.fromhex("013f41700041000000000000000000000000000000000000000000000000000000"),
    "Pitch": bytearray.fromhex("0a007f700041000000000000000000000000000000000000000000000000000000"),
    "-": bytearray.fromhex("00007f700040000000000000000000000000000000000000000000000000000000"),
}

class FieldSet():
    def __init__(self, fields, name=None):
        self.name = name
        self.fields = fields

    @property
    def bytes(self):
        bytes = bytearray()
        for field in self.fields:
            bytes.extend(field.bytes)
        return bytes

    def __len__(self):
        return len(self.bytes)

    def __getitem__(self, key):
        field = next((x for x in self.fields if x.name == key), None)
        if field is None:
            raise KeyError
        return field

    def __eq__(self, other):
        return self.bytes == other.bytes

    def get_field_position(self, field_name):
        for idx, field in enumerate(self.fields):
            if field.name == field_name:
                return idx
        return None

    def to_spreadsheet(self, ws, row_number):
        ws.cell(row=row_number, column=1, value=self.name.strip())
        for idx, field in enumerate(self.fields):
            value = str(field)
            if value is None:
                raise Exception('value is required')
            ws.cell(row=row_number, column=idx + 2, value=value)
        ws.cell(row=row_number, column=len(self.fields) + 2, value=self.bytes.hex())

    def get_known_template_name(self):
        return next((template_name for template_name, template_bytes in KNOWN_TEMPLATES.items() if template_bytes == self.bytes), None)

class SingleControl(FieldSet):
    def __init__(self, idx, fields):
        name = next(x.bytes for x in fields if x.name == 'Name')
        self.index = idx
        self.full_name = ''.join([chr(x) for x in name])
        self.name = self.full_name.strip()
        self.fields = fields

    def __str__(self):
        return '%s' % (' '.join([str(x) for x in self.fields]))

    def get_template(self):
        return FieldSet([x for x in self.fields if x.name not in ('Name', 'CC', 'Ch', 'Default')])

    @property
    def section(self):
        return indices[self.index]['section']

    @property
    def group(self):
        selector = '(%s)' % indices[self.index]['selector'] if 'selector' in indices[self.index] else ''
        group = '%s%s' % (indices[self.index]['section'], selector)
        return group

    @property
    def label(self):
        if 'selector' not in indices[self.index]:
            return indices[self.index]['legend']
        return '%s (%s)' % (indices[self.index]['legend'], indices[self.index]['selector'])

    @property
    def physical(self):
        return indices[self.index].get('physical', None)

    @property
    def legend(self):
        legend = '%s>%s' % (self.group, indices[self.index]['legend'])
        return legend

    @classmethod
    def from_sysex(cls, idx, cmd):
        if isinstance(cmd, bytes):
            if len(cmd) != 52:
                raise Exception('bad length')

            cmd = bytearray(cmd)

        fields = [ct._pop_from(cmd) for ct in CONTROL_FIELDS]

        if len(cmd) != 0:
            raise Exception('non parsed fields')

        return cls(idx, fields)

    @classmethod
    def from_spreadsheet(cls, idx, row):
        (legend, template, *values) = (c.value for c in row)
        fields = [ct(values[idx] if values[idx] is not None else "") for idx, ct in enumerate(CONTROL_FIELDS)]
        return cls(idx, fields)

    def to_spreadsheet(self, ws, row_number, template_name):
        ws.cell(row=row_number, column=1, value=self.legend.strip())
        ws.cell(row=row_number, column=2, value=template_name)

        template = self.get_template()

        for idx, field in enumerate(self.fields):
            pos = template.get_field_position(field.name)
            if pos is not None:
                value = '=IFERROR(VLOOKUP($B%s,Templates!$A$2:$P$1001,%s,0), "")' % (row_number, pos + 2)
            else:
                value = str(field)
            if value is None:
                raise Exception('value is required')
            ws.cell(row=row_number, column=idx + 3, value=value)

    def to_realearn_dict(self):
        id = '%s. %s' % (self.index, self.legend)
        control = {
          "id": id,
          "name": self.label,
          "groupId": self.section,
          "source": {
            **REALEARN_CONTROL_SOURCE_COMMON,
            "character": 1 if self.physical == 'Button' else 0,
            "channel": int(str(self['Ch'])),
            "number": int(str(self['CC'])),
          },
          "mode": {
            "maxStepSize": 0.05,
            "minStepFactor": 1,
            "maxStepFactor": 5,
            "takeoverMode": "pickup-tolerant"
          },
          "target": {
                **REALEARN_CONTROL_TARGET_COMMON,
                "controlElementType": "Button" if self.physical == 'Button' else None,
                "controlElementIndex": self.label,
          },
          "feedbackIsEnabled": False,
          "visibleInProjection": False
        }
        return control

class Template():
    LINE_SIZE = 52
    MESSAGE_START=b'\xf0\x00 )\x02\x00\x7f\x00\x00'
    MESSAGE_END=b'\x124\xf7'

    def __init__(self, header_fields, controls):
        self.header_fields = header_fields
        self.controls = controls

    @property
    def bytes(self):
        bytes = bytearray(Template.MESSAGE_START)
        for field in self.header_fields:
            bytes.extend(field.bytes)
        for control in self.controls:
            bytes.extend(control.bytes)
        bytes.extend(Template.MESSAGE_END)
        return bytes

    def __getitem__(self, key):
        field = next((x for x in self.header_fields if x.name == key), None)
        if field is None:
            raise KeyError
        return field

    def __str__(self):
       return '\n'.join([str(x) for x in self.controls])

    def __len__(self):
        return len(self.bytes)

    def __eq__(self, other):
        if not isinstance(other, Template):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if len(self) != len(other):
            return False

        for idx, byte in enumerate(self.bytes):
            if byte != other.bytes[idx]:
                return False
        return True

    @property
    def name(self):
        name = next(str(x) for x in self.header_fields if x.name == 'Name')
        manufacturer = next(str(x) for x in self.header_fields if x.name == 'Manufacturer')
        return ('%s %s' % (manufacturer.strip(), name.strip())).strip()

    @property
    def unknowns(self):
        return [x for x in self.controls if x.section == '']

    def diff_headers(self, other):
        for idx, header in enumerate(self.header_fields):
            other_header = other.header_fields[idx]
            for byte_index, byte in enumerate(header.bytes):
                if byte != other_header.bytes[byte_index]:
                    print('-', idx + 1, header.name, header,'---->', other_header)
                    break

    def compare_unknowns(self, other):
        other_unknowns = other.controls
        for idx, control in enumerate(self.controls):
            other_control = other_unknowns[idx]
            for field_index, field in enumerate(control.fields):
                if field.name not in ('Name', 'Ch', 'CC', 'Display', 'Type', 'Pot'): # 'Name', 'Low', 'High', 'Ch', 'MSBank', 'Sysex'):
                    other_field = other_control.fields[field_index]
                    if field != other_field:
                        print(control.index + 2, control.legend, field.name, str(field), '---->', str(other_field))

    @classmethod
    def from_sysex(cls, filename):
        with open(filename, "rb") as f:
            file_contents = f.read()

        if file_contents[:len(Template.MESSAGE_START)] != Template.MESSAGE_START:
            raise Exception('bad header')

        if file_contents[-len(Template.MESSAGE_END):] != Template.MESSAGE_END:
            raise Exception('bad footer')

        body = file_contents[len(Template.MESSAGE_START):-len(Template.MESSAGE_END)]
        offset = 405 - len(Template.MESSAGE_START)
        full_header = bytearray(body[:offset])
        controls = body[len(full_header):]

        if len(full_header) != 396:
            raise Exception('bad header bytes length')

        instance = cls(
            header_fields=[
                ct._pop_from(full_header)
                for ct in TEMPLATE_FIELDS
            ],
            controls = [
                SingleControl.from_sysex(idx, controls[i:i + cls.LINE_SIZE])
                for idx, i in enumerate(range(0, len(controls), cls.LINE_SIZE))
            ],
        )

        bytes = instance.bytes

        for idx, byte in enumerate(file_contents):
            if byte != bytes[idx]:
                raise Exception('bad serializing')

        return instance

    def to_sysex(self, file):
        with open(file, "wb") as f:
            f.write(self.bytes)

    @classmethod
    def from_spreadsheet(cls, filename):
        wb = load_workbook(filename=filename, data_only=True)
        ws = wb['Template configuration']
        header_fields = [TEMPLATE_FIELDS[idx](row[1].value if row[1].value is not None else "") for idx, row in enumerate(ws.rows)]

        ws = wb['Controls']
        controls = [SingleControl.from_spreadsheet(idx - 1, row) for idx, row in enumerate(ws.rows) if idx > 0]
        return cls(header_fields, controls)


    def to_spreadsheet(self, filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "Template configuration"

        for idx, field in enumerate(self.header_fields):
            ws.cell(row=idx+1, column=1, value=field.name)
            ws.cell(row=idx+1, column=2, value=str(field))

        wb.create_sheet("Templates")
        wst = wb['Templates']
        for idx, field in enumerate(self.controls[0].get_template().fields):
            wst.cell(row=1, column=idx + 2, value=field.name)
        wst.cell(row=1, column=len(self.controls[0].get_template().fields) + 2, value='Bytes')


        wb.create_sheet("Controls")
        ws = wb['Controls']
        ws.cell(row=1, column=1, value='Legend')
        ws.cell(row=1, column=2, value='Template')
        for idx, field in enumerate(self.controls[0].fields):
            ws.cell(row=1, column=idx + 3, value=field.name)
        templates = []
        for idx, control in enumerate(self.controls):
            found_template = None
            for template in templates:
                if control.get_template() == template:
                    found_template = template

            if not found_template:
                found_template = control.get_template()
                known_name = found_template.get_known_template_name()
                found_template.name = known_name if known_name is not None else 'template %s' % (idx + 1)
                found_template.to_spreadsheet(wst, len(templates) + 2)
                templates.append(found_template)

            control.to_spreadsheet(ws, idx + 2, found_template.name)

        wb.save(filename)

    def to_json(self, filename):
        id = self.name
        groups = {c.section for c in self.controls if c.section != ''}
        main = {
          "kind": "Instance",
          "version": "2.16.14",
          "value": {
            "mainUnit": {
              "version": "2.16.14",
              "id": id,
              "name": "Main",
              "stayActiveWhenProjectInBackground": "OnlyIfBackgroundProjectIsRunning",
              "livesOnUpperFloor": False,
              "controlDeviceId": "0",
              "defaultGroup": {},
              "controllerGroups": [{"id": s, "name": s} for s in groups],
              "defaultControllerGroup": {},
              "controllerMappings": [c.to_realearn_dict() for c in self.controls if c.physical is not None],
              "instanceFx": {
                "address": "Focused"
              }
            },
            "additionalUnits": []
          }
        }
        with open(filename, "w") as f:
            f.write(json.dumps(main, indent=2))

parser = argparse.ArgumentParser(
    prog='x-station-sheet',
    description='Converts from Novation X-station Sysex to Excel files and back',
)

parser.add_argument('command', choices=['xlsx', 'syx', 'json'])
parser.add_argument('filename')
parser.add_argument("--output", help="output")
args = parser.parse_args()

path = Path(args.filename).absolute()

if args.command == 'xlsx':
    if path.suffix != '.syx':
        raise Exception('expecting a \'*.syx\' file as input')
    output = args.output if args.output else path.with_suffix('.xlsx')
    template = Template.from_sysex(path)
    template.to_spreadsheet(output)
elif args.command == 'syx':
    if path.suffix != '.xlsx':
        raise Exception('expecting a \'*.xlsx\' file as input')
    output = args.output if args.output else path.with_suffix('.syx')
    template = Template.from_spreadsheet(path)
    template.to_sysex(output)
elif args.command == 'json':
    if path.suffix != '.xlsx':
        raise Exception('expecting a \'*.xlsx\' file as input')
    output = args.output if args.output else path.with_suffix('.json')
    template = Template.from_spreadsheet(path)
    template.to_json(output)
else:
    raise Exception('unknown command')
