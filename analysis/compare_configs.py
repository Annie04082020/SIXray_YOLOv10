import pandas as pd
import yaml
import glob
import os
from typing import List, Dict, Any

def read_yaml_config(file_path: str) -> Dict[str, Any]:
    """
    讀取單個 YAML 檔案並返回其內容的字典。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 載入 YAML 檔案
            data = yaml.safe_load(f)
            return data
    except Exception as e:
        print(f"🚨 讀取檔案失敗: {file_path}. 錯誤: {e}")
        return {}

def load_and_compare_configs(folder_path: str, file_pattern: str = "*.args.yaml") -> pd.DataFrame:
    """
    載入指定資料夾中所有符合模式的 YAML 設定檔，並整理成一個 Pandas DataFrame。

    參數:
        folder_path (str): 包含訓練參數設定檔的資料夾路徑。
        file_pattern (str): 要搜尋的檔案模式 (e.g., "*.args.yaml")。
    
    回傳:
        pd.DataFrame: 包含所有訓練參數的表格。
    """
    # 組合完整的搜尋路徑
    search_path = os.path.join(folder_path, file_pattern)
    
    # 找出所有符合模式的檔案路徑
    config_files: List[str] = glob.glob(search_path)
    
    print(f"✅ 找到 {len(config_files)} 個設定檔。")
    
    all_configs: List[Dict[str, Any]] = []
    
    for file_path in config_files:
        # 讀取 YAML 內容
        config_data = read_yaml_config(file_path)
        
        if config_data:
            # 從檔案名稱中提取訓練名稱作為識別 ID
            # 假設檔案名稱是 trainXX.args.yaml，我們取 trainXX
            file_name = os.path.basename(file_path)
            config_id = file_name.replace('.args.yaml', '')
            
            # 將識別 ID 加入到數據字典中
            config_data['config_name'] = config_id
            
            all_configs.append(config_data)

    # 將所有字典轉換為 Pandas DataFrame
    if all_configs:
        df = pd.DataFrame(all_configs)
        # 將 config_name 欄位移動到最前面
        cols = ['config_name'] + [col for col in df.columns if col != 'config_name']
        df = df[cols]
        return df
    else:
        print("⚠️ 沒有找到任何可用的設定檔。")
        return pd.DataFrame()


# --- 主程式區塊 ---
if __name__ == "__main__":
    # 🔴 【請修改此處】設定您的設定檔所在的資料夾路徑
    # 假設您的所有 trainXX.args.yaml 都在這個資料夾裡
    target_folder = "./analysis_data"
    
    # 呼叫主函式
    comparison_df = load_and_compare_configs(target_folder, file_pattern="train*.args.yaml")

    # 顯示結果
    if not comparison_df.empty:
        print("\n--- 📝 訓練參數比較表格 (前五行) ---")
        print(comparison_df.head())
        
        # 🟢 【可選】將結果儲存為 CSV 檔案
        output_file = "training_configs_comparison.csv"
        comparison_df.to_csv(output_file, index=False)
        print(f"\n✨ 完整的比較表格已儲存到: {output_file}")