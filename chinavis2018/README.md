## 0.参考资料
* [Python + wordcloud + jieba 十分钟学会用任意中文文本生成词云](https://blog.csdn.net/fontthrone/article/details/72782971)
* [Python词云 wordcloud 十五分钟入门与进阶](https://blog.csdn.net/fontthrone/article/details/72775865)
* [Python中文分词 jieba 十五分钟入门与进阶](https://blog.csdn.net/fontthrone/article/details/72782499)
* [jieba·PyPI](https://pypi.org/project/jieba/)
# 1.数据预筛选和处理
## 1.将email.csv的subject绘制词云，观察文本分布情况，可以首先筛除垃圾邮件;
看到包含“ALARM”，“RECOVER”，“互联网资产监控报警”，“安全邮件崩溃”字样的邮件主题，这些我们明显不需要：

![](/chinavis2018/res/wrong_result.png)

## 2.再者根据前二十高频词汇，也能尽量找到无用记录：
```
HOST 0.7083569789095852
邮件 0.5233368348207466
崩溃 0.4402549631286797
ALARM 0.3615879377571882
RECOVER 0.34676904115239693
安全 0.32229094578948253
文档 0.24175923428257629
报警 0.13963687165883418
葡京 0.13448404268243297
监控 0.12412264358465147
互联网 0.11885318218949696
澳門 0.11210220857513435
38 0.10455554826713877
com 0.09368149682334513
116498 0.09124598372394656
群號 0.08414526243415073
资产 0.0841363421215404
会计核算 0.08324108391702387
需求 0.07141084949166569
项目 0.06777019155158302
```
## 3.清理代码
```
def clean(target_csv, clean_csv):
    read_data = pd.read_csv(target_csv)  # 读取原始Email.csv
    # print(read_data)
    read_data = read_data[~ read_data['subject'].str.contains('邮件')]  # 删除某列包含特殊字符的行
    read_data = read_data[~ read_data['subject'].str.contains('崩溃')]  
    read_data = read_data[~ read_data['subject'].str.contains('HOST')]
    read_data = read_data[~ read_data['subject'].str.contains('ALARM')]
    read_data = read_data[~ read_data['subject'].str.contains('RECOVER')]
    read_data = read_data[~ read_data['subject'].str.contains('报警')]
    read_data = read_data[~ read_data['subject'].str.contains('葡京')]
    read_data = read_data[~ read_data['subject'].str.contains('澳門')]
    read_data = read_data[~ read_data['subject'].str.contains('38')]
    read_data = read_data[~ read_data['subject'].str.contains('群號')]
    # print(read_data)
    read_data.to_csv(clean_csv, index=False)  # 将数据重新写入Email.csv
```
## 4.剔除后前二十高频词和词云，达到了要求：
清理数据后的高频词汇
```
文档 0.6547430658567895
会计核算 0.22543719023105152
需求 0.19339802539646225
项目 0.18353823431754343
财务 0.17090855224163862
税务 0.1634438203477047
用户手册 0.160830880914214
api 0.15635222762432255
配置 0.15598272665734156
分析 0.15424798424972375
系统配置 0.15022076771748638
初验 0.1482698486562203
终验 0.14520411870280223
软件开发 0.13839853942736494
设计 0.13572664266454468
概要 0.12885281438319748
测试数据 0.12789329858039522
传输 0.12710249619060948
子系统 0.1265628142423125
```
可以看到，借助词云和高频词我们已经基本剔除了无用数据，至此简单清洗数据工作完成

![](/chinavis2018/res/result.png)

## 5.补充说明 jiaba分词
两点：使用邮件主题词txt（utf_8）、自定义词典subject_dict.txt（utf_8）
这样做的原因是想以后完善数据准备环节，文档在res目录下

# 2.邮件主题分类
1.题目意思有三大部门：预定义了人力、财务、技术三个部门对主题初步分类；

>[LDA参考](https://github.com/ljpzzz/machinelearning/blob/master/natural-language-processing/lda.ipynb)



2.从收件人的角度建立分类的*对应关键词表*。我们采用 jieba 分词切分 subject 并与关键词表相匹配，得到每条 email 日志所对应的部门分类，为内部邮箱的收件地址打上部门大类的标签。

# 3. 随机森林——东北师范大学
前面第二大点的方法较为古老，并且是我理解错了迪哥的意思：
应当参考东北师范大学在2018年可视化大会的方法去做2016年的分析，这样才能彻底清晰学会方法，之后自己去分析新的内容
18年的先停一停，20190317（词云主题绘制两遍bug）

## 挑战 1.1：分析公司内部员工所属部门及各部门的人员组织结构，给出公司员工的组织结构图。

邮件作为公司人员交流的主要方式之一，存储着员工之间的工作关系、沟通主题等有价值的信息。
针对该题，我们基于邮件数据，使用随机森林算法将员工进行部门划分，构建员工间的关系网络，结
合信息熵探索部门内部的组织结构。

（1） 部门划分 
邮件主题反映了各员工的工作范围，因此它成为判别员工所属部门的重要特征。基于随机森林算
法，我们将员工分为财务、人力、研发三个部门，步骤如下：

a. 提取所有数据中频数最大的 90 个主题，为每个员工构建一个 90 维的向量，分别存储该员工
收发该主题邮件的频数。

b. 随机选取 40 名员工，基于邮件主题人工赋予其所属部门的标签，构建为训练集，并进行随机
森林训练。

c. 利用训练好的随机森林将剩余的 259 名员工分类。
我们发现财务部门有 24 名员工，人力资源部门有 18 员工，研发部门有 257 名员工

