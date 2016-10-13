# -*- coding: utf-8 -*-
# 将指定数据库的表结构信息导出到excel
# 适用于Mysql 5.6.x

import sys
from optparse import OptionParser

import MySQLdb
import xlwt

# opts, args = getopt.getopt(sys.argv[1:], "hi:o:",
#                            ("help", "host=", "port=", "user=", "passwd=", "database=", "charset=", "output="))

# 默认参数,数据库配置
# 如果不在启动的时候传入参数,则需要在此处进行数据库配置
host = "192.168.45.155"
port = 3306
user = "welicai"
passwd = "welicai"
db = "db-house-td"
charset = "utf8"

# 默认参数,导出的文件路径配置
# 如果不在启动的时候传入参数,则默认在当前目录生成导出的excel文件
excel_full_path = "./export_table_columns_info.xls"

reload(sys)
sys.setdefaultencoding('utf-8')

parser = OptionParser(usage="%prog [-f] [-q]", version="%prog 1.0")
parser.add_option("", "--host", dest="host", default=host, help="config mysql host")
parser.add_option("", "--port", type="int", dest="port", default=port, help="config mysql port")
parser.add_option("-u", "--user", dest="user", default=user, help="config mysql login user")
parser.add_option("-p", "--passwd", dest="passwd", default=passwd, help="config mysql login password")
parser.add_option("-d", "--database", dest="db", default=db, help="select a mysql database")
parser.add_option("-c", "--charset", dest="charset", default=charset, help="select a mysql encode")
parser.add_option("-o", "--output", dest="excel_full_path", default=excel_full_path,
                  help="config export excel abstract path")

options, args = parser.parse_args(sys.argv)

# 默认参数,定义查询出来的表结构信息中各字段的索引
table_info_name_index = 0
table_info_comment_index = 17
# 默认参数,定义查询出来的表字段信息中各字段的索引
column_info_name_index = 0
column_info_type_index = 1
column_info_allow_null_index = 3
column_info_default_index = 5
column_info_comment_index = 8

conn = MySQLdb.connect(
        host=options.host,
        port=options.port,
        user=options.user,
        passwd=options.passwd,
        db=options.db,
        charset=options.charset
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

wbk.save(options.excel_full_path)
print "导出表结构到Excel文件成功,文件路径:", options.excel_full_path

cur.close()
conn.commit()
conn.close()
print "Finish!"
