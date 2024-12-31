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


def replace_with_references(values_table, references_table, from_column, to_column, ignore_headers):
    reference_headers = references_table[0]
    headers = values_table[0]

    pointers = {
        from_idx: to_idx + 1
        for from_idx, header in enumerate(headers)
        for to_idx, reference in enumerate(reference_headers)
        if header==reference and header not in ignore_headers
    }

    with_references = []
    for row_idx, row in enumerate(values_table):
        if row_idx == 0:
            with_references.append(row)
        else:
            row_with_references = [
                '=IFERROR(VLOOKUP($B%s,Templates!$A$2:$P$1001,%s,0), "")' % (row_idx + 1, pointers[col_idx]) if col_idx in pointers else x
                for col_idx, x in enumerate(row)
            ]
            with_references.append(row_with_references)
    return with_references


def create_sheet(workbook, sheet_name, values_table):
    workbook.create_sheet(sheet_name)
    wst = workbook[sheet_name]
    for row_idx, row_values in enumerate(values_table):
        for col_idx, value in enumerate(row_values):
            wst.cell(row=row_idx + 1, column=col_idx + 1, value=value)
