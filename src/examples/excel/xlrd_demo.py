import os
import xlrd  # 读取xls，不能读取xlsx, pip install xlrd
import openpyxl  # pip install openpyxl


project_path = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    print("start read xlsx...")
#     readbook = xlrd.open_workbook(project_path + r'\优化热门中英文歌曲.xlsx')
#     sheet = readbook.sheet_by_index(0)#索引的方式，从0开始
# # 　　sheet = readbook.sheet_by_name('sheet2') # 名字的方式
#     songs_name = sheet.col_values(1)
#     print(songs_name)
    wb = openpyxl.load_workbook(project_path + r'\优化热门中英文歌曲.xlsx')
    sheet1 = wb.worksheets[0]
    # sheet1 = wb['Sheet']
    col_b = []

    test_from_file_path = project_path + "\\优化热门中英文歌曲.txt"
    with open(test_from_file_path, "w+", encoding='utf-8') as fromfile:
        for col in sheet1["B"]:
            col_b.append(col.value)
            print(str(col.value))
            fromfile.write(str(col.value) + "。\n")
    # print(col_b)
