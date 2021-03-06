# -*- coding: utf-8 -*-
# @Time    : 2019/4/7 21:12
# @Author  : Randolph
# @Email   : cyg0504@outlook.com
# @File    : display_per_subject_txt.py
# @Software: PyCharm


import pandas as pd
import numpy as np
import os.path
import re

source_path = '../res/results/display_list.txt'
path = '../res/chinavis2016_data'
save_path = '../res/corpus_file/'
top100 = '../res/results/raw_modify_top100.txt'
path2 = '../res/test_corpus_seg'


def is_number(s):
    """
    判断是否为数字
    :param s:字符串
    :return:T OR F
    """
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def manual_clear_subject(str):
    """
    传主题 反清洗过主题
    :param str:字符串
    :return:字符串
    """
    while 're: ' in str or 'r: ' in str or 'i:' in str:
        str = ' '.join(str.split(' ')[1:])
    if '[vtmis]' in str:
        str = ' '.join(str.split(' ')[1:])
    if '[!' in str:
        str = ' '.join(str.split(' ')[1:])
    # 忽略空回复、数字、空
    if str == 'r:' or is_number(str) or str.isspace():
        pass
    else:
        return str


def get_display_subject(find_name):
    name = '_'.join(find_name.replace('\n', '').split(' ')) + '_subject.txt'
    print(save_path + name)
    for i, f in enumerate(os.listdir(path)):
        file = os.path.join('../res/chinavis2016_data/', f)
        print('正在处理第', i + 1, '个文件', file, '：')
        data = pd.read_csv(file, encoding='utf-8', error_bad_lines=False)
        data.fillna(value='0', inplace=True)    # 缺失值处理
        # 筛选发出邮箱
        from_result = data.loc[data['from (display)'].str.contains(
            find_name, na=False)]

        # 将from_result数据转换为list，用索引把主题切出来
        train_data = np.array(from_result)  # np.ndarray()
        train_x_list = train_data.tolist()  # list
        for i, line in enumerate(train_x_list):
            print(i + 1, manual_clear_subject(line[0]))
            # 放入筛选函数

            # 写入函数
            f = open(save_path + name, 'a', encoding='utf_8')
            if manual_clear_subject(line[0]) is None:
                pass
            else:
                f.write(manual_clear_subject(line[0]) + ' ')
            f.close()


def display_occur_to_array():
    """这里我们打开分词后的内部员工名字对应的txt文档、top100关键词，
    尝试遍历第一个文件中，各top100关键词出现的次数
    :return:
    """
    for i, f in enumerate(os.listdir(path2)):
        file = os.path.join('../res/test_corpus_seg/', f)
        print('正在处理第', i + 1, '个文件', file, '：')
        with open(top100, encoding='utf8', errors='ignore') as fw:
            wordlist = fw.read().split('\n')  # top词汇表
            aim_array = []
            with open(file, encoding='utf8', errors='ignore') as fw2:
                for content in fw2:
                    for w in wordlist:
                        count = len(re.findall(w, content))
                        # print(w, '出现的次数是：', count)
                        aim_array.append(count)
            print(aim_array)


def display_occur_to_array_single(filename):
    """这里我们打开分词后的内部员工名字对应的txt文档、top100关键词，
    尝试遍历第一个文件中，各top100关键词出现的次数
    :return:
    """
    # for i, f in enumerate(os.listdir(path2)):
    file = os.path.join('../res/test_corpus_seg/', filename)
    print('正在处理文件', file, '：')
    with open(top100, encoding='utf8', errors='ignore') as fw:
        wordlist = fw.read().split('\n')  # top词汇表
        aim_array = []
        with open(file, encoding='utf8', errors='ignore') as fw2:
            for content in fw2:
                for w in wordlist:
                    count = len(re.findall(w, content))
                    # print(w, '出现的次数是：', count)
                    aim_array.append(count)
        print(aim_array)


if __name__ == "__main__":
    # get_display_subject()

    # find_name = 'simonetta gallucci'

    # find_name = 'serge woon'
    # get_display_subject(find_name)

    display_occur_to_array()

    # display_occur_to_array_single(filename='alberto_ornaghi_subject.txt')

    # with open(top100, encoding='utf8', errors='ignore') as fw:
    #     wordlist = fw.read().split('\n')    # top词汇表
    #
    #     with open(source_txt, encoding='utf8', errors='ignore') as fw2:
    #         for content in fw2:
    #             for w in wordlist:
    #                 count = len(re.findall(w, content))
    #                 print(w, '出现的次数是：', count)
