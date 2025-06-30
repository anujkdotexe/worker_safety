import os
import requests
from tqdm import tqdm

MODELS = {
    "yolov8n_ppe.pt": "https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt",
    "yolov8_pose.pt": "https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8s-pose.pt"
}

def download_file(url, filename):
    print(f"⬇️ Downloading {filename}...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        with open(filename, 'wb') as f, tqdm(
                desc=filename,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                size = f.write(chunk)
                bar.update(size)

os.makedirs("models", exist_ok=True)

print("🚀 Starting model downloads...")
for name, url in MODELS.items():
    dest = f"models/{name}"
    if not os.path.exists(dest):
        download_file(url, dest)
    else:
        print(f"✅ {name} already exists")

print("🔥 All models downloaded successfully!")
