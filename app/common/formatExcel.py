import openpyxl
from app.common.addDots import addDots
from app.common.sortInput import sortInput

def formatExcel(excel_file, columnIndex, filters, paramorder):
    dataWorkbook = openpyxl.load_workbook(excel_file)
    dataWorksheet = dataWorkbook.active

    data = []
    for c in list(dataWorksheet.values):
        data.append(c[columnIndex])
    sortData = []
    for d in data:
        if d is not None:
            sortData.append(d)
    firstItem = sortData.pop(0)

    output = []
    for d in sortData:
        sorted = sortInput(d.split("\n"), filters, paramorder)
        dotted = addDots(sorted)
        output.append(dotted)
    output.insert(0, firstItem)

    return output