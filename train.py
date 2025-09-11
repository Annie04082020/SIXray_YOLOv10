from ultralytics import YOLOv10  
import torch
model = YOLOv10.from_pretrained('jameslahm/yolov10n')
print(f"Model loaded successfully: {type(model)}")
print(torch.version.cuda)
print(torch.cuda.is_available())

# model.train(data='./../SIXray_YOLO/dataset.yaml', epochs=500, batch=256, imgsz=640)
model.train(data='./../SIXray_YOLO/dataset.yaml', epochs=100, batch=256, imgsz=640, device="cuda", amp=False)

model.save('./savemodel/yolov10n_sixray1.pt')

