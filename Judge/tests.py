from django.test import TestCase
import hashlib
def Md5Pwd(s):
    md = hashlib.md5()  # 创建md5对象
    md.update(s.encode(encoding='utf-8'))
    return md.hexdigest()


print(Md5Pwd("zxc123123"))