# import pandas as pd
# from matplotlib import pyplot as plt
#
# # 加载数据
# train_df = pd.read_csv('./train.csv')
# test_df = pd.read_csv('./test.csv')
#
#
# # 填充思路；
# # 可以看到train年龄（Age）有177个缺失值，客舱号码（Cabin）有687个缺失值，还有登船港口（Embarked）有2个缺失值
# # 对于Age，可以使用中位数或平均值来填充。
# # 对于Embarked（仅在训练集中有少量缺失），可以使用众数（最常见的值）来填充。
# # 对于Cabin，考虑到缺失较多，可以填充为一个常数，如'Unknown'，或者从中提取有用信息，如甲板号。
# # Fare缺失值（在测试集中仅有1个）可以用中位数或平均值填充。
#
# # 填充年龄  平均值填充
# train_df['Age']= train_df['Age'].fillna(train_df['Age'].median())
#
#
# # 填充登船港口  众数填充
# most_common_embarked = train_df['Embarked'].mode()[0]
# train_df['Embarked'].fillna(most_common_embarked, inplace=True)
#
# # 填充Cabin的缺失值为 'Unknown'
# train_df['Cabin'].fillna('Unknown', inplace=True)
# # 提取Cabin的甲板号，将NaN视为 'U'（代表Unknown）
# train_df['Deck'] = train_df['Cabin'].apply(lambda x: x[0] if pd.notna(x) else 'U')
# # 检查提取后的甲板号
# print(train_df['Deck'].value_counts())
#
# # 填充票价  平均值填充
# train_df['Fare'] = train_df['Fare'].fillna(train_df['Fare'].median())
#
# # 缺失值检查:
#
# # 检查训练集中的缺失值
# print("\n各列缺失值计数:")
# print(train_df.isnull().sum())
#
# # 检查测试集中的缺失值
# print("\n测试集中的缺失值")
# print(test_df.isnull().sum())

import pandas as pd

# 1. 读数据
train_df = pd.read_csv('./train.csv')
test_df  = pd.read_csv('./test.csv')

# # 2. 定义统一的缺失值填充函数
# def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
#     """对 Age, Embarked, Cabin, Fare 做缺失值填充"""
#     df = df.copy()          # 避免修改原 DataFrame
#
#     # Age：用中位数填充
#     df['Age'] = df['Age'].fillna(df['Age'].median())
#
#     # Embarked：用众数填充（训练集 2 个缺失，测试集无此列）
#     if 'Embarked' in df.columns:
#         most_common_embarked = df['Embarked'].mode()[0]
#         df['Embarked'] = df['Embarked'].fillna(most_common_embarked)
#
#     # Cabin：缺失值 -> 'Unknown'，并提取甲板号
#     df['Cabin'] = df['Cabin'].fillna('Unknown')
#     df['Deck']  = df['Cabin'].str[0].fillna('U')   # 更简洁的写法
#
#     # Fare：用中位数填充（测试集 1 个缺失）
#     df['Fare']  = df['Fare'].fillna(df['Fare'].median())
#
#     return df
#
# # 3. 应用
# train_df = fill_missing(train_df)
# test_df  = fill_missing(test_df)
#
# # 4. 检查缺失值
# print('训练集缺失值：\n', train_df.isnull().sum())
# print('\n测试集缺失值：\n', test_df.isnull().sum())
#
# # 5. 甲板号分布
# print('\n训练集甲板号分布：\n', train_df['Deck'].value_counts())


train = train_df.copy()
train['Embarked'] = train['Embarked'].fillna(train['Embarked'].mode()[0])
train['Cabin'] = train['Cabin'].fillna('NO')
#求出每个头衔对应的年龄中位数
Age_Appellation_median = train.groupby('Appellation')['Age'].median()
#在当前表设置Appellation为索引
train.set_index('Appellation', inplace = True)
#在当前表填充缺失值
train.Age.fillna(Age_Appellation_median, inplace = True)
#重置索引
train.reset_index(inplace = True)
#第一种: 返回0即表示没有缺失值
train.Age.isnull().sum()
#第二种: 返回False即表示没有缺失值
train.Age.isnull().any()
#第三种: 描述性统计
train.Age.describe()