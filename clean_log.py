import re

input_file = 'training_logs/models_result/s_4th_1-65result.txt'
output_file = 'training_logs/models_result/s_4th_cleaned.txt'

# 匹配 YOLO 訓練進度的正則表達式 (包含 Epoch, 顯存, 各種 Loss)
# 範例行: 65/100      7.22G      1.957      2.795 ...
epoch_pattern = re.compile(r'^\s*\d+/\d+\s+\d+\.\d+G\s+')

print(f"正在處理: {input_file}...")

with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

cleaned_lines = []
last_epoch_data = ""
current_epoch = ""

for line in lines:
    # 處理含有 \r 的行（進度條通常長這樣），取最後一段
    sub_lines = line.split('\r')
    for sl in sub_lines:
        sl = sl.strip()
        if epoch_pattern.search(sl):
            # 提取當前 Epoch 序號 (例如 "65/100")
            epoch_id = sl.split()[0]
            
            if epoch_id != current_epoch:
                # 換 Epoch 了，把上一個 Epoch 的最後一行存起來
                if last_epoch_data:
                    cleaned_lines.append(last_epoch_data + '\n')
                current_epoch = epoch_id
            
            # 更新當前 Epoch 的最新數據
            last_epoch_data = sl

# 加入最後一個 Epoch 的數據
if last_epoch_data:
    cleaned_lines.append(last_epoch_data + '\n')

with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(cleaned_lines)

print(f"處理完成！乾淨的日誌已儲存至: {output_file}")
print(f"原始大小: {len(lines)} 行 -> 處理後: {len(cleaned_lines)} 行")