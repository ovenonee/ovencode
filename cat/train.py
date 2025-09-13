import torch
import os
import shutil
from ultralytics import YOLO



# 训练模型

if __name__ == '__main__':
    model = YOLO("yolo11n.pt")
    model.train(
        data="D:/oven/ovenrm/cat/data.yaml",
        epochs=10,
        imgsz=640,
        project="D:/oven/ovenrm/cat",
        name="model"
    )




