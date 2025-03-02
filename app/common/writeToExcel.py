import openpyxl

def writeOutputToExcel(output, file_path):
    outputWorkbook = openpyxl.Workbook()
    outputWorksheet = outputWorkbook.active
    rowIndex = 1
    for item in output:
        outputWorksheet.cell(rowIndex, 1).value = item
        rowIndex += 1

    outputWorkbook.save(file_path + "/output.xlsx")