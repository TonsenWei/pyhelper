import os
import openpyxl  # pip install openpyxl

project_path = os.path.dirname(os.path.abspath(__file__))


class ExcelUtil:

    @staticmethod
    def get_col_words(excel_path, sheet_index=0, x_from="A", y_from=0):
        wb = openpyxl.load_workbook(excel_path)
        sheet = wb.worksheets[sheet_index]
        words = []
        for i in range(y_from, len(sheet[x_from])):
            value = sheet[x_from][i].value
            if value is not None:
                words.append(value)
                print(value)
        wb.close()
        return words


if __name__ == "__main__":
    ExcelUtil.get_col_words(excel_path=project_path + "\\优化热门中英文歌曲.xlsx", x_from="B", y_from=1)
