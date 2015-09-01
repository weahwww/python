#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'weahwww'

import base64

text = "*晓黎".encode(encoding="utf-8")
print(text)
en_text = base64.b64encode(text)
print(en_text)
en_text = b"KuadsA=="
de_text = base64.b64decode(en_text)
print(de_text.decode("utf-8"))
# class NameDecode:
#     def __init__(self):
#         self.keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
#
#     def decode(self, input):
#         self.input = input
#         Rz1 = ""
#         oszZez9 = 0
#
#
#     def utf8_decode(self, utftext):
#         self.utftext = utftext
