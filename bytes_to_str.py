#!/usr/bin/python
# -*- coding: utf-8 -*-

def python3xBytesToStr():
    f = open("BytesToStr.txt", "wb")
    zhcnBytes = b'\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74'
    zhcnUnicodeStr = zhcnBytes.decode('gbk')
    print(zhcnUnicodeStr)
    f.write(zhcnUnicodeStr.encode('utf-8'))
    f.close()
    
if __name__ == "__main__":
    python3xBytesToStr()