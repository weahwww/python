#!/usr/bin/env python
# -*- coding: utf-8 -*-

' a log to excel module '

__author__ = 'weahwww'

import os.path
import xlwt,xlrd

# log_filename = input("Please input the log name: ").strip()
# excel_filename = input("Please input the excel name: ").strip()

def run(coding,log_filename,excel_filename):
    input_file = open(log_filename, "r")

    # 获取实际log文件名
    log_file = os.path.basename(log_filename)

    # 创建xls表格
    wb = xlwt.Workbook()
    ws = wb.add_sheet(log_file)

    # 判断之前是否输入excel文件名
    if excel_filename == "":
        excel_filename = log_filename + ".xls"
    else:
        excel_filename = excel_filename

    # 迭代分割每一行并写入xls文件中
    x = input_file.readline()           # 逐行读取
    y = x.split(coding)                 # 分割每行
    for j in range(0, len(x)):          # 行迭代
        for i in range(0, len(y)):      # 列迭代
            ws.write(j, i, y[i])        # 写入xls
        x = input_file.readline()       # 重复
        y = x.split(coding)

    # 保存xls文件
    wb.save(excel_filename)
    input_file.close()

coding = " "
log_filename = input("Please input the log name(ex. C:/log.log): ").strip()
excel_filename = input("Please input the excel name(ex. C:/excel.xls): ").strip()
run(coding, log_filename, excel_filename)