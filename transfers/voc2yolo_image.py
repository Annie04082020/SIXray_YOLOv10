import os
import xml.etree.ElementTree as ET
from pathlib import Path
from tqdm import tqdm
import yaml

# --- 輔助函式：從 YAML 載入類別 ---

def load_classes_from_yaml(yaml_path):
    """從 dataset.yaml 檔案中讀取類別名稱。"""
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            names_dict = data.get('names', {})
            # 確保按照索引 0, 1, 2... 的順序來取得名稱
            classes = [names_dict[i] for i in sorted(names_dict.keys())]
            return classes
    except Exception as e:
        print(f"❌ 無法讀取或解析 YAML 檔案 {yaml_path}: {e}")
        return []

# --- 轉換邏輯 ---

def convert_annotation(xml_file, txt_file, CLASSES_list):
    """將單個 VOC XML 轉換為 YOLO TXT 格式，並返回標註行列表。"""
    
    # 檢查 XML 檔案是否存在。若不存在，直接返回空列表 (作為 Negative 樣本)
    if not xml_file.exists():
        return [] 
    
    lines = []
    
    try:
        tree = ET.parse(xml_file)
    except ET.ParseError:
        print(f"⚠️ 無法解析 XML 檔案，跳過標註轉換: {xml_file.name}")
        return lines

    root = tree.getroot()
    size = root.find("size")
    if size is None:
        print(f"⚠️ {xml_file.name} 缺少 <size> 標籤，無法計算座標，跳過")
        return lines
    
    try:
        w = float(size.find("width").text)
        h = float(size.find("height").text)
    except:
        print(f"⚠️ {xml_file.name} 的 <size> 內容有問題，無法計算座標，跳過")
        return lines

    for obj in root.findall("object"):
        name_tag = obj.find("name")
        cls = name_tag.text.strip().lower() if name_tag is not None and name_tag.text is not None else None

        if cls is None or cls not in CLASSES_list:
            if cls is not None:
                 print(f"⚠️ {xml_file.name} 出現未知類別: {cls}，跳過物件")
            continue

        cls_id = CLASSES_list.index(cls)

        bndbox = obj.find("bndbox") 
        if bndbox is None:
            print(f"⚠️ {xml_file.name} 的 <object> 沒有 bndbox，跳過物件")
            continue

        try:
            xmin = float(bndbox.find("xmin").text)
            ymin = float(bndbox.find("ymin").text)
            xmax = float(bndbox.find("xmax").text)
            ymax = float(bndbox.find("ymax").text)
        except:
            print(f"⚠️ {xml_file.name} 的 bndbox 座標有問題，跳過物件")
            continue
            
        # 邊界檢查：避免除以零或寬高為零/負數
        if w <= 0 or h <= 0 or xmax <= xmin or ymax <= ymin:
            print(f"⚠️ {xml_file.name} 的尺寸或邊界框無效，跳過物件")
            continue

        # YOLO 格式轉換
        x_center = (xmin + xmax) / 2 / w
        y_center = (ymin + ymax) / 2 / h
        width = (xmax - xmin) / w
        height = (ymax - ymin) / h
        
        # 檢查 YOLO 座標是否在 0 到 1 之間
        if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= width <= 1 and 0 <= height <= 1):
             print(f"⚠️ {xml_file.name} 轉換後的 YOLO 座標超出範圍，跳過物件")
             continue

        lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
        
    return lines # 返回標註行列表

def process_split(base_dir, split, CLASSES_list, unified_xml_dir):
    """根據 images/{split} 資料夾的檔案清單，從統一的 XML 資料夾中進行轉換。"""
    
    image_dir = base_dir / "images" / split
    label_dir = base_dir / "labels" / split
    
    if not image_dir.is_dir():
        print(f"❌ 找不到圖片資料夾: {image_dir}，跳過 {split} 處理。")
        return

    # 1. 以 images 資料夾中的 .jpg 檔名為準
    image_files = list(image_dir.glob("*.jpg"))
    
    if not image_files:
        print(f"ℹ️ {image_dir} 中沒有找到 JPG 圖片檔案。")
        return

    print(f"\n--- 開始處理 {split} (共 {len(image_files)} 張圖片) ---")
    label_dir.mkdir(parents=True, exist_ok=True) # 確保 labels 資料夾存在

    for img_file in tqdm(image_files, desc=f"Processing {split} files"):
        file_stem = img_file.stem # 取得檔名 (不含副檔名), 例如 P00001

        # *** 關鍵修改：從統一的資料夾尋找 XML ***
        xml_file = unified_xml_dir / f"{file_stem}.xml" 
        txt_file = label_dir / f"{file_stem}.txt"
        
        # 2. 執行轉換邏輯
        lines = convert_annotation(xml_file, txt_file, CLASSES_list)
        
        # 3. 寫入 TXT 檔案 (無論是否有物件都寫入，以覆蓋或生成空白 TXT)
        with open(txt_file, "w") as f:
            f.write("\n".join(lines))

    print(f"✅ {split} 分割處理完成。已在 {label_dir} 生成所有標註檔案 (含空白 TXT)。")

if __name__ == "__main__":
    
    # 1. 載入類別名稱
    YAML_PATH = Path("./../SIXray_compressed/dataset.yaml") 
    GLOBAL_CLASSES = load_classes_from_yaml(YAML_PATH)
    
    if not GLOBAL_CLASSES:
        print("❌ 類別列表是空的。請確認 dataset.yaml 檔案存在且內容正確。")
        exit()
        
    print(f"ℹ️ 從 YAML 載入的類別: {GLOBAL_CLASSES}")
        
    # 2. 定義基礎路徑和 XML 統一路徑
    base_dir = Path("./../../SIXray_YOLO") 
    
    # *** 假設所有的 XML 檔案都集中在這個資料夾內 ***
    # 請根據您實際存放 XML 檔案的位置來調整這個路徑。
    # 假設您將所有 XML 檔都放在 SIXray_YOLO/xmls/ 下
    UNIFIED_XML_DIR = base_dir / "xml_all" 

    if not UNIFIED_XML_DIR.is_dir():
        print(f"❌ 找不到 XML 統一資料夾: {UNIFIED_XML_DIR}。請確認您已將所有 XML 檔移入此處。")
        exit()


    # 3. 執行轉換
    for split in ["train", "val", "test"]:
        # 將 XML 統一路徑傳入
        process_split(base_dir, split, GLOBAL_CLASSES, UNIFIED_XML_DIR)

    print("\n====================================")
    print("✅ VOC -> YOLO 轉換及 Labels 建立完成！")
    print("已成功根據 Images 分割資料夾和統一的 XML 資料夾進行轉換。")
    print("====================================")