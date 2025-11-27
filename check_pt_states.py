import torch
import ultralytics

# 1. 允許 YOLOv10DetectionModel 類別被 unpickle
from ultralytics.nn.tasks import YOLOv10DetectionModel
torch.serialization.add_safe_globals([YOLOv10DetectionModel])

# 2. 允許 ultralytics.nn.modules 裡面的所有 module
import inspect
import ultralytics.nn.modules as um

module_classes = [obj for name, obj in inspect.getmembers(um) if inspect.isclass(obj)]
torch.serialization.add_safe_globals(module_classes)

# 3. 允許常見的 torch modules（若你上次用過，也可加上）
import torch.nn as nn

torch_classes = [
    nn.Sequential,
    nn.ModuleList,
    nn.Identity,
    nn.Conv2d,
    nn.BatchNorm2d,
    nn.ReLU,
    nn.SiLU,
    nn.MaxPool2d,
]
torch.serialization.add_safe_globals(torch_classes)

# 4. 現在安全地載入 last.pt
ckpt = torch.load("runs/detect/train28/weights/last.pt", weights_only=False)

print("Checkpoint keys:", ckpt.keys())

if "optimizer" in ckpt:
    print("Optimizer state FOUND.")
else:
    print("Optimizer state NOT found.")
