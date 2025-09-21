### SIXray Yolov10

This is a project using [SIXray](https://github.com/MeioJane/SIXray) dataset to build up security image recognition for some common danger goods: Gun, Knife, Wrench, Pliers, and Scissors.

This repo is targeted to compare the YOLOv10 method with the original and YOLOv4 method in the dimensions of detect precision, training parameters and also optimisers.

### Building Commands

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
