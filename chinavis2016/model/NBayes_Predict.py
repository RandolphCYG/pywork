# -*- coding: utf-8 -*-
# @Time    : 2019/4/9 21:18
# @Author  : Randolph
# @Email   : cyg0504@outlook.com
# @File    : NBayes_Predict.py
# @Software: PyCharm

# from sklearn.naive_bayes import MultinomialNB  # 导入多项式贝叶斯算法

from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from Tools import readbunchobj

# 导入训练集
trainpath = "../res/train_word_bag/tfdifspace.dat"
train_set = readbunchobj(trainpath)

# 导入测试集
testpath = "../res/test_word_bag/testspace.dat"
test_set = readbunchobj(testpath)

# 训练分类器：输入词袋向量和分类标签，alpha:0.001 alpha越小，迭代次数越多，精度越高
print(train_set.label)
# clf = MultinomialNB(alpha=0.001).fit(train_set.tdm, train_set.label)
# clf = MultinomialNB(alpha=0.001).fit(test_set.tdm, test_set.label)
# print(clf)

clf = LogisticRegression().fit(train_set.tdm, train_set.label)
# 预测分类结果
predicted = clf.predict(test_set.tdm)
print(predicted)

for flabel, file_name, expct_cate in zip(test_set.label, test_set.filenames, predicted):
    if flabel != expct_cate:
        print(file_name, ": 实际类别:", flabel, " -->预测类别:", expct_cate)
    else:
        print(file_name, ": 实际类别:", flabel, " -->预测类别:", expct_cate)


# 计算分类精度：

def metrics_result(actual, predict):
    print("预测结果：")
    print('精度:{0:.4f}'.format(metrics.precision_score(actual, predict, average='weighted')))
    print('召回:{0:0.4f}'.format(metrics.recall_score(actual, predict, average='weighted')))
    print('F1-score:{0:.4f}'.format(metrics.f1_score(actual, predict, average='weighted')))


if __name__ == "__main__":

    metrics_result(test_set.label, predicted)
