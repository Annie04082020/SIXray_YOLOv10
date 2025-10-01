import os
from pathlib import Path

def verify_dataset(base_dir, splits):
    """驗證 Image 與 Label 的檔名是否完全對應，並檢查 P 開頭的 Label 是否包含標註內容。"""
    
    base_dir = Path(base_dir)
    print(f"--- 開始驗證數據集完整性 (基礎路徑: {base_dir.resolve()}) ---")
    
    overall_status = True
    all_empty_p_files = [] # 用來收集所有分割中空白的 P-files
    
    for split in splits:
        print(f"\n====================================")
        print(f"🔬 檢查分割: {split}")
        print(f"====================================")
        
        image_dir = base_dir / "images" / split
        label_dir = base_dir / "labels" / split
        
        if not image_dir.is_dir() or not label_dir.is_dir():
            print(f"❌ 警告: 找不到 {split} 分割的 images 或 labels 資料夾。")
            overall_status = False
            continue

        # 1. 取得所有檔案名稱 (不含副檔名)
        image_stems = {f.stem for f in image_dir.glob("*.jpg")}
        label_stems = {f.stem for f in label_dir.glob("*.txt")}
        
        
        # --- 檢查 1：檔案數量與名稱對應性 (保持不變) ---
        
        missing_labels = image_stems - label_stems
        extra_labels = label_stems - image_stems
        
        if missing_labels or extra_labels:
            print(f"❌ 檢查 1 失敗: 檔案對應失敗！(Image 數量: {len(image_stems)}, Label 數量: {len(label_stems)})")
            # 這裡只印出警告，讓程式繼續檢查 P-files
            overall_status = False
        else:
            print("✅ 檢查 1 通過: Image 檔案與 Label 檔案數量及名稱完全匹配。")

            
        # --- 檢查 2：P 開頭的 Label 檔案是否包含內容 (應為 Positive 樣本) ---
        
        p_files_to_check = [s for s in label_stems if s.startswith('P')]
        empty_p_files_in_split = []
        
        for stem in p_files_to_check:
            label_file_path = label_dir / f"{stem}.txt"
            
            try:
                content = label_file_path.read_text(encoding='utf-8').strip()
                
                # 如果 strip() 之後內容為空，表示 P 開頭檔案缺少標註
                if not content: 
                    empty_p_files_in_split.append(f"{split}/{stem}.txt") # 記錄完整路徑 (分割/檔名)
                    
            except Exception as e:
                print(f"⚠️ 讀取檔案失敗 {stem}.txt: {e}")
                overall_status = False

        if empty_p_files_in_split:
            print(f"❌ 檢查 2 失敗: 有 {len(empty_p_files_in_split)} 個 P 開頭的 Label 檔案是空白的 (應包含內容)。")
            # 將這個分割的錯誤檔案加入總列表
            all_empty_p_files.extend(empty_p_files_in_split)
            overall_status = False
        else:
            print(f"✅ 檢查 2 通過: 所有 {len(p_files_to_check)} 個 P 開頭的 Label 檔案都包含內容。")
            
    
    print("\n----------------------------------------------------")
    if all_empty_p_files:
        print("🔴 總結：標註失敗的 P 開頭檔案清單 (空白 TXT)：")
        # 完整列出所有有問題的檔案
        for f in all_empty_p_files:
            print(f"    - {f}")
        print(f"\n請回去檢查這些檔案對應的 XML ({len(all_empty_p_files)} 個) 是否有錯誤。")
    elif overall_status:
        print("🎉 恭喜！數據集驗證全部通過，Image 與 Label 完全對應，且 P 檔案內容正確。")
    else:
        print("⚠️ 驗證失敗！請根據上述錯誤訊息修正對應的檔案。")
    print("----------------------------------------------------")


if __name__ == "__main__":
    
    # *** 請根據您的實際路徑修改 base_dir ***
    BASE_DIR = Path("./../SIXray_YOLO") 
    
    SPLITS = ["train", "val", "test"]
    
    verify_dataset(BASE_DIR, SPLITS)