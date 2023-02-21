import xlwt
import os


project_path = os.path.dirname(os.path.abspath(__file__))

workbook = xlwt.Workbook()
sheet1=workbook.add_sheet('tmmr',cell_overwrite_ok=True)
#style = "font:colour_index blue;"
#blue_style = xlwt.easyxf(style)

row0=[u"TIME",u"MOS_CPU",u"MOS_MEM",u"TMMR_CPU",u"TIMMR_MEM",u"Load Average_1",u"Load Average_5",u"Load Average_15"]
for i in range(0,len(row0)):
    sheet1.write(0,i,row0[i])
    #sheet1.write(0,i,row0[i],blue_style)

f = open(project_path + r'\perf.txt') 
next(f) 
index = 1
for line in f: 
    data = line.strip('\n').split(' ')
    print(data)
    if data[7] =="tmmr":
        #print "********************************"
        #print data
        data[7],data[12] = data[12],data[7]
        data[8],data[13] = data[13],data[8]
        data[9],data[14] = data[14],data[9]
        data[10],data[15] = data[15],data[10]
        data[11],data[16] = data[16],data[11]
       # print data
        #print "********************************"
    sheet1.write(index,0,data[1])
    sheet1.write(index,1,float(data[9]))
    sheet1.write(index,2,float(data[11]))
    sheet1.write(index,3,float(data[14]))
    sheet1.write(index,4,float(data[16]))
    sheet1.write(index,5,float(data[4].strip(',')))
    sheet1.write(index,6,float(data[5].strip(',')))
    sheet1.write(index,7,float(data[6].strip(',')))
    index = index + 1
# 默认输出在pylearning文件夹根目录下
workbook.save('perf.xls')
