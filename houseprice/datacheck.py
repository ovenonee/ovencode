import pandas as pd

# 加载数据
train_df = pd.read_csv('./train.csv')
test_df = pd.read_csv('./test.csv')

# 数据概览
print("数据前五行:")
print(train_df.head())

print("\n数据集基本信息:")
print(train_df.info())

print("\n数值型特征的描述性统计:")
print(train_df.describe())

# 缺失值检查:

# 检查训练集中的缺失值
print("\n各列缺失值计数:")
print(train_df.isnull().sum())

# 检查测试集中的缺失值
print("\n测试集中的缺失值")
print(test_df.isnull().sum())