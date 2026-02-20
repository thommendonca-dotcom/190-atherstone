import os
import json
import base64
import requests

def get_api_key():
    env_path = r"E:\2026\AntiGravity\Image GEN APP\.env"
    with open(env_path, "r") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                return line.strip().split("=")[1].strip("'\"")
    return None

def main():
    api_key = get_api_key()
    if not api_key:
        print("Failed to find api key")
        return
        
    image_dir = r"E:\2026\AntiGravity\Website\190 Atherstone\images\screenshot"
    images = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not images:
        print("No images found in screenshots.")
        return
        
    contents = []
    
    for img_file in images:
        img_path = os.path.join(image_dir, img_file)
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        contents.append({
            "inlineData": {
                "mimeType": "image/jpeg",
                "data": encoded_string
            }
        })
        
    contents.append({
        "text": "These are screenshots of the UI the user wants their real estate website to look like. Please provide a highly detailed design system analysis of this UI so I can recreate it in HTML/CSS. Specifically:\n1. Exact Color Palette (find hex codes or close approximations for background, accent, text, etc).\n2. Typography (font families, sizing for headings and body).\n3. Layout patterns (hero section layout, navigation, grid styles, card designs).\n4. Specific UI elements like buttons, overlays, borders, shadows, and any unique visual motifs.\nGive me a highly detailed list so I can rewrite my HTML/CSS to exactly match it."
    })
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": contents}]
    }
    
    print("Calling Gemini API...")
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 200:
        res_json = resp.json()
        with open("ui_analysis.md", "w", encoding="utf-8") as f:
            f.write(res_json["candidates"][0]["content"]["parts"][0]["text"])
        print("\n=== AI Design Analysis Saved to ui_analysis.md ===\n")
    else:
        print(f"Error {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    main()
