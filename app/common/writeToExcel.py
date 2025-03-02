'''
Copyright (C) 2025 IceBear8965

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.
'''

import openpyxl

def writeOutputToExcel(output, file_path):
    outputWorkbook = openpyxl.Workbook()
    outputWorksheet = outputWorkbook.active
    rowIndex = 1
    for item in output:
        outputWorksheet.cell(rowIndex, 1).value = item
        rowIndex += 1

    outputWorkbook.save(file_path + "/output.xlsx")