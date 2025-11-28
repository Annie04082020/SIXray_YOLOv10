import pandas as pd
import os

# --- 設定變數 ---
# 1. 存放所有 CSV 檔案的資料夾路徑 (如果 CSV 在程式碼的同一個資料夾，可以使用 '.')
csv_folder_path = './csvs/'

# 2. 輸出 Excel 檔案的名稱
output_excel_file = 'Combined_100_Epoch_Data.xlsx'

# 3. 新增過濾條件：目標資料筆數 (即 '100 epochs' 的資料筆數，不含標頭列)
TARGET_ROWS = 100
# ----------------

# 建立 Excel 寫入器物件
try:
    writer = pd.ExcelWriter(output_excel_file, engine='openpyxl', mode='w')
except ImportError:
    print("Warning: openpyxl not found. Trying xlsxwriter.")
    writer = pd.ExcelWriter(output_excel_file, engine='xlsxwriter', mode='w')


print(f"正在掃描資料夾: {csv_folder_path}...")
print(f"本次只處理資料筆數為 {TARGET_ROWS} 的 CSV 檔案...")

processed_count = 0
processed_files = [] # 記錄所有成功寫入的檔名 (即符合 100 筆資料條件)

# 迴圈遍歷資料夾中的所有檔案
for filename in os.listdir(csv_folder_path):
    # 確保只處理以 .csv 結尾的檔案
    if filename.endswith(".csv"):
        file_path = os.path.join(csv_folder_path, filename)
        
        # 1. 讀取 CSV 檔案
        try:
            # 嘗試使用 utf-8 讀取，如果失敗則嘗試 big5
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file_path, encoding='big5')
            except Exception as e:
                print(f"  > 錯誤：無法讀取檔案 {filename} - {e}")
                continue # 跳過當前檔案
        except Exception as e:
            print(f"  > 錯誤：讀取檔案 {filename} 時發生其他問題 - {e}")
            continue

        # 2. 檢查資料筆數 (DataFrame 的長度即為資料列數，不包含標頭)
        data_rows = len(df)

        if data_rows == TARGET_ROWS:
            # 3. 決定工作表名稱 (使用 CSV 檔案名，去除副檔名)
            sheet_name = os.path.splitext(filename)[0]
            sheet_name = sheet_name[:31] # 確保名稱不超過 31 個字元

            # 4. 將 DataFrame 寫入 Excel 檔案的一個新的工作表
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"✅ 成功寫入：{filename} (資料筆數：{data_rows}) -> 工作表: {sheet_name}")
            processed_files.append(filename) # 記錄檔案名
            processed_count += 1
        else:
            print(f"🚫 略過檔案：{filename} (資料筆數：{data_rows}，不等於 {TARGET_ROWS})")


# 5. 儲存並關閉 Excel 寫入器
try:
    writer.close()
    
    print("\n-------------------------------------------------")
    print(f"🎉 **操作完成！**")
    print(f"總共處理了 {processed_count} 個符合條件的 CSV 檔案。")
    print(f"所有資料已儲存到檔案: **{output_excel_file}**")
    
    # 輸出符合條件的檔案列表 (讓您知道是哪一次訓練)
    if processed_files:
        print("\n--- ✅ 成功寫入 Excel 的 CSV 檔名 (即跑完 100 epoch 的訓練) ---")
        for file in processed_files:
            print(f"  > {file}")
        print("--------------------------------------------------")
    else:
        print("\n⚠️ 沒有找到符合 100 筆資料條件的 CSV 檔案。")

except Exception as e:
    print(f"\n❌ 錯誤：儲存 Excel 檔案時發生問題 - {e}")