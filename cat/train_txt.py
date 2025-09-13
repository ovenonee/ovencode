import os
import random

# 设置数据集划分比例
train_percent = 0.7  # 训练集占比
val_percent = 0.2  # 验证集占比
test_percent = 0.1  # 测试集占比（自动计算）

# 设置路径
xmlfilepath = r'D:\oven\ovenrm\cat\Annotations'  # XML标注文件路径
txtsavepath = r'D:\oven\ovenrm\cat\ImageSets'  # 输出txt文件保存路径

# 获取所有XML文件名并打乱顺序
total_xml = os.listdir(xmlfilepath)
num = len(total_xml)
list_indices = list(range(num))
random.shuffle(list_indices)  # 建议显式打乱顺序

# 计算各数据集样本数量
num_train = int(num * train_percent)
num_val = int(num * val_percent)
num_test = num - num_train - num_val  # 剩余作为测试集

# 随机划分数据集
train_set = set(list_indices[:num_train])  # 前70%作为训练集
val_set = set(list_indices[num_train:num_train + num_val])  # 接着20%作为验证集
test_set = set(list_indices[num_train + num_val:])  # 最后10%作为测试集

# 写入文件（使用with语句更安全）
with open(os.path.join(txtsavepath, 'train.txt'), 'w') as ftrain, \
        open(os.path.join(txtsavepath, 'val.txt'), 'w') as fval, \
        open(os.path.join(txtsavepath, 'test.txt'), 'w') as ftest:
    for i in list_indices:
        name = total_xml[i][:-4] + '\n'  # 去掉.xml后缀并添加换行
        if i in train_set:
            ftrain.write(name)
        elif i in val_set:
            fval.write(name)
        else:
            ftest.write(name)