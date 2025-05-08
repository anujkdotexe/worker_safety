# Worker Safety Monitoring System 🦺📹

This project is a plug-and-play computer vision system designed for real-time industrial safety monitoring. It detects whether workers are wearing essential safety gear (helmets, vests, gloves) and identifies fall events using video feeds from any connected camera.

## 🚀 Features

- ✅ Helmet, vest, and gloves detection using YOLOv5
- ⚠️ Real-time fall detection using MediaPipe pose estimation
- 📹 Plug-and-play camera support
- 🧠 Easy model download and switching
- 🔧 Modular and configurable codebase

## 🗂️ Project Structure

```
worker_safety/
├── main.py                # Entry point for running the system
├── test_cam.py            # Simple camera test script
├── download_models.py     # Downloads required YOLOv5 models
├── requirements.txt       # Python dependencies
├── configs/               # Config files and model settings
├── models/                # Pretrained YOLOv5 model files
├── utils/                 # Utility scripts (drawing, detection, etc.)
├── venv/                  # Virtual environment (excluded from Git)
```

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourname/worker_safety.git
   cd worker_safety
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download model weights:
   ```bash
   python download_models.py
   ```

## ▶️ Usage

Run the main system:

```bash
python main.py
```

> Make sure a webcam or external camera is connected.

## 📦 Requirements

- Python 3.8+
- OpenCV
- torch
- yolov5
- mediapipe

(All included in `requirements.txt`)

## 📌 Notes

- The `models/` folder may be large and is excluded from version control.
- For new cameras, simply connect and re-run the script — it will auto-detect.

## 👨‍💼 Maintainer / Developer

This project was developed as a part of skill assessment and learning under mentor guidance.  
For suggestions or improvements, feel free to raise an issue or contact me.
