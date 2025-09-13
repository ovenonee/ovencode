import re

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

# 加载数据
train_df = pd.read_csv('./train.csv')
test_df = pd.read_csv('./test.csv')

# # 绘制年龄的直方图
# train_df['Age'].hist(bins=50)
# plt.title('Histogram of Age')
# plt.xlabel('Age')
# plt.ylabel('Frequency')
# plt.show()

# #生成Pclass_Survived的列联表
# Pclass_Survived = pd.crosstab(train_df['Pclass'], train_df['Survived'])
# #绘制堆积柱形图
# Pclass_Survived.plot(kind = 'bar', stacked = True)
# Survived_len = len(Pclass_Survived.count())
# Pclass_index = np.arange(len(Pclass_Survived.index))
# Sum1 = 0
# for i in range(Survived_len):
#     SurvivedName = Pclass_Survived.columns[i]
#     PclassCount = Pclass_Survived[SurvivedName]
#     Sum1, Sum2= Sum1 + PclassCount, Sum1
#     Zsum = Sum2 + (Sum1 - Sum2)/2
#     for x, y, z in zip(Pclass_index, PclassCount, Zsum):
#         #添加数据标签
#         plt.text(x,z, '%.0f'%y, ha = 'center',va='center' )
# #修改x轴标签
# plt.xticks(Pclass_Survived.index-1, Pclass_Survived.index, rotation=360)
# plt.title('Survived status by pclass')
# plt.show()

# 绘制年龄的箱线图
# plt.boxplot(train_df['Age'].dropna())
# plt.title('Box Plot of Age')
# plt.xlabel('Age')
# plt.ylabel('Value')
# plt.show()

# 1.1.2 箱线图分析
# 箱线图显示出多个离群点，这些点主要集中在高年龄区域。
# 中位数（箱体中的橙线）低于平均年龄（如果用箱体大小表示的话），这支持我们之前的观察结果，即数据向高年龄方向偏斜。
# 由于这些离群点，平均值会受到较高年龄值的影响，从而偏离大多数乘客的实际年龄。

# #生成列联表
# Sex_Survived = pd.crosstab(train_df['Sex'], train_df['Survived'])
# Survived_len = len(Sex_Survived.count())
# Sex_index = np.arange(len(Sex_Survived.index))
# single_width = 0.35
# for i in range(Survived_len):
#     SurvivedName = Sex_Survived.columns[i]
#     SexCount = Sex_Survived[SurvivedName]
#     SexLocation = Sex_index * 1.05 + (i - 1/2)*single_width
#    #绘制柱形图
#     plt.bar(SexLocation, SexCount, width = single_width)
#     for x, y in zip(SexLocation, SexCount):
#         #添加数据标签
#         plt.text(x, y, '%.0f'%y, ha='center', va='bottom')
# index = Sex_index * 1.05
# plt.xticks(index, Sex_Survived.index, rotation=360)
# plt.title('Survived status by sex')
# plt.show()

# #生成列联表
# SibSp_Survived = pd.crosstab(train_df['Embarked'], train_df['Survived'])
# SibSp_Survived.plot(kind = 'bar')
# plt.title('Survived status by SibSp')
# plt.show()

# #对Fare进行分组: 2**10>891分成10组, 组距为(最大值512.3292-最小值0)/10取值60
# bins = [0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600]
# train_df['GroupFare'] = pd.cut(train_df.Fare, bins, right = False)
# GroupFare_Survived = pd.crosstab(train_df['GroupFare'], train_df['Survived'])
# #GroupFare_Survived.plot(kind = 'bar')
# #plt.title('Survived status by GroupFare')
# GroupFare_Survived.iloc[2:].plot(kind = 'bar')
# plt.title('Survived status by GroupFare(Fare>=120)')
# plt.show()

#提取出头衔
train_df['Appellation'] = train_df.Name.apply(lambda x: re.search(r'\w+\.', x).group()).str.replace('.', '')
#查看有多种不同的结果
train_df.Appellation.unique()

Appellation_Sex = pd.crosstab(train_df.Appellation, train_df.Sex)
Appellation_Sex.T

train_df['Appellation'] = train_df['Appellation'].replace(['Capt','Col','Countess','Don','Dr','Jonkheer','Lady','Major','Rev','Sir'], 'Rare')
train_df['Appellation'] = train_df['Appellation'].replace(['Mlle','Ms'], 'Miss')
train_df['Appellation'] = train_df['Appellation'].replace('Mme', 'Mrs')
train_df.Appellation.unique()
#绘制柱形图
Appellation_Survived = pd.crosstab(train_df['Appellation'], train_df['Survived'])
Appellation_Survived.plot(kind = 'bar')
plt.xticks(np.arange(len(Appellation_Survived.index)), Appellation_Survived.index, rotation = 360)
plt.title('Survived status by Appellation')
plt.show()