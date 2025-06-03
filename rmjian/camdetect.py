import torch
import cv2
from ultralytics import YOLO

# 加载模型
model = YOLO(r'.\runs\detect\rm_detect\weights\final_model.pt')

# 打开摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    # 读取摄像头帧
    ret, frame = cap.read()
    if not ret:
        break

    # 进行目标检测
    results = model(frame)

    # 遍历每个检测结果并绘制
    for result in results:
        annotated_frame = result.plot()

    # 显示结果
    cv2.imshow('rm_detect', annotated_frame)


    # 按下空格键退出循环
    if cv2.waitKey(1) == ord(' '):
        break

# 释放摄像头资源
cap.release()

# 关闭所有 OpenCV 窗口
cv2.destroyAllWindows()