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

# wbk = xlwt.Workbook()
# tables_sheet = wbk.add_sheet('数据表概览', cell_overwrite_ok=True)

for table_info in tables_list:
    cur.execute("SHOW FULL FIELDS FROM " + table_info[0])
    columns_list = cur.fetchall()
    print "=" * 50, table_info[0], "(", table_info[1], ")", "=" * 50
    for column_info in columns_list:
        column_name = column_info[column_info_name_index]
        column_type = column_info[column_info_type_index]
        column_allow_null = column_info[column_info_allow_null_index]
        column_default = column_info[column_info_default_index]
        column_comment = column_info[column_info_comment_index]



        print column_name, column_type, column_allow_null, column_default, column_comment


cur.close()
conn.commit()
conn.close()
