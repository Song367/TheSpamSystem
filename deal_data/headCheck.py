import os
import re

spam = "F:/pycharm file/SpamSystem/dataSet/normal/"
file_list = os.listdir(spam)[:1]


def get_title_word_dict(files, file_table):
    words = []
    for file_dir in files:
        word = []
        for line in open(file_table + file_dir):
            match = re.compile("[\u4e00-\u9fa5]")
            s = match.sub("", line)
            match2 = re.compile("([a-z-A-Z]*):")
            x = match2.match(s)
            if not x or not x.group(1):
                continue
            table = []
            if x and x != "":
                for new_line in open("../deal_data/title_word_list"):
                    y = new_line.replace("\n", "")
                    table.append(y)
                if x.group(1) in table:
                    word.append(x.group(1))
        words.append(len(word))
    return words


res = get_title_word_dict(file_list, spam)
print(res)
