import os
from pathlib import Path

def find_missing_xmls(xml_dir, start_num, end_num, prefix="P", padding=5):
    """
    檢查指定目錄中 Pxxxx.xml 檔案序列是否有缺失。

    Args:
        xml_dir (Path): 存放所有 XML 檔案的目錄路徑。
        start_num (int): 序列的起始數字 (例如: 1)。
        end_num (int): 序列的結束數字 (例如: 8929)。
        prefix (str): 檔案名稱的前綴 (例如: "P")。
        padding (int): 數字部分的零填充位數 (例如: 5 表示 P00001)。
    """
    
    if not xml_dir.is_dir():
        print(f"❌ 錯誤：找不到 XML 資料夾: {xml_dir.resolve()}。請確認路徑設定是否正確。")
        return

    print(f"--- 開始檢查 {prefix} 系列 XML 檔案 (從 {prefix}{str(start_num).zfill(padding)}.xml 到 {prefix}{str(end_num).zfill(padding)}.xml) ---")

    # 1. 取得目錄中所有實際存在的 XML 檔名
    actual_files = {f.name for f in xml_dir.glob(f"{prefix}*.xml")}
    
    # 2. 生成所有預期存在的 XML 檔名
    expected_files = set()
    for i in range(start_num, end_num + 1):
        num_str = str(i).zfill(padding)
        expected_files.add(f"{prefix}{num_str}.xml")

    # 3. 找出預期存在但實際不存在的檔案 (缺失檔案)
    missing_files = sorted(list(expected_files - actual_files))

    # 4. 輸出結果
    if missing_files:
        print(f"\n🔴 發現 {len(missing_files)} 個 XML 檔案缺失：")
        for filename in missing_files:
            print(f"    - {filename}")
        print("\n⚠️ 請檢查這些檔案是否被遺漏或存放於其他位置。")
    else:
        print(f"\n🎉 恭喜！{prefix} 系列 XML 檔案 ({end_num} 個) 序列完整，沒有發現缺失。")


if __name__ == "__main__":
    
    # --- 請依照您的實際情況修改以下設定 ---
    
    # 1. XML 統一路徑設定 (假設在 SIXray_YOLO/xmls/ 下)
    # 如果您的 XML 統一放在 SIXray_YOLO/xmls，則不需要修改。
    BASE_DIR = Path("./../../SIXray_YOLO") 
    XML_ALL_DIR = BASE_DIR / "xml_all" 

    # 2. 檔案序列範圍設定
    START_NUMBER = 1
    END_NUMBER = 8929 
    
    # 3. 執行檢查
    find_missing_xmls(
        xml_dir=XML_ALL_DIR,
        start_num=START_NUMBER,
        end_num=END_NUMBER
    )