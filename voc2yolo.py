import os
import xml.etree.ElementTree as ET
from pathlib import Path
from tqdm import tqdm
import yaml

# 從 dataset.yaml 載入類別
def load_classes_from_yaml(yaml_path):
    """從 dataset.yaml 檔案中讀取類別名稱。"""
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            # names 是一個字典 {0: 'gun', 1: 'knife', ...}
            # 我們需要按鍵排序後取出值
            names_dict = data.get('names', {})
            # 確保按照索引 0, 1, 2... 的順序來取得名稱
            classes = [names_dict[i] for i in sorted(names_dict.keys())]
            return classes
    except Exception as e:
        print(f"❌ 無法讀取或解析 YAML 檔案 {yaml_path}: {e}")
        # 如果失敗，使用預設的，但請注意可能與 dataset.yaml 不符
        return [ "gun", "knife", "wrench", "pliers", "scissors"]

# 預先定義一個空的 CLASSES 列表，稍後會從 YAML 載入
CLASSES = []

def convert_annotation(xml_file, txt_file, CLASSES_list):
    try:
        tree = ET.parse(xml_file)
    except ET.ParseError:
        print(f"⚠️ 無法解析 {xml_file}")
        return
    
    root = tree.getroot()
    size = root.find("size")
    if size is None:
        print(f"⚠️ {xml_file} 缺少 <size> 標籤，跳過")
        return
    
    try:
        w = float(size.find("width").text)
        h = float(size.find("height").text)
    except:
        print(f"⚠️ {xml_file} 的 <size> 內容有問題，跳過")
        return

    lines = []
    for obj in root.findall("object"):
        name_tag = obj.find("name")
        if name_tag is None or name_tag.text is None:
            print(f"⚠️ {xml_file} 有空的 <object> 名稱，跳過")
            continue

        # 將類別名稱轉為小寫，並去除前後空白，以匹配
        cls = name_tag.text.strip().lower()
        
        # 使用傳入的 CLASSES_list 進行檢查
        if cls not in CLASSES_list:
            # *重要提醒：您的 dataset.yaml 中是 'pilers'，但一般應為 'pliers'。*
            # 為了讓程式正常運作，這裡會依據 YAML 檔案中讀到的為準。
            print(f"⚠️ {xml_file} 出現未知類別: {cls} (請確認它是否在 dataset.yaml 中)，跳過")
            continue

        cls_id = CLASSES_list.index(cls)

        bndbox = obj.find("bndbox")
        if bndbox is None:
            print(f"⚠️ {xml_file} 的 <object> 沒有 bndbox，跳過")
            continue

        try:
            # 確保座標轉換為 float
            xmin = float(bndbox.find("xmin").text)
            ymin = float(bndbox.find("ymin").text)
            xmax = float(bndbox.find("xmax").text)
            ymax = float(bndbox.find("ymax").text)
        except Exception as e:
            print(f"⚠️ {xml_file} 的 bndbox 座標有問題 ({e})，跳過")
            continue
            
        # 進行邊界檢查，避免除以零或寬高為負
        if w <= 0 or h <= 0 or xmax <= xmin or ymax <= ymin:
            print(f"⚠️ {xml_file} 的尺寸或邊界框無效 (W:{w}, H:{h}, Xmin:{xmin}, Ymax:{ymax})，跳過")
            continue

        # YOLO 格式轉換
        x_center = (xmin + xmax) / 2 / w
        y_center = (ymin + ymax) / 2 / h
        width = (xmax - xmin) / w
        height = (ymax - ymin) / h
        
        # 檢查 YOLO 座標是否在 0 到 1 之間
        if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= width <= 1 and 0 <= height <= 1):
             print(f"⚠️ {xml_file} 轉換後的 YOLO 座標超出範圍，可能原始座標有誤: {x_center:.3f}, {y_center:.3f}, {width:.3f}, {height:.3f}，跳過")
             continue


        lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    if lines:
        txt_file.parent.mkdir(parents=True, exist_ok=True)
        with open(txt_file, "w") as f:
            f.write("\n".join(lines))

def process_split(xml_dir, label_dir, CLASSES_list):
    xml_dir = Path(xml_dir)
    label_dir = Path(label_dir)
    
    # 檢查 XML 資料夾是否存在
    if not xml_dir.is_dir():
        print(f"❌ 找不到 XML 資料夾: {xml_dir}。請檢查路徑設定是否正確。")
        return

    xml_files = list(xml_dir.glob("*.xml"))
    if not xml_files:
        print(f"ℹ️ {xml_dir} 中沒有找到 XML 檔案。")
        return
        
    for xml_file in tqdm(xml_files, desc=f"Processing {xml_dir.parts[-2]}/{xml_dir.parts[-1]}"):
        txt_file = label_dir / (xml_file.stem + ".txt")
        # 傳入類別列表
        convert_annotation(xml_file, txt_file, CLASSES_list)

if __name__ == "__main__":
    
    # 1. 載入類別名稱
    # 假設 dataset.yaml 檔案與 voc2yolo.py 在同一個目錄下，或者你知道它的絕對或相對路徑。
    # 如果您的程式碼是放在一個專案資料夾內，請根據實際情況修改路徑。
    YAML_PATH = Path("./../SIXray_compressed/dataset.yaml") 
    GLOBAL_CLASSES = load_classes_from_yaml(YAML_PATH)
    
    if not GLOBAL_CLASSES:
        print("❌ 類別列表是空的。請確認 dataset.yaml 檔案存在且內容正確。")
    else:
        print(f"ℹ️ 從 YAML 載入的類別: {GLOBAL_CLASSES}")
        
    # 2. 定義基礎路徑
    # 根據您的 voc2yolo.py 內原始路徑：base_dir = Path("./../SIXray_YOLO") 
    # 以及 dataset.yaml 內的路徑：path: D://SIXray_YOLO
    # 如果您希望 XML 檔案在 D://SIXray_YOLO/xmls/train, val, test 
    # 且 Label 檔案輸出到 D://SIXray_YOLO/labels/train, val, test
    # 您需要確定這個 base_dir 指向 SIXray_YOLO 資料夾
    # 這裡假設您的執行目錄層級和原始腳本設定一致
    # 根據您的檔案結構，我假定您希望 `base_dir` 指向專案根目錄或 `SIXray_YOLO` 上一層。
    # 如果您的 xml 資料夾在 D://SIXray_YOLO/xmls/train，請這樣設定：
    
    # ***請根據您的實際資料夾結構，選擇以下兩種 base_dir 設定之一***
    # 設定 A：如果您的 XML 資料夾路徑是 D://SIXray_YOLO/xmls/train 等
    # base_dir = Path("D://SIXray_YOLO") 
    
    # 設定 B (使用相對路徑，較靈活)：如果您的 voc2yolo.py 在某個目錄下，而 SIXray_YOLO 在其同級或上一級
    base_dir = Path("./../SIXray_compressed") # 保持您原來的相對路徑設定

    for split in ["train", "val", "test"]:
        # XML 檔案應在 base_dir/xmls/split_name
        xml_dir = base_dir / "xmls" / split
        # 輸出 YOLO label 檔案到 base_dir/labels/split_name
        label_dir = base_dir / "labels" / split
        # 將類別列表傳入
        process_split(xml_dir, label_dir, GLOBAL_CLASSES)

    print("---")
    print("✅ VOC -> YOLO 轉換完成！")