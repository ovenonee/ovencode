"""
将 VOC 格式的 XML 标注转换成 YOLO 所需的 txt 标注，并生成 train / val / test 列表。
目录结构（相对本项目根目录）：
    Annotations/    *.xml
    JPEGImages/     *.jpg
    ImageSets/      train.txt  val.txt  test.txt（仅存放文件名，无扩展名）
运行后：
    labels/         *.txt（YOLO 格式）
    train.txt       每行为对应图片绝对路径
    val.txt
    test.txt
"""

import os
import xml.etree.ElementTree as ET
from os import getcwd

# -------------------------------------------------
# 仅需修改这一处：项目根目录
ROOT_DIR = r'D:\oven\ovenrm\cat'
# -------------------------------------------------

ANNOT_DIR = os.path.join(ROOT_DIR, 'Annotations')
IMAGE_DIR = os.path.join(ROOT_DIR, 'JPEGImages')
LABEL_DIR = os.path.join(ROOT_DIR, 'labels')

SETS    = ['train', 'val', 'test']
CLASSES = ['white', 'black']   # 标签顺序即类别 id

# ---------- 工具函数 ----------
def detect_encoding(file_path):
    """简单检测文件编码：utf-8 / gbk / utf-8-sig"""
    for enc in ('utf-8', 'utf-8-sig', 'gbk'):
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read()
            return enc
        except UnicodeDecodeError:
            continue
    raise ValueError(f'无法识别编码: {file_path}')

def convert(size, box):
    """将边界框从像素坐标转为归一化中心点坐标"""
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return (x * dw, y * dh, w * dw, h * dh)

def convert_annotation(image_id):
    """单张图片：XML -> txt"""
    xml_path = os.path.join(ANNOT_DIR, f'{image_id}.xml')
    txt_path = os.path.join(LABEL_DIR, f'{image_id}.txt')

    if not os.path.exists(xml_path):
        print(f'⚠️  跳过缺失标注：{xml_path}')
        return

    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    with open(txt_path, 'w', encoding='utf-8') as f:
        for obj in root.iter('object'):
            cls_name = obj.find('name').text
            difficult = int(obj.find('difficult').text)

            if cls_name not in CLASSES or difficult == 1:
                continue

            cls_id = CLASSES.index(cls_name)
            bnd = obj.find('bndbox')
            box = (
                float(bnd.find('xmin').text),
                float(bnd.find('xmax').text),
                float(bnd.find('ymin').text),
                float(bnd.find('ymax').text),
            )
            yolo_box = convert((w, h), box)
            f.write(f'{cls_id} {" ".join(map(str, yolo_box))}\n')

# ---------- 主流程 ----------
if __name__ == '__main__':
    print('当前工作目录：', getcwd())

    os.makedirs(LABEL_DIR, exist_ok=True)

    for set_name in SETS:
        id_file = os.path.join(ROOT_DIR, 'ImageSets', f'{set_name}.txt')
        if not os.path.exists(id_file):
            print(f'⚠️  未找到 {id_file}，跳过该集合')
            continue

        enc = detect_encoding(id_file)
        with open(id_file, 'r', encoding=enc) as f:
            image_ids = [line.strip() for line in f if line.strip()]

        list_txt = os.path.join(ROOT_DIR, f'{set_name}.txt')
        with open(list_txt, 'w', encoding='utf-8') as list_file:
            for img_id in image_ids:
                img_path = os.path.join(IMAGE_DIR, f'{img_id}.jpg')
                list_file.write(f'{img_path}\n')
                convert_annotation(img_id)

    print('✅ 全部处理完成！')