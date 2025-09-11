import os
import shutil
import random

# --------- 設定路徑 ---------
negative_dir = "./../SIXray/JPEGImages"  # 原始負樣本資料夾
output_dir = "./../SIXray_YOLO"  # 最終 YOLO 資料夾

splits = {
    "train": 0.8,
    "test": 0.2,
}

# 先建立資料夾結構
for split in ["train", "val", "test"]:
    for folder in ["images", "labels"]:
        os.makedirs(os.path.join(output_dir, split, folder), exist_ok=True)

# --------- 取得所有圖片 ---------
all_imgs = [f for f in os.listdir(negative_dir) if f.lower().endswith(".jpg")]
random.shuffle(all_imgs)

# --------- 切分 train/test ---------
num_total = len(all_imgs)
num_train = int(num_total * splits["train"])
train_imgs = all_imgs[:num_train]
test_imgs = all_imgs[num_train:]

# --------- 從 train 再切 val ---------
num_val = int(len(train_imgs) * 0.1)
val_imgs = train_imgs[:num_val]
train_imgs = train_imgs[num_val:]

split_dict = {
    "train": train_imgs,
    "val": val_imgs,
    "test": test_imgs
}

# --------- 複製圖片並產生空的 labels ---------
for split, imgs in split_dict.items():
    for img_name in imgs:
        # 複製圖片
        src_img = os.path.join(negative_dir, img_name)
        dst_img = os.path.join(output_dir, split, "images", img_name)
        shutil.copy2(src_img, dst_img)

        # 生成空 txt
        label_name = os.path.splitext(img_name)[0] + ".txt"
        label_path = os.path.join(output_dir, split, "labels", label_name)
        with open(label_path, "w") as f:
            pass  # 空檔案

print("Negative dataset 分割完成！")
print(f"Train: {len(train_imgs)}張, Val: {len(val_imgs)}張, Test: {len(test_imgs)}張")
