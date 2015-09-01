#!/usr/bin/python
# -*- coding: utf-8 -*-

def python3xStrToBytes():
    f = open("StrToBytes.txt", "w")
    zhcnUnicode = eval(input("请输入需要转换的字符: "))
    print("type(zhcnUnicode)=",type(zhcnUnicode))
    zhcnGbkBytes = zhcnUnicode.encode()
    print("Bytes : {0}".format(zhcnGbkBytes))
    f.write(zhcnGbkBytes.encode('utf-8'))
    f.close()

if __name__=="__main__":
    python3xStrToBytes()