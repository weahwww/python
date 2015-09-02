import hashlib

password = input("输入密码: ")
sha1obj = hashlib.sha1()
sha1obj.update(password.encode())
hash = sha1obj.hexdigest()
print(hash)