from ultralytics import YOLO

# 加载模型
model = YOLO(r'E:\machine\people\detect\cat_detect6\weights\last.pt')

# 运行
results = model(r'D:\oven\ovenrm\cat\images\test\4.jpg', conf=0.006405)  # 返回检测结果

# 结果
results[0].show()