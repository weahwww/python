text = input("请输入需要计算的字符串: ")
length = len(text)
utf8_length = len(text.encode('utf-8'))
length = (utf8_length - length)/2 + length
print(length)