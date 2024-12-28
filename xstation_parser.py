#!/usr/bin/env python3
import json
from openpyxl import Workbook, load_workbook
from fields import define_field, NumericArray, NumericValue, SelectValue, BitMap, StringValue, ZeroPadding, FieldSet

with open('x-station-indices.json', 'r') as f:
    indices = json.loads(f.read())

def get_control_section(idx):
    return indices[idx]['section']

def get_control_physical(idx):
    return indices[idx].get('physical', None)

def get_control_label(idx):
    if 'selector' not in indices[idx]:
        return indices[idx]['legend']
    return '%s (%s)' % (indices[idx]['legend'], indices[idx]['selector'])

def get_control_legend(idx):
    selector = '(%s)' % indices[idx]['selector'] if 'selector' in indices[idx] else ''
    group = '%s%s' % (indices[idx]['section'], selector)
    legend = '%s>%s' % (group, indices[idx]['legend'])
    return legend.strip()

Sysex = define_field(NumericArray, num_bytes=18, name="Sysex")
ControlName = define_field(StringValue, num_bytes=16, name="Name", aliases=['Control name'])
TemplateName = define_field(StringValue, num_bytes=16)
ManufacturerName = define_field(StringValue, num_bytes=13)
Pad1 = define_field(ZeroPadding, num_bytes=1, name="Zeros")
Pad2 = define_field(ZeroPadding, num_bytes=2, name="Zeros")
Pad3 = define_field(ZeroPadding, num_bytes=3, name="Zeros")
Pad4 = define_field(ZeroPadding, num_bytes=4, name="Zeros")
Pad5 = define_field(ZeroPadding, num_bytes=5, name="Zeros")
Pad6 = define_field(ZeroPadding, num_bytes=6, name="Zeros")
Pad7 = define_field(ZeroPadding, num_bytes=7, name="Zeros")
Pad8 = define_field(ZeroPadding, num_bytes=8, name="Zeros")
Pad170 = define_field(ZeroPadding, num_bytes=170, name="Zeros")

CONTROL_FIELDS = [
    ControlName,
    define_field(NumericValue, name="Type", aliases=['Control Type']),
    define_field(NumericValue, name="Low", aliases=['Template', 'Velocity', 'MMC Command']),
    define_field(NumericValue, name="High"),
    define_field(BitMap, ms_name='Ports', ls_name='Button'),
    define_field(NumericValue, name='Pot', aliases=['Pot / Slider Control Type']),
    define_field(NumericValue, name='Display', aliases=['Display type']),
    define_field(NumericValue, name='MSBank', aliases=['NRPN MSBank Num']),
    define_field(NumericValue, name='CC', aliases=['Note']),
    define_field(NumericValue, name='Ch', aliases=['Channel', 'Device id']),
    define_field(NumericValue, name='Default', aliases=['Template', 'Velocity', 'MMC Command']),
    define_field(NumericValue, name='N/A 1'),
    define_field(NumericValue, name='N/A 2'),
    define_field(NumericValue, name='N/A 3'),
    Sysex,
    define_field(NumericValue, name='Step'),
    Pad4,
]

CONTROL_TEMPLATE_FIELDS = [
    define_field(NumericValue, name="Type", aliases=['Control Type']),
    define_field(NumericValue, name="Low", aliases=['Template', 'Velocity', 'MMC Command']),
    define_field(NumericValue, name="High"),
    define_field(BitMap, ms_name='Ports', ls_name='Button'),
    define_field(NumericValue, name='Pot', aliases=['Pot / Slider Control Type']),
    define_field(NumericValue, name='Display', aliases=['Display type']),
    define_field(NumericValue, name='MSBank', aliases=['NRPN MSBank Num']),
    define_field(NumericValue, name='N/A 1'),
    define_field(NumericValue, name='N/A 2'),
    define_field(NumericValue, name='N/A 3'),
    Sysex,
    define_field(NumericValue, name='Step'),
    Pad4,
]

TEMPLATE_FIELDS = [
    define_field(SelectValue, name='N/A 1', valid_values=[8, 17, 19, 24, 25]),
    define_field(SelectValue, name='N/A 2', valid_values=[1, 2, 3, 10]),
    Pad1,
    define_field(NumericValue, name='N/A 3'),
    define_field(TemplateName, name='Name'),
    define_field(NumericValue, name='N/A 4'),
    define_field(ManufacturerName, name='Manufacturer'),
    define_field(SelectValue, name='Channel', valid_values=[0, 16]),
    define_field(SelectValue, name='Midi port | Keyb MIDI Chan', valid_values=[0, 16, 48, 53, 54, 112]),
    Pad2,
    define_field(SelectValue, name='Velocity curve', valid_values=[0, 1, 2, 3]),
    define_field(SelectValue, name='Select 2', valid_values=[4, 5]),
    define_field(SelectValue, name='Aftertouch | Auto Snapshot | Not Synth', valid_values=[0, 1, 2, 3, 4, 5, 6, 7]),
    define_field(NumericValue, name='Override MIDI Ch'),
    define_field(SelectValue, name='Touchpad X Type', valid_values=[0, 1, 2]),
    define_field(SelectValue, name='Touchpad Y Type', valid_values=[0, 1, 2]),
    Pad2,
    define_field(SelectValue, name='Select 6', valid_values=[48, 64, 79]),
    define_field(SelectValue, name='Select 7', valid_values=[0, 64]),
    Pad2,
    define_field(SelectValue, name='Select 8', valid_values=[64, 78]),
    define_field(SelectValue, name='Select 9', valid_values=[64, 127]),
    Pad2,
    define_field(SelectValue, name='Select 10', valid_values=[64]),
    define_field(SelectValue, name='Select 11', valid_values=[127]),
    Pad3,
    define_field(SelectValue, name='Select 12', valid_values=[0,1]),
    define_field(SelectValue, name='Select 13', valid_values=[0,49]),
    define_field(SelectValue, name='Select 14', valid_values=[64,68]),
    define_field(SelectValue, name='Select 15', valid_values=[43,64]),
    define_field(SelectValue, name='Select 16', valid_values=[127]),
    Pad6,
    define_field(SelectValue, name='Select 17', valid_values=[0,18]),
    define_field(SelectValue, name='Select 18', valid_values=[3,5]),
    define_field(SelectValue, name='Select 19', valid_values=[90]),
    define_field(SelectValue, name='Select 19', valid_values=[0,64]),
    Pad7,
    define_field(SelectValue, name='Select 19', valid_values=[0,1]),
    define_field(SelectValue, name='Select 19', valid_values=[20]),
    define_field(SelectValue, name='Select 19', valid_values=[64]),
    define_field(SelectValue, name='Select 19', valid_values=[64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    Pad5,
    define_field(SelectValue, name='Select 19', valid_values=[64]),
    Pad1,
    define_field(SelectValue, name='Select 19', valid_values=[64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 32]),
    Pad1,
    define_field(SelectValue, name='Select 19', valid_values=[127]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    Pad1,
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    Pad3,
    define_field(SelectValue, name='Select 19', valid_values=[100]),
    define_field(SelectValue, name='Select 19', valid_values=[64]),
    Pad3,
    define_field(SelectValue, name='Select 19', valid_values=[52, 64]),
    define_field(SelectValue, name='Select 19', valid_values=[64, 78]),
    define_field(SelectValue, name='Select 19', valid_values=[64, 72]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    Pad6,
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    Pad4,
    define_field(SelectValue, name='Select 19', valid_values=[64]),
    define_field(SelectValue, name='Select 19', valid_values=[64]),
    define_field(SelectValue, name='Select 19', valid_values=[127]),
    Pad2,
    define_field(SelectValue, name='Select 19', valid_values=[0, 64, 78]),
    Pad4,
    define_field(SelectValue, name='Select 19', valid_values=[3, 4]),
    define_field(SelectValue, name='Select 19', valid_values=[90]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    Pad8,
    define_field(SelectValue, name='Select 19', valid_values=[20]),
    define_field(SelectValue, name='Select 19', valid_values=[64]),
    define_field(SelectValue, name='Select 19', valid_values=[64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64, 74]),
    Pad1,
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    Pad2,
    define_field(SelectValue, name='Select 19', valid_values=[0, 127]),
    define_field(SelectValue, name='Select 19', valid_values=[6, 44, 64]),
    Pad1,
    define_field(SelectValue, name='Select 19', valid_values=[64, 127]),
    define_field(SelectValue, name='Select 19', valid_values=[0,32]),
    Pad1,
    define_field(SelectValue, name='Select 19', valid_values=[96, 127]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    Pad1,
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    Pad2,
    define_field(SelectValue, name='Select 19', valid_values=[0, 36]),
    define_field(SelectValue, name='Select 19', valid_values=[100]),
    define_field(SelectValue, name='Select 19', valid_values=[64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64, 65]),
    Pad2,
    define_field(SelectValue, name='Select 19', valid_values=[0, 64, 98]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64, 74]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    Pad6,
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    Pad3,
    define_field(SelectValue, name='Select 19', valid_values=[0, 1]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 1]),
    define_field(SelectValue, name='Midi port', valid_values=[0, 112]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 2]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 56]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 60, 127]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 7]),
    Pad4,
    define_field(SelectValue, name='Midi port', valid_values=[0, 112]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 2]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 69]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 72, 127]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 7]),
    Pad5,
    define_field(SelectValue, name='Select 19', valid_values=[0, 2]),
    Pad1,
    define_field(SelectValue, name='Select 19', valid_values=[0, 127]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 7]),
    Pad5,
    define_field(SelectValue, name='Select 19', valid_values=[0, 2]),
    Pad1,
    define_field(SelectValue, name='Select 19', valid_values=[0, 127]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 64]),
    define_field(SelectValue, name='Select 19', valid_values=[0, 7]),
    Pad170,
]


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
    "Trigger": "1,127,0,01110000,4,64,0,0,0,0,000000000000000000000000000000000000,0,4",
    "Toggle": "1,0,127,01111000,4,64,0,0,0,0,000000000000000000000000000000000000,0,4",
    "Momentary": "1,0,127,01110100,0,0,0,0,0,0,000000000000000000000000000000000000,0,4",
    "Continuous": "1,0,127,01110000,0,0,0,0,0,0,000000000000000000000000000000000000,0,4",
    "ContinuousPickup": "1,0,127,01110000,9,64,0,0,0,0,000000000000000000000000000000000000,0,4",
    "Unary": "1,63,64,01110000,0,65,0,0,0,0,000000000000000000000000000000000000,0,4",
    "Jog": "1,63,65,01110000,0,65,0,0,0,0,000000000000000000000000000000000000,0,4",
    "Pitch": "10,0,127,01110000,0,1,0,0,0,0,000000000000000000000000000000000000,0,4",
    "-": "0,0,127,01110000,0,64,0,0,0,0,000000000000000000000000000000000000,0,4",
}

class SingleControl(FieldSet):
    @classmethod
    def from_bytes(cls, *args, **kwargs):
        return super(SingleControl, cls).from_bytes(CONTROL_FIELDS, *args, **kwargs)

    @classmethod
    def from_values(cls, *args, **kwargs):
        return super(SingleControl, cls).from_values(CONTROL_FIELDS, *args, **kwargs)

    @classmethod
    def from_spreadsheet(cls, idx, row):
        (legend, template, *values) = (c.value for c in row)
        return super(SingleControl, cls).from_values(CONTROL_FIELDS, values, index=idx)

    def __init__(self, fields, index):
        super().__init__(fields)
        self.index = index

    def get_template(self):
        return self.get_subset(CONTROL_TEMPLATE_FIELDS)

    def to_spreadsheet(self, ws, row_number, template_name):
        ws.cell(row=row_number, column=1, value=get_control_legend(row_number - 2))
        ws.cell(row=row_number, column=2, value=template_name)

        template = self.get_subset(CONTROL_TEMPLATE_FIELDS)

        for idx, field in enumerate(self.fields):
            pos = template.find_index(field.name)
            value = '=IFERROR(VLOOKUP($B%s,Templates!$A$2:$P$1001,%s,0), "")' % (row_number, pos + 2) if pos is not None else str(field)
            if value is None:
                raise Exception('value is required')
            ws.cell(row=row_number, column=idx + 3, value=value)

    def get_references(self, other_fieldset_definition=CONTROL_TEMPLATE_FIELDS):
        other_fields = self.get_subset(CONTROL_TEMPLATE_FIELDS)
        references = []
        for idx, field in enumerate(self.fields):
            other_idx = other_fields.find_index(field.name)
            if other_idx is not None:
                references.append((idx, other_idx))
        return references

    def to_realearn_dict(self, idx):
        id = '%s. %s' % (idx, get_control_legend(idx))
        control = {
          "id": id,
          "name": get_control_label(idx),
          "groupId": get_control_section(idx),
          "source": {
            **REALEARN_CONTROL_SOURCE_COMMON,
            "character": 1 if get_control_physical(idx) == 'Button' else 0,
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
                "controlElementType": "Button" if get_control_physical(idx) == 'Button' else None,
                "controlElementIndex": "%s-%s" % (get_control_section(idx), get_control_label(idx)),
          },
          "feedbackIsEnabled": False,
          "visibleInProjection": False
        }
        return control

class Template():
    LINE_SIZE = 52
    MESSAGE_START=b'\xf0\x00 )\x02\x00\x7f\x00\x00'
    MESSAGE_END=b'\x124\xf7'

    def __init__(self, header_fields, controls, sysex=None):
        self.header_fields = header_fields
        self.controls = controls
        self.sysex = sysex

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
        full_header = bytearray(body[:offset]) # 396 bytes
        controls_bytes = body[len(full_header):] # 52 x 149 = 7748 bytes

        if len(full_header) != 396:
            raise Exception('bad header bytes length')

        instance = cls(
            header_fields=[
                ct._pop_from(full_header)
                for ct in TEMPLATE_FIELDS
            ],
            controls = [
                SingleControl.from_bytes(bytearray(controls_bytes[i:i + cls.LINE_SIZE]), index=idx)
                for idx, i in enumerate(range(0, len(controls_bytes), cls.LINE_SIZE))
            ],
            sysex = body
        )

        bytes = instance.bytes

        for idx, byte in enumerate(file_contents):
            if byte != bytes[idx]:
                raise Exception('bad serializing %s %s' % (byte, bytes[idx]))

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

    @staticmethod
    def extract_templates(controls):
        permutations = {bytes(t.get_subset(CONTROL_TEMPLATE_FIELDS).bytes) for t in controls}
        known = [FieldSet.from_csv(CONTROL_TEMPLATE_FIELDS, csv, name=name) for name, csv in KNOWN_TEMPLATES.items()]
        templates = []
        for idx, x in enumerate(permutations):
            name = 'template%s' % idx
            template = FieldSet.from_bytes(CONTROL_TEMPLATE_FIELDS, bytearray(x), name)
            match = next((x for x in known if x == template), None)
            if match:
                template.name = match.name
            templates.append(template)
        return templates

    def __templates_to_spreadsheet(self, wb):
        wb.create_sheet("Templates")
        wst = wb['Templates']
        for idx, field in enumerate(self.controls[0].get_subset(CONTROL_TEMPLATE_FIELDS).fields):
            wst.cell(row=1, column=idx + 2, value=field.name)
        wst.cell(row=1, column=len(self.controls[0].get_subset(CONTROL_TEMPLATE_FIELDS).fields) + 2, value='Bytes')
        templates = self.extract_templates(self.controls)
        for idx, template in enumerate(templates):
            template.to_spreadsheet(wst, idx + 2)
            print(template)
        return templates

    def to_spreadsheet(self, filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "Template configuration"

        for idx, field in enumerate(self.header_fields):
            ws.cell(row=idx+1, column=1, value=field.name)
            ws.cell(row=idx+1, column=2, value=str(field))

        templates = self.__templates_to_spreadsheet(wb)

        wb.create_sheet("Controls")
        ws = wb['Controls']
        ws.cell(row=1, column=1, value='Legend')
        ws.cell(row=1, column=2, value='Template')
        for idx, name in enumerate(self.controls[0].get_field_names()):
            ws.cell(row=1, column=idx + 3, value=name)

        for idx, control in enumerate(self.controls):
            found_template = next((x for x in templates if x == control.get_subset(CONTROL_TEMPLATE_FIELDS)), None)

            if not found_template:
                raise Exception('unknown template')

            control.to_spreadsheet(ws, idx + 2, found_template.name)

        wb.save(filename)
        wb.close()

    def to_json(self, filename):
        id = self.name
        groups = {get_control_section(idx) for idx, c in enumerate(self.controls) if get_control_section(idx) != ''}
        main = {
          "version": "2.16.14",
          "name": "x-station",
          "defaultGroup": {},
          "groups": [{"id": s, "name": s} for s in groups],
          "mappings": [c.to_realearn_dict(idx) for idx, c in enumerate(self.controls) if get_control_physical(idx) is not None],
        }
        with open(filename, "w") as f:
            f.write(json.dumps(main, indent=2))

    def __get_control_legend(self, idx):
        selector = '(%s)' % indices[idx]['selector'] if 'selector' in indices[idx] else ''
        group = '%s%s' % (indices[idx]['section'], selector)
        legend = '%s>%s' % (group, indices[idx]['legend'])
        return legend.strip()

    def get_control_values(self):
        return [control.get_values() for control in self.controls]

    def to_sql(self):
        templates = self.extract_templates(self.controls)

        values = [
            [
                get_control_legend(idx),
                next((x.name for x in templates if x == control.get_subset(CONTROL_TEMPLATE_FIELDS)), None),
            ] +  control.get_values()
            for idx, control in enumerate(self.controls)
        ]

        for value in values:
            print(value)

        # for control in self.controls:
        #     refs = control.get_references()
        #     print(refs)

        return values

    def control_permutations(self, field_name):
        return {str(c[field_name]) for c in self.controls}

    def diff(self, other):
        template_diffs = []
        field_diffs = []

        other_headers = other.header_fields
        for idx, control in enumerate(self.header_fields):
            if control != other_headers[idx]:
                template_diffs.append([idx, control, other_headers[idx]])

        other_controls = other.controls
        for idx, control in enumerate(self.controls):
            for field_idx, field in enumerate(control.fields):
                other_field = other_controls[idx].fields[field_idx]
                if field != other_field:
                    field_diffs.append([idx, field_idx, field.name, str(field), str(other_field)])

        print('TEMPLATE DIFFS', template_diffs)
        print('FIELD DIFFS', field_diffs)
