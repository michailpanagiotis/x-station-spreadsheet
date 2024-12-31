#!/usr/bin/env python3
from openpyxl.styles import PatternFill, Font
from openpyxl import Workbook, load_workbook

def assert_workbook_sheets_are_same(ws1, ws2, ignore_columns=(1,)):
    for row in ws1.rows:
        for cell in row:
            if cell.column in ignore_columns:
                continue
            other_cell = ws2.cell(row=cell.row, column=cell.column)
            cell_value = cell.value if cell.value is not None else ""
            other_value = other_cell.value if other_cell.value is not None else ""
            if cell_value != other_value:
                raise Exception('difference at cell %s (%s != %s)' % (cell, cell.value, other_cell.value))

def add_references(from_sheet, to_sheet, compare_columns=('B', 'A'), column_refs=(
    ('D', 'B'), ('E', 'C'), ('F', 'D'), ('G', 'E'), ('H', 'F'), ('I', 'G'), ('J', 'H'), ('N', 'I'), ('O', 'J'), ('P', 'K'), ('Q', 'L'), ('R', 'M'), ('S', 'N'),
)):
    target_cell_range = '%s!$%s$2:$P$1001' % (to_sheet.title, compare_columns[1])
    offset_per_column_letter = {x[0]: to_sheet['%s1' % x[1]].column for x in column_refs}

    for row in from_sheet.rows:
        for cell in row:
            if cell.row > 1 and cell.column_letter in offset_per_column_letter:
                offset = offset_per_column_letter[cell.column_letter]
                cell.value = '=IFERROR(VLOOKUP($B%s,%s,%s,0), "")' % (cell.row, target_cell_range, offset)

def create_sheet(workbook, sheet_name, values_table):
    workbook.create_sheet(sheet_name)
    wst = workbook[sheet_name]
    for row_idx, row_values in enumerate(values_table):
        for col_idx, value in enumerate(row_values):
            wst.cell(row=row_idx + 1, column=col_idx + 1, value=value)
