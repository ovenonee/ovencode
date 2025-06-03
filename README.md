# oven
本项目是使用深度学习(yolo11)的办法检测机器人和装甲板
数据集来源于https://github.com/houhongyi/RM-DATASET

依赖安装：
os：pip install os  (以下同理）
yaml:
torch:
ultralytics:
argparse:
json:
cv2:

使用教程：
0.克隆仓库中的所有文件：
git clone https://github.com/ovenonee/oven.git
1.下载数据集，找到数据集中的RM-ARMOR-COCO文件夹并将其保存到rmjian目录下，运行dataconvert.py以将coco数据集中的json文件转化为txt文件,并生成data.yaml文件
2.安装依赖后，运行cudatest.py和camtest.py以测试是否成功安装
3.调整train_.py中的参数后运行进行训练
4.训练成功后的模型保存在目的文件夹中，可以用picturetest.py文件测试对单张图片的识别
5.调整camdetect.py中的摄像头参数后运行即可进行机器人和装甲板的实时识别
