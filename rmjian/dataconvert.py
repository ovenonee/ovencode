import json
import os
import os
import yaml
import argparse


def convert_coco_to_yolo(json_path, output_path):
    with open(json_path) as f:
        data = json.load(f)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for image in data['images']:
        image_id = image['id']
        file_name = image['file_name']
        width = image['width']
        height = image['height']

        annotations = [ann for ann in data['annotations'] if ann['image_id'] == image_id]

        with open(os.path.join(output_path, f"{os.path.splitext(file_name)[0]}.txt"), 'w') as f:
            for ann in annotations:
                category_id = ann['category_id']
                bbox = ann['bbox']
                x_center = (bbox[0] + bbox[2] / 2) / width
                y_center = (bbox[1] + bbox[3] / 2) / height
                w = bbox[2] / width
                h = bbox[3] / height
                f.write(f"{category_id} {x_center} {y_center} {w} {h}\n")

json_path0 = r'.\RM-DATASET\RM-DATASET\RM-ARMOR-COCO\annotations\voc_2007_val.json'
output_path0 = r'.\RM-DATASET\RM-DATASET\RM-ARMOR-COCO\annotations\val'
convert_coco_to_yolo(json_path0, output_path0)

json_path1 = r'.\RM-ARMOR-COCO\annotations\train_2007_val.json'
output_path1 = r'.\RM-ARMOR-COCO\annotations\train'
convert_coco_to_yolo(json_path1, output_path1)

json_path2 = r'./RM-ARMOR-COCO/annotations/voc_2007_test.json'
output_path2 = r'.\RM-ARMOR-COCO\annotations\test'
convert_coco_to_yolo(json_path2, output_path2)

# 文件路径配置
dataset_path = r".\RM-ARMOR-COCO"
data_yaml_path = os.path.join(dataset_path, "data.yaml")
checkpoint_dir = os.path.join("runs", "detect", "rm_detect")
checkpoint_path = os.path.join(checkpoint_dir, "weights", "last.pt")

# 定义类别信息
class_names = [
    "car_red", "car_blue", "car_unknow",
    "watcher_red", "watcher_blue", "watcher_unknow",
    "armor_red", "armor_blue", "armor_grey"
]

# 创建YAML配置文件（检测任务）
data_dict = {
    'train': os.path.join(dataset_path, r'.\RM-ARMOR-COCO\images\train').replace('\\', '/'),
    'val': os.path.join(dataset_path, r'.\RM-ARMOR-COCO\images\val').replace('\\', '/'),
    'test': os.path.join(dataset_path, r'.\RM-ARMOR-COCO\images\test').replace('\\', '/'),
    'nc': len(class_names),
    'names': class_names
}

with open(data_yaml_path, 'w') as f:
    yaml.dump(data_dict, f, sort_keys=False)

# 检查路径是否存在
required_paths = [
    os.path.join(dataset_path, 'images/train'),
    os.path.join(dataset_path, 'images/val'),
    os.path.join(dataset_path, 'labels/train'),
    os.path.join(dataset_path, 'labels/val')
]