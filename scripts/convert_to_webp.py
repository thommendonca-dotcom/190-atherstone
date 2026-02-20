import os
from PIL import Image

image_dirs = [
    r"E:\2026\AntiGravity\Website\190 Atherstone\images\enhanced\outdoor",
    r"E:\2026\AntiGravity\Website\190 Atherstone\images\enhanced\indoor",
    r"E:\2026\AntiGravity\Website\190 Atherstone\images\final"
]

for d in image_dirs:
    if not os.path.exists(d):
        continue
    for f in os.listdir(d):
        if f.lower().endswith(('.jpg', '.png', '.jpeg')):
            full_path = os.path.join(d, f)
            name, ext = os.path.splitext(f)
            webp_path = os.path.join(d, name + '.webp')
            try:
                img = Image.open(full_path)
                img.save(webp_path, 'WEBP')
                print(f"Converted {f} to {name}.webp")
            except Exception as e:
                print(f"Failed to convert {f}: {e}")
