import os
import shutil
import xml.etree.ElementTree as ET

# ===== 設定路徑 =====
positive_img_dir = "./../SIXray/Image"   # 原始圖片資料夾
positive_xml_dir = "./../SIXray/positive-Annotation"     # 原始 XML 資料夾
output_dir = "./../SIXray_Categories"       # 複製後的類別資料夾根目錄

# 違禁品種類列表
categories = ["Gun", "Knife", "Wrench", "Pliers", "Scissors"]

# 確保每個類別資料夾存在
for cat in categories:
    os.makedirs(os.path.join(output_dir, cat, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, cat, "xmls"), exist_ok=True)

# ===== 讀 XML 並複製 =====
xml_files = [f for f in os.listdir(positive_xml_dir) if f.endswith(".xml")]

for xml_file in xml_files:
    xml_path = os.path.join(positive_xml_dir, xml_file)
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        objects = root.findall("object")
        
        # 取出該圖裡的所有違禁品種類
        obj_categories = set()
        for obj in objects:
            name_tag = obj.find("name")
            if name_tag is not None:
                obj_categories.add(name_tag.text)
        
        # 對每個種類複製檔案
        for cat in obj_categories:
            if cat in categories:
                # 對應圖片檔名
                img_file = os.path.splitext(xml_file)[0] + ".jpg"
                src_img_path = os.path.join(positive_img_dir, img_file)
                dst_img_path = os.path.join(output_dir, cat, "images", img_file)
                dst_xml_path = os.path.join(output_dir, cat, "xmls", xml_file)
                
                if os.path.exists(src_img_path):
                    shutil.copy2(src_img_path, dst_img_path)
                else:
                    print(f"[WARNING] 圖片不存在: {img_file}")
                
                shutil.copy2(xml_path, dst_xml_path)
                
    except ET.ParseError:
        print(f"[ERROR] 無法解析 XML: {xml_file}")

print("複製完成！")
