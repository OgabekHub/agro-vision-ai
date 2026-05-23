"""
AgroVision AI - Kaggle Dataset Downloader and Merger
This script downloads multiple agricultural datasets from Kaggle using the Kaggle API,
extracts them, and structures them into a single unified dataset folder for training.

Before running:
1. Install kaggle package: pip install kaggle
2. Download kaggle.json from Kaggle (Settings -> Create New Token)
3. Place kaggle.json in ~/.kaggle/ (Linux/Mac) or C:\\Users\\<Username>\\.kaggle\\ (Windows)
   OR set environment variables:
   import os
   os.environ['KAGGLE_USERNAME'] = "your_username"
   os.environ['KAGGLE_KEY'] = "your_api_key"
"""

import os
import shutil
import zipfile
import glob
from pathlib import Path

# Configuration
DATASETS = {
    # format: 'local_temp_folder': 'kaggle_dataset_slug'
    'plantvillage': 'vipoooool/new-plant-diseases-dataset',
    'cotton': 'janmejaybhatt/cotton-disease-dataset',
    'wheat': 'noumanshah/wheat-rust-dataset-stripe-rust-and-leaf-rust',
    'rice': 'vbookshelf/rice-leaf-diseases-dataset',
    'citrus': 'gauravduttakiit/citrus-leaf-disease-image-dataset'
}

TEMP_DIR = Path("./temp_kaggle_data")
OUTPUT_DIR = Path("./merged_dataset")

def setup_kaggle_api():
    """Verify Kaggle API credentials are set up."""
    # Check environment variables first
    if os.environ.get('KAGGLE_USERNAME') and os.environ.get('KAGGLE_KEY'):
        print("[OK] Kaggle API credentials found in environment variables.")
        return True
    
    # Check KAGGLE_API_TOKEN env var
    if os.environ.get('KAGGLE_API_TOKEN'):
        print("[OK] Kaggle API token found in environment variable.")
        return True
        
    # Check local home directory for new-style access_token or legacy kaggle.json
    home = Path.home()
    access_token = home / ".kaggle" / "access_token"
    kaggle_config = home / ".kaggle" / "kaggle.json"
    if access_token.exists():
        print(f"[OK] Kaggle API access_token found at {access_token}")
        return True
    if kaggle_config.exists():
        print(f"[OK] Kaggle API configuration found at {kaggle_config}")
        return True
        
    print("[ERROR] Kaggle API configuration NOT found!")
    print("Please follow instructions in the header comments to configure your Kaggle token.")
    return False

def download_dataset(slug, temp_folder):
    """Download a dataset using Kaggle API."""
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    
    target_path = TEMP_DIR / temp_folder
    target_path.mkdir(parents=True, exist_ok=True)
    
    print(f"[DOWNLOAD] Downloading dataset '{slug}' into {target_path}...")
    api.dataset_download_files(slug, path=str(target_path), unzip=True)
    print(f"[OK] Successfully downloaded and extracted '{slug}'")

def copy_images(src_dir, dst_class_name):
    """Copy all images from src_dir to OUTPUT_DIR/dst_class_name."""
    dst_dir = OUTPUT_DIR / dst_class_name
    dst_dir.mkdir(parents=True, exist_ok=True)
    
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    files_copied = 0
    
    for ext in image_extensions:
        for file_path in glob.glob(os.path.join(src_dir, ext)):
            # Create a unique name to prevent collisions
            filename = os.path.basename(file_path)
            # Ensure the filename is unique using the source directory hash or counter
            unique_filename = f"{files_copied}_{filename}"
            shutil.copy2(file_path, dst_dir / unique_filename)
            files_copied += 1
            
    return files_copied

def process_plantvillage():
    """Organize PlantVillage dataset into merged_dataset."""
    print("[PROCESS] Processing PlantVillage...")
    # PlantVillage usually has a train/valid subfolder
    pv_train_dir = TEMP_DIR / "plantvillage" / "New Plant Diseases Dataset(Augmented)" / "New Plant Diseases Dataset(Augmented)" / "train"
    if not pv_train_dir.exists():
        # Fallback search
        found = list(TEMP_DIR.glob("**/train"))
        if found:
            pv_train_dir = found[0]
        else:
            print("[WARN] Could not find PlantVillage train folder")
            return
            
    total_files = 0
    for class_folder in os.listdir(pv_train_dir):
        src_class_path = pv_train_dir / class_folder
        if src_class_path.is_dir():
            # Standardize naming: e.g. "Tomato___Bacterial_spot" -> "Tomato__bacterial_spot"
            clean_class_name = class_folder.replace("___", "__").replace(" ", "_").lower()
            # Capitalize the plant name part
            parts = clean_class_name.split("__")
            parts[0] = parts[0].capitalize()
            clean_class_name = "__".join(parts)
            
            copied = copy_images(src_class_path, clean_class_name)
            total_files += copied
            
    print(f"[OK] PlantVillage complete: copied {total_files} images.")

def process_cotton():
    """Organize Cotton dataset into merged_dataset."""
    print("[PROCESS] Processing Cotton Dataset...")
    # janmejaybhatt/cotton-disease-dataset has folders like:
    # 'Cotton Disease/train' containing 'diseased cotton leaf', 'diseased cotton plant', 'fresh cotton leaf', 'fresh cotton plant'
    cotton_root = TEMP_DIR / "cotton"
    train_dir = list(cotton_root.glob("**/train"))
    if not train_dir:
        train_dir = list(cotton_root.glob("**/Cotton Disease"))
        
    if not train_dir:
        print("[WARN] Could not find Cotton train folder")
        return
        
    src_dir = train_dir[0]
    total_files = 0
    
    mapping = {
        'diseased cotton leaf': 'Cotton__diseased_leaf',
        'diseased cotton plant': 'Cotton__diseased_plant',
        'fresh cotton leaf': 'Cotton__healthy_leaf',
        'fresh cotton plant': 'Cotton__healthy_plant'
    }
    
    for folder, clean_name in mapping.items():
        folder_path = src_dir / folder
        if folder_path.exists():
            copied = copy_images(folder_path, clean_name)
            total_files += copied
            
    print(f"[OK] Cotton complete: copied {total_files} images.")

def process_wheat():
    """Organize Wheat dataset into merged_dataset."""
    print("[PROCESS] Processing Wheat Dataset...")
    # noumanshah/wheat-rust-dataset-stripe-rust-and-leaf-rust has folders like:
    # 'Wheat Rust Dataset' containing 'Leaf Rust', 'Stripe Rust', 'Healthy'
    wheat_root = TEMP_DIR / "wheat"
    total_files = 0
    
    mapping = {
        'Leaf Rust': 'Wheat__leaf_rust',
        'Stripe Rust': 'Wheat__stripe_rust',
        'Healthy': 'Wheat__healthy'
    }
    
    for folder, clean_name in mapping.items():
        # Search recursively for these folders
        found = list(wheat_root.glob(f"**/{folder}"))
        if found:
            copied = copy_images(found[0], clean_name)
            total_files += copied
            
    print(f"[OK] Wheat complete: copied {total_files} images.")

def process_rice():
    """Organize Rice dataset into merged_dataset."""
    print("[PROCESS] Processing Rice Dataset...")
    # vbookshelf/rice-leaf-diseases-dataset has:
    # 'rice_leaf_diseases' containing 'Bacterial leaf blight', 'Brown spot', 'Leaf smut'
    rice_root = TEMP_DIR / "rice"
    total_files = 0
    
    mapping = {
        'Bacterial leaf blight': 'Rice__bacterial_blight',
        'Brown spot': 'Rice__brown_spot',
        'Leaf smut': 'Rice__leaf_smut'
    }
    
    for folder, clean_name in mapping.items():
        found = list(rice_root.glob(f"**/{folder}"))
        if found:
            copied = copy_images(found[0], clean_name)
            total_files += copied
            
    print(f"[OK] Rice complete: copied {total_files} images.")

def process_citrus():
    """Organize Citrus dataset into merged_dataset."""
    print("[PROCESS] Processing Citrus Dataset...")
    # gauravduttakiit/citrus-leaf-disease-image-dataset has folders like:
    # 'Citrus' containing 'Black Spot', 'Canker', 'Greening', 'Healthy'
    citrus_root = TEMP_DIR / "citrus"
    total_files = 0
    
    mapping = {
        'Black Spot': 'Citrus__black_spot',
        'Canker': 'Citrus__canker',
        'Greening': 'Citrus__greening',
        'Healthy': 'Citrus__healthy'
    }
    
    for folder, clean_name in mapping.items():
        found = list(citrus_root.glob(f"**/{folder}"))
        if found:
            copied = copy_images(found[0], clean_name)
            total_files += copied
            
    print(f"[OK] Citrus complete: copied {total_files} images.")

def main():
    if not setup_kaggle_api():
        return
        
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Download all datasets
    for folder, slug in DATASETS.items():
        if not (TEMP_DIR / folder).exists():
            try:
                download_dataset(slug, folder)
            except Exception as e:
                print(f"[ERROR] Failed to download {slug}: {e}")
        else:
            print(f"[INFO] Dataset '{slug}' already exists in temp dir, skipping download.")
            
    # 2. Process and merge
    process_plantvillage()
    process_cotton()
    process_wheat()
    process_rice()
    process_citrus()
    
    # Print summary
    class_dirs = [d for d in OUTPUT_DIR.iterdir() if d.is_dir()]
    print("\n==========================================")
    print("MERGED DATASET SUMMARY")
    print("==========================================")
    print(f"Total Categories: {len(class_dirs)}")
    
    total_images = 0
    for class_dir in sorted(class_dirs):
        num_imgs = len(list(class_dir.glob("*")))
        total_images += num_imgs
        print(f"  - {class_dir.name}: {num_imgs} images")
        
    print("------------------------------------------")
    print(f"Total Merged Images: {total_images}")
    print("==========================================")
    print("Ready for training! Run train_mega_dataset.py now.")
    
    # Optionally clean up temp data to save disk space
    # shutil.rmtree(TEMP_DIR)
    
if __name__ == "__main__":
    main()
