#!/usr/bin/env python3
"""
split_categories_to_yolo.py

- SOURCE_CATEGORIES_DIR: 下層為各類別資料夾，每個類別資料夾內含 images/ 與 xmls/
  範例:
    categories/
      Gun/
        images/
        xmls/
      Knife/
        images/
        xmls/

- TARGET_DIR: 會建立 images/{train,val,test} 與 xmls/{train,val,test}

行為:
- 以圖片 basename (no ext) 當 key 做去重
- 隨機 shuffle，依 72% / 8% / 20% 分配
- 複製檔案並印出統計資訊
"""

import os
import shutil
import random
from collections import defaultdict, Counter

# ===== 設定 =====
SOURCE_CATEGORIES_DIR = "./../SIXray_Categories"   # <-- 改成你 categories 根目錄
TARGET_DIR = "./../SIXray_YOLO"          # <-- 改成你想輸出的資料夾
IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".bmp"]
SEED = 42

# 切分比例 (train, val, test) = 0.72, 0.08, 0.20
TRAIN_RATIO = 0.72
VAL_RATIO = 0.08
TEST_RATIO = 0.20

# ===== 準備目標資料夾 =====
for sub in ["images/train", "images/val", "images/test", "xmls/train", "xmls/val", "xmls/test"]:
    os.makedirs(os.path.join(TARGET_DIR, sub), exist_ok=True)

# ===== 掃描 categories 資料夾 =====s
# images_map: basename -> {'img_paths': set(), 'xml_paths': set(), 'categories': set()}
images_map = {}

categories = []
for name in os.listdir(SOURCE_CATEGORIES_DIR):
    cat_path = os.path.join(SOURCE_CATEGORIES_DIR, name)
    if not os.path.isdir(cat_path):
        continue
    categories.append(name)

categories.sort()
print("找到 categories:", categories)

for cat in categories:
    cat_images_dir = os.path.join(SOURCE_CATEGORIES_DIR, cat, "images")
    cat_xmls_dir = os.path.join(SOURCE_CATEGORIES_DIR, cat, "xmls")

    if not os.path.isdir(cat_images_dir):
        print(f"[WARN] {cat_images_dir} not found, skip images for {cat}")
        continue

    # 圖片
    for fn in os.listdir(cat_images_dir):
        base, ext = os.path.splitext(fn)
        if ext.lower() not in IMAGE_EXTS:
            continue
        img_path = os.path.join(cat_images_dir, fn)
        entry = images_map.setdefault(base, {"img_paths": set(), "xml_paths": set(), "categories": set()})
        entry["img_paths"].add(img_path)
        entry["categories"].add(cat)

    # xmls (有些 category 可能沒有 xmls 資料夾)
    if os.path.isdir(cat_xmls_dir):
        for fn in os.listdir(cat_xmls_dir):
            base, ext = os.path.splitext(fn)
            if ext.lower() != ".xml":
                continue
            xml_path = os.path.join(cat_xmls_dir, fn)
            entry = images_map.setdefault(base, {"img_paths": set(), "xml_paths": set(), "categories": set()})
            entry["xml_paths"].add(xml_path)

n_total = len(images_map)
print(f"總共發現唯一圖片數 (basename): {n_total}")

if n_total == 0:
    raise SystemExit("沒有找到任何圖片，請檢查 SOURCE_CATEGORIES_DIR 路徑與子資料夾結構。")

# ===== 建立可分配的列表並 shuffle =====
random.seed(SEED)
all_basenames = list(images_map.keys())
random.shuffle(all_basenames)

n_train = int(n_total * TRAIN_RATIO)
n_val = int(n_total * VAL_RATIO)
# 調整保證總和正確（把剩下都當 test）
n_test = n_total - n_train - n_val

train_keys = all_basenames[:n_train]
val_keys = all_basenames[n_train:n_train + n_val]
test_keys = all_basenames[n_train + n_val:]

print(f"分配結果: train={len(train_keys)}, val={len(val_keys)}, test={len(test_keys)} (總 {n_total})")

# ===== 複製檔案到目標 =====
def pick_image_path(img_paths_set):
    """從 set 選一個較合適的 image path（優先 jpg，再 jpeg，再 png）"""
    if not img_paths_set:
        return None
    # 依 extension 優先順序選取
    preferred = [".jpg", ".jpeg", ".png", ".bmp"]
    for ext in preferred:
        for p in img_paths_set:
            if p.lower().endswith(ext):
                return p
    # fallback
    return next(iter(img_paths_set))

def copy_for_split(basenames, split_name):
    copied = 0
    missing_xml = 0
    for base in basenames:
        entry = images_map[base]
        img_src = pick_image_path(entry["img_paths"])
        xml_src = None
        if entry["xml_paths"]:
            # 若 xml 有多個，隨便選一個（通常只有一個）
            xml_src = sorted(entry["xml_paths"])[0]

        if img_src is None:
            print(f"[ERROR] {base} 沒有任何 image path，跳過")
            continue

        img_dst = os.path.join(TARGET_DIR, "images", split_name, os.path.basename(img_src))
        shutil.copy2(img_src, img_dst)
        if xml_src:
            xml_dst = os.path.join(TARGET_DIR, "xmls", split_name, os.path.basename(xml_src))
            shutil.copy2(xml_src, xml_dst)
        else:
            missing_xml += 1

        copied += 1
    return copied, missing_xml

copied_train, miss_train = copy_for_split(train_keys, "train")
copied_val, miss_val = copy_for_split(val_keys, "val")
copied_test, miss_test = copy_for_split(test_keys, "test")

print("複製完成。")
print(f"train: copied={copied_train}, missing_xml={miss_train}")
print(f"val:   copied={copied_val}, missing_xml={miss_val}")
print(f"test:  copied={copied_test}, missing_xml={miss_test}")

# ===== 印出每個 category 在各 split 的分佈（sanity check） =====
cat_counts = {cat: Counter() for cat in categories}
for split_name, keys in [("train", train_keys), ("val", val_keys), ("test", test_keys)]:
    for k in keys:
        for cat in images_map[k]["categories"]:
            cat_counts[cat][split_name] += 1

print("\n各 category 在各 split 的分佈 (count of images containing that category):")
for cat in categories:
    total_cat = sum(cat_counts[cat].values())
    print(f" - {cat}: total={total_cat}, train={cat_counts[cat]['train']}, val={cat_counts[cat]['val']}, test={cat_counts[cat]['test']}")

print("\n完成。請檢查 target 資料夾，並視需要把 XML 轉成 YOLO txt 標註。")
