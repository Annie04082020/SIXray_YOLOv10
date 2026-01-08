import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 中文字體 (Windows優先SimHei)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 🔥 **關鍵修復：自動清理欄位空格**
df = pd.read_csv('training_record/csvs/train33.results.csv')
df.columns = df.columns.str.strip()  # ← **這行救命！**
df['epoch'] = df['epoch'].astype(int)  # Epoch轉整數

print("✅ 欄位清理完成！形狀:", df.shape)
print("📊 最佳 mAP50-95:", df['metrics/mAP50-95(B)'].max())

# 總Loss (OM版：標準指標)
df['train_total_loss'] = df['train/box_om'] + df['train/cls_om'] + df['train/dfl_om']
df['val_total_loss'] = df['val/box_om'] + df['val/cls_om'] + df['val/dfl_om']

# 4子圖：Loss收斂 + 分解 + mAP + LR
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle(' YOLOv10n SIXray訓練曲線 (100 Epochs) | 最終mAP@0.5:0.95 = {:.4f}'.format(
    df['metrics/mAP50-95(B)'].max()), fontsize=18, fontweight='bold')

# 1️⃣ **Total Loss收斂** (Train藍/Val紅 → 無過擬合✅)
axes[0,0].plot(df['epoch'], df['train_total_loss'], 'b-', lw=3, label='Train Loss')
axes[0,0].plot(df['epoch'], df['val_total_loss'], 'r-', lw=3, label='Val Loss')
axes[0,0].set_title(' Total Loss (Box+Cls+Dfl)')
axes[0,0].set_xlabel('Epoch'); axes[0,0].set_ylabel('Loss')
axes[0,0].legend(); axes[0,0].grid(alpha=0.3); axes[0,0].set_ylim(0, None)

# 2️⃣ **Val Loss分解** (Cls主導 → 調cls=1.0優化)
for col, c in zip(['val/box_om', 'val/cls_om', 'val/dfl_om'], ['g', 'orange', 'purple']):
    axes[0,1].plot(df['epoch'], df[col], c, lw=2, label=col.split('/')[-1])
axes[0,1].set_title(' Val Loss 分解')
axes[0,1].legend(); axes[0,1].grid(alpha=0.3)

# 3️⃣ **mAP曲線** (黑粗線=最終指標)
for col, c, lbl in zip(['metrics/precision(B)', 'metrics/recall(B)', 'metrics/mAP50(B)', 'metrics/mAP50-95(B)'],
                       ['c', 'm', 'gold', 'k'], ['Precision', 'Recall', 'mAP@0.5', 'mAP@0.5:0.95']):
    lw = 4 if col == 'metrics/mAP50-95(B)' else 2.5
    axes[1,0].plot(df['epoch'], df[col], c, lw=lw, label=lbl)
axes[1,0].set_title(' 檢測精度 (SOTA: 0.2167)')
axes[1,0].set_ylim(0,1); axes[1,0].legend(); axes[1,0].grid(alpha=0.3)

# 4️⃣ **學習率** (Cosine衰減完美)
axes[1,1].plot(df['epoch'], df['lr/pg0'], 'brown', lw=2)
axes[1,1].set_title(' LR Schedule (Log)')
axes[1,1].set_yscale('log'); axes[1,1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('training_record/figure/yolov10s_analysis_4th.png', dpi=300, bbox_inches='tight')
plt.show()

# 🏆 **最佳Epoch自動印出**
best_idx = df['metrics/mAP50-95(B)'].idxmax()
print(f"\n🏅 **最佳 Epoch {best_idx}**")
print(f"   mAP@0.5:0.95: {df.loc[best_idx, 'metrics/mAP50-95(B)']:.4f}")
print(f"   mAP@0.5    : {df.loc[best_idx, 'metrics/mAP50(B)']:.4f}")
print(f"   P/R        : {df.loc[best_idx, 'metrics/precision(B)']:.4f} / {df.loc[best_idx, 'metrics/recall(B)']:.4f}")
print(f"   Val Loss   : {df.loc[best_idx, 'val_total_loss']:.4f}")