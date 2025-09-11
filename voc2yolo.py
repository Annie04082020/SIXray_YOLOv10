import os
import xml.etree.ElementTree as ET
from pathlib import Path
from tqdm import tqdm

# 定義你的類別
CLASSES = [ "gun","knife", "wrench", "pliers", "scissors"]

def convert_annotation(xml_file, txt_file):
    try:
        tree = ET.parse(xml_file)
    except ET.ParseError:
        print(f"⚠️ 無法解析 {xml_file}")
        return
    
    root = tree.getroot()
    size = root.find("size")
    w = float(size.find("width").text)
    h = float(size.find("height").text)

    lines = []
    for obj in root.findall("object"):
        name_tag = obj.find("name")
        if name_tag is None or name_tag.text is None:
            print(f"⚠️ {xml_file} 有空的 <object>，跳過")
            continue

        cls = name_tag.text.strip().lower()
        if cls not in CLASSES:
            print(f"⚠️ {xml_file} 出現未知類別: {cls}，跳過")
            continue

        cls_id = CLASSES.index(cls)

        bndbox = obj.find("bndbox")
        if bndbox is None:
            print(f"⚠️ {xml_file} 的 <object> 沒有 bndbox，跳過")
            continue

        try:
            xmin = float(bndbox.find("xmin").text)
            ymin = float(bndbox.find("ymin").text)
            xmax = float(bndbox.find("xmax").text)
            ymax = float(bndbox.find("ymax").text)
        except:
            print(f"⚠️ {xml_file} 的 bndbox 有問題，跳過")
            continue

        # YOLO 格式
        x_center = (xmin + xmax) / 2 / w
        y_center = (ymin + ymax) / 2 / h
        width = (xmax - xmin) / w
        height = (ymax - ymin) / h

        lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    if lines:
        txt_file.parent.mkdir(parents=True, exist_ok=True)
        with open(txt_file, "w") as f:
            f.write("\n".join(lines))

def process_split(xml_dir, label_dir):
    xml_dir = Path(xml_dir)
    label_dir = Path(label_dir)
    xml_files = list(xml_dir.glob("*.xml"))
    for xml_file in tqdm(xml_files, desc=f"Processing {xml_dir}"):
        txt_file = label_dir / (xml_file.stem + ".txt")
        convert_annotation(xml_file, txt_file)

if __name__ == "__main__":
    base_dir = Path("./../SIXray_YOLO")
    for split in ["train", "val", "test"]:
        xml_dir = base_dir / "xmls" / split
        label_dir = base_dir / "labels" / split
        process_split(xml_dir, label_dir)

    print("✅ VOC -> YOLO 轉換完成！")
