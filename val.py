from ultralytics import YOLOv10
import torch
def main():
    model = YOLOv10(r"D:\SIXray_code\savemodel\best.pt")
    print(f"Model loaded successfully: {type(model)}")
    print(torch.version.cuda)
    print(torch.cuda.is_available())

    dataset_path = r"D:\SIXray_YOLO\dataset.yaml"  # 改成 Windows 絕對路徑

    results = model.val(
        data=dataset_path,
        batch=16,
        imgsz=320,
        device="cuda",
        save_json=True
    )
    print(results)
    model.save(r"D:\SIXray_code\savemodel\yolov10n_sixray1.pt")  # 改成絕對路徑

if __name__ == "__main__":
    main()