import openpyxl


class Excel:
    def getData(self, worksheet):
        values = list(worksheet.values)
        max_row = len(values)
        max_column = 0
        for row in values:
            max_column = len(row) if len(row) > max_column else max_column
        return values, max_row, max_column


excelHandler = Excel()
