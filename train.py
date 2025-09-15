# from ultralytics import YOLOv10  
# import torch
# model = YOLOv10.from_pretrained('jameslahm/yolov10n')
# print(f"Model loaded successfully: {type(model)}")
# print(torch.version.cuda)
# print(torch.cuda.is_available())

# # model.train(data='./../SIXray_YOLO/dataset.yaml', epochs=500, batch=256, imgsz=640)
# # model.train(data='./../SIXray_YOLO/dataset.yaml', epochs=100, batch=256, imgsz=640, device="cuda", amp=False)
# model.train(
#     data='./../SIXray_YOLO/dataset.yaml',
#     epochs=100,
#     batch=16,           # 先小一點
#     imgsz=640,
#     device="cuda",
#     amp=False,
#     workers=0,          # 關閉多線程 dataloader
#     verbose=True,
#     # cache=False
# )
# model.val(data='./../SIXray_YOLO/dataset.yaml', batch=16, imgsz=640, device="cuda", save_json=True)

# model.save('./savemodel/yolov10n_sixray1.pt')

from ultralytics import YOLOv10
import torch

model = YOLOv10.from_pretrained('jameslahm/yolov10n')
print(f"Model loaded successfully: {type(model)}")
print(torch.version.cuda)
print(torch.cuda.is_available())

dataset_path = r"D:\SIXray_YOLO\dataset.yaml"  # 改成 Windows 絕對路徑

model.train(
    data=dataset_path,
    epochs=10,
    batch=20,           # 先小一點
    imgsz=480,
    device="cuda",
    amp=False,
    workers=0,          # 關閉多線程 dataloader
    verbose=True,
    cache=True
)

model.val(
    data=dataset_path,
    batch=20,
    imgsz=480,
    device="cuda",
    save_json=True
)

model.save(r"D:\SIXray_code\savemodel\yolov10n_sixray1.pt")  # 改成絕對路徑
