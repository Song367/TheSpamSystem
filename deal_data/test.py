import os
import re
import jieba
import xlsxwriter
from SpamSystem.settings import BASE_DIR


def email_word_times(os_file_list, emails, file_dir, spam_or_normal_word_list):
    for lu in os_file_list:
        email = {}
        with open(file_dir + lu) as f:
            text = f.read()
            pub = re.compile(r"[^\u4e00-\u9fa5]")
            result = pub.sub("", text)
            jie_list = list(jieba.cut(result))
            for jie in jie_list:
                if jie in spam_or_normal_word_list:
                    email[jie] = 1
                else:
                    email[jie] = 0
        emails.append(email)


def spam_or_normal_word(os_file_list, file_dir, word_dict):
    for dir in os_file_list:
        with open(file_dir + dir) as f:
            x = f.read()
            match = re.compile(r"[^\u4e00-\u9fa5]")
            y = match.sub("", x)
            jie = list(jieba.cut(y))
            for j in jie:
                if j in word_dict:
                    word_dict[j] += 1
                else:
                    word_dict[j] = 0


spam = BASE_DIR + "/dataSet/spam/"
normal = BASE_DIR + "/dataSet/normal/"
os_spam_list = os.listdir(spam)
os_normal_list = os.listdir(normal)
spam_word_dict = {}
normal_word_dict = {}

spam_or_normal_word(os_spam_list, spam, spam_word_dict)
spam_or_normal_word(os_normal_list, normal, normal_word_dict)

spam_tuple = sorted(spam_word_dict.items(), key=lambda x: x[1], reverse=True)[:1000]
normal_tuple = sorted(normal_word_dict.items(), key=lambda x: x[1], reverse=True)[:800]

spam_word_list = []
normal_word_list = []
for r in spam_tuple:
    spam_word_list.append(r[0])

for n in normal_tuple:
    normal_word_list.append(n[0])

# with open("spam_words", 'w+') as word:
#     for s in spam_word_list:
#         word.write(s + '\n')
#     word.close()
# with open("normal_words",mode='w') as word:
#     for n in normal_word_list:
#         word.write(n + '\n')
#     word.close()
workBook = xlsxwriter.Workbook("dataSet.xlsx")
sheet = workBook.add_worksheet()
for i in range(3):
    if i == 0:
        sheet.write(0, i, "spam_rate")
    elif i == 1:
        sheet.write(0, 1, "normal_rate")
    else:
        sheet.write(0, 2, "target")
# 判断邮件字数是否存在

spam_emails = []  # 垃圾邮件中垃圾词汇
normal_emails = []  # 正常邮件中正常词汇

spam_normal_emails = []  # 垃圾邮件中正常词汇
normal_spam_emails = []  # 正常邮件中垃圾词汇

email_word_times(os_spam_list, spam_emails, spam, spam_word_list)
email_word_times(os_normal_list, normal_emails, normal, normal_word_list)
email_word_times(os_spam_list, spam_normal_emails, spam, normal_word_list)
email_word_times(os_normal_list, normal_spam_emails, normal, spam_word_list)
# print(sum(spam_emails[0].values()), sum(spam_emails[1].values()), sum(spam_emails[100].values()))
# print(sum(normal_emails[0].values()), sum(normal_emails[1].values()), sum(normal_emails[100].values()))
#
# print(sum(spam_normal_emails[0].values()), sum(spam_normal_emails[1].values()))
# print(sum(normal_spam_emails[0].values()), sum(normal_spam_emails[1].values()))

j = 1
for e in range(len(spam_emails)):
    sheet.write(j, 0, sum(spam_emails[e].values()))
    sheet.write(j, 1, sum(spam_normal_emails[e].values()))
    sheet.write(j,2,"spam")
    j += 1

for e in range(len(normal_emails)):
    sheet.write(j, 0, sum(normal_spam_emails[e].values()))
    sheet.write(j, 1, sum(normal_emails[e].values()))
    sheet.write(j, 2, "normal")
    j += 1

workBook.close()
