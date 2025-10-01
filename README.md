### SIXray Yolov10

This is a project using [SIXray](https://github.com/MeioJane/SIXray) dataset to build up security image recognition for some common danger goods: Gun, Knife, Wrench, Pliers, and Scissors.

This repo is targeted to compare the [YOLOv10](https://github.com/THU-MIG/yolov10?tab=readme-ov-file) method with the original and YOLOv4 method in the dimensions of detect precision, training parameters and also optimisers.

### Building Commands

- Build Environment with Conda

1. Install anaconda
2. Create environment

```
conda create -n yolov10 python==3.10 --strict-channel-priority -c conda-forge -y
conda activate yolov10
```

- Set VScode Terminal with conda

In settings.json

```
"terminal.integrated.profiles.windows": {
    "PowerShell": {
        "path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
    },
    "Anaconda Prompt": {
        "path": "C:\\Windows\\System32\\cmd.exe",
        "args": ["/K", "C:\\Users\\你的使用者名稱\\Anaconda3\\Scripts\\activate.bat"]
    }
},
"terminal.integrated.defaultProfile.windows": "Anaconda Prompt"

```

- Clone This Repo

```
git clone https://github.com/Annie04082020/SIXray_YOLOv10.git
```

- Clone YOLOv10 inside of this repo

```
cd SIXray_YOLOv10
git clone https://github.com/THU-MIG/yolov10.git
```

- Install requirements

```
cd yolov10
pip install -r requirements.txt
pip install -e .
cd ..
pip install -r requirements.txt
```

- Start Training

```
set KMP_DUPLICATE_LIB_OK=TRUE
python train.py
```

- If needed to install different cuda in env:

```
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Validation** 

```
python
>>> import torch
>>> print(torch.cuda.is_available())
# Expected Output：True
```

- Can't import ultralytics: (from [YOLOv10](https://github.com/THU-MIG/yolov10?tab=readme-ov-file))

```
cd yolov10
pip install -r requirements.txt
pip install -e .
```