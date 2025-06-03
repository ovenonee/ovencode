from ultralytics import YOLO

# 加载模型
model = YOLO(r'.\runs\detect\rm_detect\weights\final_model.pt')

# 运行
results = model(r'.\testpicture.jpg')  # 返回检测结果

# 结果
results[0].show()