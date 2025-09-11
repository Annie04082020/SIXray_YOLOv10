# save as check_annotations.py
import os
import shutil
import xml.etree.ElementTree as ET

xml_dir = "./../SIXray/positive-Annotation"    # 改成你的 xml 資料夾
img_dir = "./../SIXray/Image"         # 改成你放圖的資料夾
out_review_dir = "/mnt/d/SIXray/review_empty"  # 用來放要人工檢視的影像
hammer_dir = "./../SIXray/empty_hammer_image"  # 放含 Hammer 的 xml

os.makedirs(out_review_dir, exist_ok=True)

empty_xmls = []
hammer_xmls = []
other_issue_xmls = []

def get_image_filename_from_xml(root):
    fn_tag = root.find('filename')
    if fn_tag is not None and fn_tag.text:
        return fn_tag.text.strip()
    return None

for fname in sorted(os.listdir(xml_dir)):
    if not fname.endswith('.xml'):
        continue
    xml_path = os.path.join(xml_dir, fname)
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        other_issue_xmls.append((xml_path, f"parse_error:{e}"))
        continue

    objects = root.findall('object')
    names = []
    for obj in objects:
        name_tag = obj.find('name')
        if name_tag is not None and name_tag.text:
            names.append(name_tag.text.strip())

    # 空標註
    if len(names) == 0:
        empty_xmls.append(xml_path)
        # 嘗試把對應影像複製過去 review folder，方便你手動打開看
        img_name = get_image_filename_from_xml(root)
        if img_name:
            # 如果 xml filename 是 P00001.xml 但 image 存 P00001.jpg
            img_path = os.path.join(img_dir, img_name)
            if os.path.exists(img_path):
                shutil.copy(img_path, out_review_dir)
            else:
                # 嘗試 jpg/png 副檔名
                for ext in ['.jpg', '.png', '.jpeg', '.bmp']:
                    alt = os.path.join(img_dir, os.path.splitext(img_name)[0] + ext)
                    if os.path.exists(alt):
                        shutil.copy(alt, out_review_dir)
                        break

    # 含 Hammer 的 xml（大小寫不敏感）
    if any(n.lower() == 'hammer' for n in names):
        hammer_xmls.append(xml_path)

# 輸出清單
print("===== 空標註 XML 清單（len={}） =====".format(len(empty_xmls)))
for p in empty_xmls:
    print(p)

print("\n===== 含 Hammer 的 XML 清單（len={}） =====".format(len(hammer_xmls)))
for p in hammer_xmls:
    print(p)

print("\n===== 讀取錯誤或其他問題 XML（len={}） =====".format(len(other_issue_xmls)))
for p, e in other_issue_xmls[:50]:
    print(p, e)

print("\n已把空標註對應影像複製到：", out_review_dir)
print(empty_xmls)

for filename in empty_xmls:
    img_path = filename.replace('.xml', '.jpg').replace('positive-Annotation', 'Image')
    print(img_path)
    # src_path = os.path.join(img_dir, img_path)
    # print(src_path)
    dst_path = img_path.replace('Image', 'empty_hammer_image')
    print(dst_path)
    
    if os.path.exists(img_path):
        shutil.move(img_path, dst_path)
        print(f"Moved {filename} to hammer folder.")
    else:
        print(f"{filename} not found in positive folder.")