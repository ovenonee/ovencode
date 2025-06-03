import torch
import os
from ultralytics import YOLO

# 加载模型
model = YOLO('yolo11n.pt')

# 训练模型
model.train(
    data=r'.\RM-ARMOR-COCO\data.yaml',
    epochs=1,
    device='cuda',
    workers=0,
    imgsz=320,
    batch=128,
    name="rm_detect",
    save=True
)

# 验证模型
#model.val()
checkpoint_dir = os.path.join("runs", "detect", "rm_detect")
checkpoint_path = os.path.join(checkpoint_dir, "weights", "last.pt")
# 保存模型权重到指定路径
final_model_path = os.path.join(checkpoint_dir, "weights", "final_model.pt")
model.save(final_model_path)