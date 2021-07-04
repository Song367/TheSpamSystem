import re
import jieba
from sklearn import svm
from joblib import load
from SpamSystem.settings import BASE_DIR
from multiprocessing import Process, Queue


# 从测试集中测试模型
def content_filter(word_list, file_dir):
    word_rate = {}
    with open(file_dir) as f:
        text = f.read()
        match = re.compile(r"[^\u4e00-\u9fa5]")
        result = match.sub("", text)
        test_jie_list = list(set(jieba.cut(result)))
        for jie in test_jie_list:
            if jie in word_list:
                # print(word_list.index(jie))
                word_rate[jie] = 1
            else:
                word_rate[jie] = 0
    return sum(word_rate.values())


def read_spam_word_file(words_list):
    for line in open(BASE_DIR + "/deal_data/spam_words"):
        line = line.replace("\n", "")
        words_list.append(line)


def read_normal_word_file(words_list):
    for line in open(BASE_DIR + "/deal_data/normal_words"):
        line = line.replace("\n", "")
        words_list.append(line)


# 测试模型
# test = "E:/pywork/SpamSystem/dataSet/normal/"
# spam_word_list = []
# normal_word_list = []

# read_spam_word_file(spam_word_list)
# read_normal_word_file(normal_word_list)
# spam_rate = content_filter(spam_word_list, test + "300")
# normal_rate = content_filter(normal_word_list, test + "300")
# print(spam_rate, "\t", normal_rate)

# model = load("E:/pywork/SpamSystem/machine_learning/svm_model2")

# res = model.predict([[spam_rate, normal_rate]])
# print(res)


# 从内容框中预测是否为垃圾邮件系统


def web_content_filter(content, wordlist):
    word_rate = {}
    match = re.compile(r"[^\u4e00-\u9fa5]")
    result = match.sub("", content)
    test_jie_list = list(set(jieba.cut(result)))
    for jie in test_jie_list:
        if jie in wordlist:
            word_rate[jie] = 1
        else:
            word_rate[jie] = 0
    return sum(word_rate.values())


def predict_content(content):
    web_spam_word_list = []
    web_normal_word_list = []
    read_spam_word_file(web_spam_word_list)
    read_normal_word_file(web_normal_word_list)
    web_spam_rate = web_content_filter(content, web_spam_word_list)
    web_normal_rate = web_content_filter(content, web_normal_word_list)
    svm = load(BASE_DIR + "/machine_learning/svm_model2")
    result = svm.predict([[web_spam_rate, web_normal_rate]])
    return result
