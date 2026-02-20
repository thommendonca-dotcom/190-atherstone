import os
from PIL import Image, ImageEnhance

def enhance_outdoor(image_path, output_path):
    try:
        # Open and convert to standard RGB
        img = Image.open(image_path).convert('RGB')
        
        # 1. Brightness: Reduced from 1.08 to 1.02 to fix being "too bright"
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.02)
        
        # 2. Contrast: Reduced from 1.15 to 1.05 to soften the "harshness"
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.05)
        
        # 3. Saturation: Boosted from 1.25 to 1.35 specifically to make the grass greener
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.35)
        
        # 4. Sharpness: Pulled back slightly so the foliage isn't crunchy
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.1)
        
        # Save at high quality
        img.save(output_path, quality=95)
        return True
    except Exception as e:
        print(f"[!] Error processing {image_path}: {e}")
        return False

def enhance_indoor(image_path, output_path):
    try:
        # Open and convert to standard RGB
        img = Image.open(image_path).convert('RGB')
        
        # 1. Brightness: Reduced from 1.15 to 1.05 to lower harsh glare
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)
        
        # 2. Contrast: Reduced from 1.05 to 1.0 (flat) to keep shadows very soft and forgiving
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.00)
        
        # 3. Saturation: Slightly DESATURATE to remove yellow tungsten but not too aggressively (0.95)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.95)
        
        # 4. Sharpness: Pulled down from 1.3 to 1.1 so edges aren't overly crispy or harsh looking
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.1)
        
        img.save(output_path, quality=95)
        return True
    except Exception as e:
        print(f"[!] Error processing {image_path}: {e}")
        return False

def process_directory(input_dir, output_dir, process_func, label):
    if not os.path.exists(input_dir):
        print(f"Skipping {label} - Directory not found: {input_dir}")
        return
        
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    total = sum(1 for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')))
    
    if total == 0:
        print(f"No images found in {input_dir}")
        return
        
    print(f"Queueing {total} images from {label}...")
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            print(f"  -> Enhancing: {filename}")
            if process_func(input_path, output_path):
                count += 1
                
    print(f"Successfully styled {count}/{total} {label} images.\n")

def main():
    # Calculate paths realtive to the script location (assuming scripts/ folder)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    indoor_in = os.path.join(base_dir, 'images', 'raw', 'indoor')
    indoor_out = os.path.join(base_dir, 'images', 'enhanced', 'indoor')
    
    outdoor_in = os.path.join(base_dir, 'images', 'raw', 'outdoor')
    outdoor_out = os.path.join(base_dir, 'images', 'enhanced', 'outdoor')
    
    print("=========================================")
    print(" REAL ESTATE BATCH AUTO-ENHANCER STARTED ")
    print("=========================================\n")
    
    print("[1/2] Processing Indoor Photos (Focus: Bright, Airy, Neutralize Tungsten)")
    process_directory(indoor_in, indoor_out, enhance_indoor, "Indoor")
    
    print("[2/2] Processing Outdoor Photos (Focus: Punchy Contrast, Lush Greens, Sky)")
    process_directory(outdoor_in, outdoor_out, enhance_outdoor, "Outdoor")
    
    print("=========================================")
    print(" ALL BATCH PROCESSING COMPLETE! ")
    print(f" Output folders: \n - {indoor_out}\n - {outdoor_out}")
    print("=========================================")

if __name__ == "__main__":
    main()
