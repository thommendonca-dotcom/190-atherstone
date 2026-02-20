import re

html_path = r"E:\2026\AntiGravity\Website\190 Atherstone\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace .jpg and .png inside images/ dir to .webp
html = re.sub(r'(images/[^"\']*\.)(jpg|png)', r'\1webp', html, flags=re.IGNORECASE)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html to use webp")
