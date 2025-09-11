import os
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import random

# 設定資料夾路徑
xml_folder = './../SIXray/positive-Annotation'

category_counter = Counter()
objects_per_image_counter = Counter()
xml_files = [f for f in os.listdir(xml_folder) if f.endswith('.xml')]
image_objects = {}

for xml_file in xml_files:
    tree = ET.parse(os.path.join(xml_folder, xml_file))
    root = tree.getroot()
    objects = root.findall('object')
    names = []
    for obj in objects:
        name_tag = obj.find('name')
        if name_tag is not None and name_tag.text is not None:
            names.append(name_tag.text)
    for name in names:
        category_counter[name] += 1
    obj_count = len(names)
    objects_per_image_counter[obj_count] += 1
    image_objects[xml_file] = names

print("各種類數量:")
for k, v in category_counter.items():
    print(f'{k}: {v}')

print("\n單張圖違禁品數量分類:")
for k, v in objects_per_image_counter.items():
    print(f'{k}個物品: {v}張圖')

# 分割資料集
train_ratio = 0.8
val_ratio = 0.1  # train 裡面再分

data_by_count = defaultdict(list)
for xml_file, names in image_objects.items():
    forbidden_count = sum([1 for name in names if name in ['Knife', 'Gun', 'Explosive']])
    data_by_count[forbidden_count].append(xml_file)

train_files, val_files, test_files = [], [], []
for count, files in data_by_count.items():
    random.shuffle(files)
    n_total = len(files)
    n_train = int(n_total * train_ratio)
    n_test = n_total - n_train
    train_split = files[:n_train]
    test_split = files[n_train:]
    n_val = int(len(train_split) * val_ratio)
    val_split = train_split[:n_val]
    train_split_final = train_split[n_val:]

    train_files.extend(train_split_final)
    val_files.extend(val_split)
    test_files.extend(test_split)

print(f"訓練集: {len(train_files)} 張")
print(f"驗證集: {len(val_files)} 張")
print(f"測試集: {len(test_files)} 張")
