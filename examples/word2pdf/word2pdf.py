from win32com.client import Dispatch  # pypiwin32
import os
import time
import sys


# project_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(os.path.realpath(sys.argv[0]))

pdfRoot = project_path + r"\pdf"  # 保存pdf结果的文件夹
wordRoot = project_path  # 读取word的文件夹,默认为工作目录
# print("pdfRoot = " + pdfRoot)
# print("wordRoot = " + wordRoot)
# print(os.path.dirname(os.path.realpath(sys.argv[0])))


def word2pdf(filelist):
    """使用windows COM组件完成word到pdf的批量转换

    Args:
        filelist ([列表]): [文件列表]
    """
    print("打开word...")
    word = Dispatch('Word.Application')
    counter = 0
    start_tran_time = time.time()
    for file in filelist:
        start_time = time.time()
        if (file.lower().endswith(".doc") or file.lower().endswith(".docx")) and ("~$" not in file):
            counter += 1
            print("正在转换:" + file)
            filePath = wordRoot+"\\"+file
            print("文件路径： " + filePath)
            doc = word.Documents.Open(filePath)
            outFile = pdfRoot +"\\"+ file.split('.')[0] + ".pdf" #生成pdf文件路径名称
            doc.SaveAs(outFile, FileFormat=17)
            doc.Close()
            cost_time = time.time() - start_time
            print("耗时：" + str(cost_time) + "秒")
    if counter==0:
        print("未找到word文件，请将文件放到与程序在同一个文件夹！")
    else:
        total_cost_time = time.time() - start_tran_time
        print("所有word文件转PDF文件已完成！总耗时：" + str(total_cost_time) + "秒")
    word.Quit()  # 退出时会花几秒
    print("按任意键退出程序......")

if __name__ == "__main__":
    print("--------------------------------------------------------------------")
    print("-------------------------word批量转pdf-------------------------------")
    print("------------------------- By Tonsen  -------------------------------")
    print("--------------- 关注公众号：DogKeDog获取工具和源码---------------------")
    print("-------------------- 可提供工具需求，定制开发-------------------------")
    print("--------------------------------------------------------------------")
    print("初始化程序...")
    filelist = os.listdir(wordRoot)
    if not os.path.exists(pdfRoot):
        os.makedirs(pdfRoot)
    word2pdf(filelist)
    os.system("pause")