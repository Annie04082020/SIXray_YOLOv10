import os
from ultralytics import YOLOv10

def detect_all_folders(source_root, output_root, model_path):
    """
    遍歷 source_root 下的所有子資料夾，使用 YOLOv10 進行偵測，
    並將結果依據資料夾名稱存入 output_root。
    """
    
    # 1. 載入模型
    print(f"正在載入模型: {model_path} ...")
    try:
        model = YOLOv10.from_pretrained(model_path)
    except Exception as e:
        # 如果 from_pretrained 失敗，嘗試標準載入方式 (視你的安裝版本而定)
        print(f"from_pretrained 載入失敗，嘗試直接載入: {e}")
        model = YOLOv10(model_path)

    # 確保輸出資料夾存在
    if not os.path.exists(output_root):
        os.makedirs(output_root)

    # 2. 取得所有子資料夾 (例如 Gun, Knife...)
    subfolders = [d for d in os.listdir(source_root) if os.path.isdir(os.path.join(source_root, d))]
    
    print(f"找到 {len(subfolders)} 個資料夾，準備開始偵測...\n")

    # 3. 逐一偵測
    for folder_name in subfolders:
        # 建構完整的來源路徑，例如 .../My_Selected_Images/Gun
        current_source = os.path.join(source_root, folder_name)
        
        print(f"--- 正在偵測: {folder_name} ---")
        
        # 執行預測
        # project: 輸出的主目錄
        # name: 輸出的子目錄 (這裡設定為資料夾名稱，例如 Gun)
        # exist_ok=True: 如果資料夾已存在，不要建立 Gun2, Gun3，直接寫入
        model.predict(
            source=current_source,
            save=True,
            project=output_root,
            name=folder_name,
            exist_ok=True,
            conf=0.25,
            imgsz=640
        )

    print(f"\n全部完成！結果已儲存至: {output_root}")

if __name__ == "__main__":
    # --- 設定路徑 (請修改這裡) ---
    
    # 1. 剛剛用程式抓出來的圖片資料夾 (你的來源)
    # 請填入上一一個步驟的 output_folder
    images_source_dir = "./../SIXray_YOLO/detections"
    
    # 2. 你希望偵測結果存到哪裡 (你的輸出)
    detection_output_dir = "./../SIXray_YOLO/detection_results"
    
    # 3. 權重檔路徑
    model_weight = 'savemodel/yolov10n_sixray25.pt'
    
    # 執行
    detect_all_folders(images_source_dir, detection_output_dir, model_weight)