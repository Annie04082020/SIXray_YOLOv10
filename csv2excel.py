import pandas as pd
import os

# --- 設定變數 ---
# 1. 存放所有 CSV 檔案的資料夾路徑 (如果 CSV 在程式碼的同一個資料夾，可以使用 '.')
csv_folder_path = './csvs/'

# 2. 輸出 Excel 檔案的名稱
output_excel_file = 'Combined_Data_Workbook.xlsx'
# ----------------

# 建立 Excel 寫入器物件 (使用 openpyxl 引擎)
# 'mode="w"' 表示寫入模式，會覆蓋現有檔案
try:
    writer = pd.ExcelWriter(output_excel_file, engine='openpyxl', mode='w')
except ImportError:
    # 如果 openpyxl 未安裝，可以嘗試使用 xlsxwriter
    print("Warning: openpyxl not found. Trying xlsxwriter.")
    writer = pd.ExcelWriter(output_excel_file, engine='xlsxwriter', mode='w')


print(f"正在掃描資料夾: {csv_folder_path}...")
processed_count = 0

# 迴圈遍歷資料夾中的所有檔案
for filename in os.listdir(csv_folder_path):
    # 確保只處理以 .csv 結尾的檔案
    if filename.endswith(".csv"):
        # 完整的 CSV 檔案路徑
        file_path = os.path.join(csv_folder_path, filename)

        # 1. 讀取 CSV 檔案
        # 由於 CSV 檔案的編碼可能不同，通常 'utf-8' 是標準，
        # 如果遇到亂碼，可以嘗試改為 'big5' 或 'gbk'
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            print(f"  > 嘗試使用 'big5' 讀取 {filename}...")
            df = pd.read_csv(file_path, encoding='big5')
        except Exception as e:
            print(f"  > 錯誤：無法讀取檔案 {filename} - {e}")
            continue # 跳過當前檔案，繼續處理下一個

        # 2. 決定工作表名稱 (通常使用 CSV 檔案名，但要去除副檔名並確保名稱不超過 31 個字元)
        sheet_name = os.path.splitext(filename)[0]
        # Excel 工作表名稱長度限制為 31 個字元
        sheet_name = sheet_name[:31]

        # 3. 將 DataFrame 寫入 Excel 檔案的一個新的工作表
        # index=False 表示不將 Pandas 內建的索引 (通常是數字) 寫入 Excel
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"✅ 已成功將 {filename} 寫入工作表: **{sheet_name}**")
        processed_count += 1

# 4. 儲存並關閉 Excel 寫入器，這一步是必要的！
try:
    writer.close()
    print("\n-------------------------------------------------")
    print(f"🎉 **操作完成！**")
    print(f"總共處理了 {processed_count} 個 CSV 檔案。")
    print(f"所有資料已儲存到檔案: **{output_excel_file}**")
    print("-------------------------------------------------")

except Exception as e:
    print(f"\n❌ 錯誤：儲存 Excel 檔案時發生問題 - {e}")