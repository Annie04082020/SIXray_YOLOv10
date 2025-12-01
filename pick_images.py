import os
import shutil
import random

def pick_images_by_list(src_root, dst_root, folder_list, num_per_folder=5):
    
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    
    # 轉換成絕對路徑，方便比對與除錯
    src_root = os.path.abspath(src_root)
    dst_root = os.path.abspath(dst_root)

    # 防呆檢查：如果來源跟目標完全一樣，直接停止
    if src_root == dst_root:
        print(f"Error: 來源路徑與輸出路徑相同！請修改 output_folder。\n路徑: {src_root}")
        return

    if not os.path.exists(dst_root):
        os.makedirs(dst_root)

    print(f"準備處理 {len(folder_list)} 個指定的資料夾...\n")
    print(f"來源: {src_root}")
    print(f"輸出: {dst_root}\n")

    for folder_name in folder_list:
        # 組合路徑
        images_src_path = os.path.join(src_root, folder_name, "images")
        
        if os.path.exists(images_src_path) and os.path.isdir(images_src_path):
            all_files = os.listdir(images_src_path)
            images = [f for f in all_files if f.lower().endswith(valid_extensions)]
            
            if images:
                count = min(len(images), num_per_folder)
                selected_images = random.sample(images, count)
                
                target_dir = os.path.join(dst_root, folder_name)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                print(f"[O] 處理中: {folder_name} -> 複製 {count} 張")
                
                for img_name in selected_images:
                    src_file = os.path.join(images_src_path, img_name)
                    dst_file = os.path.join(target_dir, img_name)
                    
                    try:
                        shutil.copy2(src_file, dst_file)
                    except shutil.SameFileError:
                        print(f"    [!] 跳過: 來源與目標是同一個檔案 ({img_name})")
                    except Exception as e:
                        print(f"    [X] 錯誤: {e}")

            else:
                print(f"[!] {folder_name}: 找到了 images 資料夾，但沒有圖片")
        else:
            print(f"[X] 跳過: {folder_name} (路徑不存在: {images_src_path})")

    print("\n--- 全部完成 ---")

# --- 設定區域 ---
if __name__ == "__main__":
    source_folder = "./../SIXray_YOLO"  # 你的原始資料夾路徑
    output_folder = "./../SIXray_YOLO/detections_100"  # 輸出路徑
    images_to_take = 100               # 每個資料夾拿幾張
    
    # 【重點】請在這裡填入你要的資料夾名稱
    # 只需要填子資料夾的名字，例如 "cat", "dog"
    target_folders = [
        "Gun",
        "Knife",
        "Pliers",
        "Scissors",
        "Wrench",
        "negative_subset"
    ]
    
    pick_images_by_list(source_folder, output_folder, target_folders, images_to_take)