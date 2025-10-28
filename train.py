# import ultralytics
from ultralytics import YOLOv10
import torch
# import inspect
# import ultralytics.nn.modules
# import torch.nn as nn
# torch_classes = [
#     nn.Sequential,
#     nn.ModuleList,
#     nn.Identity,
#     nn.Conv2d,
#     nn.BatchNorm2d,
#     nn.ReLU,
#     nn.SiLU,
#     nn.MaxPool2d
# ]
# module_classes = [obj for name, obj in inspect.getmembers(ultralytics.nn.modules) if inspect.isclass(obj)]
# torch.serialization.add_safe_globals(module_classes)
# torch.serialization.add_safe_globals(torch_classes)
# torch.serialization.add_safe_globals([ultralytics.nn.tasks.YOLOv10DetectionModel])
# print("✅ Safe globals:", torch.serialization.get_safe_globals())

def main():
    dataset_path = "./../SIXray_YOLO/dataset.yaml" 
    # model = YOLOv10.from_pretrained('jameslahm/yolov10n')
    model = YOLOv10('savemodel/best-19.pt')  # 改成絕對路徑   
    
    print(f"Model loaded successfully: {type(model)}")
    print(torch.version.cuda)
    print(torch.cuda.is_available())
    model.train(
        data=dataset_path,
        epochs=100,
        batch=256,           
        imgsz=256,
        device="cuda",
        amp=True,
        workers=8,        # 開啟多線程 dataloader
        verbose=True,
        # cache="disk"
    )
    model.save("./SIXray_YOLOv10/savemodel/yolov10n_sixray3.pt")  # 改成絕對路徑


if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()  # 可加可不加（主要針對 PyInstaller 打包）
    main()