import openpyxl
from app.common.parsers.saksParser import parseSaks
from app.common.parsers.sauconyParser import parseSaucony
from app.common.parsers.arenaParser import parseArena

def parseExcel(excel_file, columnIndex, websiteName, filters, order):
    global parsedData
    dataWorkbook = openpyxl.load_workbook(excel_file)
    dataWorksheet = dataWorkbook.active

    sources = []
    for c in list(dataWorksheet.values):
        sources.append(c[columnIndex])

    data = []
    for source in sources:
        try:
            match(websiteName):
                case "Saks85":
                    parsedData = parseSaks(source, filters, order)
                case "Saucony":
                    parsedData = parseSaucony(source)
                case "Arena":
                    parsedData = parseArena(source)
        except Exception:
            parsedData = None
        data.append(parsedData)

    return data