# -*- coding: utf-8 -*-
# 将指定数据库的表结构信息导出到excel
# 适用于Mysql 5.6.x

import sys

import MySQLdb
import xlwt



# 默认参数,定义查询出来的表结构信息中各字段的索引
table_info_name_index = 0
table_info_comment_index = 17
# 默认参数,定义查询出来的表字段信息中各字段的索引
column_info_name_index = 0
column_info_type_index = 1
column_info_allow_null_index = 3
column_info_default_index = 5
column_info_comment_index = 8
#
excel_file_path = "./"
excel_file_name = "export_table_columns_info.xls"
excel_full_path = excel_file_path + excel_file_name

reload(sys)
sys.setdefaultencoding('utf-8')

conn = MySQLdb.connect(
        host='192.168.45.155',
        port=3306,
        user='welicai',
        passwd='welicai',
        db='db-house-td',
        charset='utf8'
        )

cur = conn.cursor()

cur.execute("SHOW TABLE STATUS")
tables_list = ((x[table_info_name_index], x[table_info_comment_index]) for x in cur.fetchall())

wbk = xlwt.Workbook()
global_tables_sheet = wbk.add_sheet(u"数据表概览", cell_overwrite_ok=True)
global_tables_sheet.write(0, 0, u"表名")
global_tables_sheet.write(0, 1, u"说明")

for table_index, table_info in enumerate(tables_list):
    global_tables_sheet.write(table_index + 1, 0, table_info[0])
    global_tables_sheet.write(table_index + 1, 1, table_info[1])

    cur.execute("SHOW FULL FIELDS FROM " + table_info[0])
    columns_list = cur.fetchall()
    print "=" * 50, table_info[0], "(", table_info[1], ")", "=" * 50
    table_info_sheet = wbk.add_sheet(table_info[1], cell_overwrite_ok=True)
    table_info_sheet.write(0, 0, u"字段名称")
    table_info_sheet.write(0, 1, u"字段类型")
    table_info_sheet.write(0, 2, u"是否允许为空")
    table_info_sheet.write(0, 3, u"默认值")
    table_info_sheet.write(0, 4, u"说明")
    for column_index, column_info in enumerate(columns_list):
        column_name = column_info[column_info_name_index]
        column_type = column_info[column_info_type_index]
        column_allow_null = column_info[column_info_allow_null_index]
        column_default = column_info[column_info_default_index]
        column_comment = column_info[column_info_comment_index]

        table_info_sheet.write(column_index + 1, 0, column_name)
        table_info_sheet.write(column_index + 1, 1, column_type)
        table_info_sheet.write(column_index + 1, 2, column_allow_null)
        table_info_sheet.write(column_index + 1, 3, column_default)
        table_info_sheet.write(column_index + 1, 4, column_comment)

        print column_index, column_name, column_type, column_allow_null, column_default, column_comment

wbk.save(excel_full_path)
print "导出表结构到Excel文件成功,文件路径:", excel_full_path

cur.close()
conn.commit()
conn.close()
print "Finish!"
