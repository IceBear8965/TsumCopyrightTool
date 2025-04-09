import openpyxl


class Excel:
    def getData(self, file, sheet_index):
        wb = openpyxl.load_workbook(file)
        if isinstance(sheet_index, int):
            ws = wb.worksheets[sheet_index]
        else:
            ws = wb[sheet_index]

        # manually get max row in sheet
        # max_row = 0
        # for row in ws:
        #     if any(cell.value is not None for cell in row):
        #         max_row += 1
        #
        # # manually get max column in sheet
        # max_column = 0
        # for row in ws:
        #     for column in row:
        #         if column.value is not None:
        #             max_column += 1
        # max_column = int(max_column/max_row)

        max_row = ws.max_row
        max_column = ws.max_column
        values = list(ws.values)
        return values, max_row, max_column

    def getSheets(self, file):
        wb = openpyxl.load_workbook(file, read_only=True)
        return wb.sheetnames


excelHandler = Excel()
