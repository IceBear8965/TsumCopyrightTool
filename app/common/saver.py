import json

import openpyxl


class Saver:
    def save(self, file_name, data):
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False)
        except Exception:
            return False

    def load(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data
        except Exception:
            return False

    def saveToExcel(self, output, output_folder):
        outputWorkbook = openpyxl.Workbook(write_only=True)
        outputWorksheet = outputWorkbook.create_sheet()
        rowIndex = 1
        for item in output:
            outputWorksheet.append([item])
            rowIndex += 1

        outputWorkbook.save(output_folder + "/output.xlsx")
        outputWorkbook.close()
