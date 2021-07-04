import re
import jieba
import os
from SpamSystem.settings import BASE_DIR

spam = BASE_DIR + "/dataSet/spam/"
normal = BASE_DIR + "/dataSet/normal/"
spam_list = os.listdir(spam)
normal_list = os.listdir(normal)

empty = []


def delete_empty_file(file_list, file_dir):
    for e in file_list:
        with open(file_dir + e) as f:
            c = f.read()
            match = re.compile(r"[^\u4e00-\u9fa5]")
            s = match.sub("", c)
            jie = list(set(jieba.cut(s)))
            if not jie:
                print(e)
                empty.append(file_dir+e)


delete_empty_file(spam_list,spam)
delete_empty_file(normal_list,normal)
for i in empty:
    os.remove(i)
