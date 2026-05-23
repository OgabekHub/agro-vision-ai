"""
AgroVision AI - Mega Dataset Training Script
This script trains an EfficientNet-B2 classifier on the merged agricultural dataset.
Supports both local execution (on `./merged_dataset` folder) and Kaggle environment.

Features:
- Fixes PyTorch dataset split transforms bug (applies proper validation transforms to the val split)
- Supports training on 100+ classes dynamically
- Mixed precision training (AMP) for faster training on GPUs
"""

import os
import json
import time
import copy
from pathlib import Path
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split, Dataset
from torchvision import datasets, transforms, models
from torch.cuda.amp import GradScaler, autocast
from PIL import Image

# ==========================================
# CONFIGURATION
# ==========================================
# Default path points to `./merged_dataset` created by `download_and_merge.py`.
# Change this if running in Kaggle and using Kaggle input datasets directly.
DATA_DIR = "./merged_dataset" 

IMG_SIZE = 224
BATCH_SIZE = 64
EPOCHS = 15
LEARNING_RATE = 0.001
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Using device: {DEVICE}")

# ==========================================
# DATASET SUBSET TRANSFORM HELPER
# ==========================================
class TransformedSubset(Dataset):
    """
    Wraps an ImageFolder dataset and its subset indices to apply 
    different transforms for train and validation splits.
    """
    def __init__(self, image_folder_dataset, indices, transform=None):
        self.dataset = image_folder_dataset
        self.indices = indices
        self.transform = transform

    def __getitem__(self, idx):
        # Retrieve the original image path and label directly from samples list
        img_path, label = self.dataset.samples[self.indices[idx]]
        img = self.dataset.loader(img_path)
        if self.transform:
            img = self.transform(img)
        return img, label

    def __len__(self):
        return len(self.indices)

# ==========================================
# DATA PREPARATION & AUGMENTATION
# ==========================================
train_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomCrop(IMG_SIZE),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(20),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"Dataset directory '{DATA_DIR}' not found. Please run download_and_merge.py first.")

# Load full dataset (no transform at root level, transforms applied in TransformedSubset)
base_dataset = datasets.ImageFolder(DATA_DIR)
class_names = base_dataset.classes
num_classes = len(class_names)
print(f"Found {num_classes} classes and {len(base_dataset)} total images.")

# Split indices (80% Train, 20% Validation)
dataset_size = len(base_dataset)
train_len = int(0.8 * dataset_size)
val_len = dataset_size - train_len

# Split indices randomly
train_indices, val_indices = random_split(range(dataset_size), [train_len, val_len])

# Create subsets with correct transforms
train_dataset = TransformedSubset(base_dataset, train_indices, transform=train_transforms)
val_dataset = TransformedSubset(base_dataset, val_indices, transform=val_transforms)

# Dataloaders
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, pin_memory=True)

# ==========================================
# MODEL SETUP (EfficientNet-B2)
# ==========================================
print(f"Setting up EfficientNet-B2 classifier with {num_classes} classes...")
model = models.efficientnet_b2(weights=models.EfficientNet_B2_Weights.IMAGENET1K_V1)

# Replace classifier for our number of classes
model.classifier = nn.Sequential(
    nn.Dropout(p=0.3, inplace=True),
    nn.Linear(model.classifier[1].in_features, num_classes)
)

model = model.to(DEVICE)
criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-4)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)
scaler = GradScaler()

# ==========================================
# TRAINING LOOP
# ==========================================
best_acc = 0.0
best_model_wts = copy.deepcopy(model.state_dict())

print("Starting training...")
for epoch in range(EPOCHS):
    start_time = time.time()
    
    # --- Train Phase ---
    model.train()
    running_loss = 0.0
    running_corrects = 0

    for inputs, labels in train_loader:
        inputs = inputs.to(DEVICE, non_blocking=True)
        labels = labels.to(DEVICE, non_blocking=True)

        optimizer.zero_grad()

        with autocast():
            outputs = model(inputs)
            loss = criterion(outputs, labels)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        _, preds = torch.max(outputs, 1)
        running_loss += loss.item() * inputs.size(0)
        running_corrects += torch.sum(preds == labels.data)

    train_loss = running_loss / train_len
    train_acc = running_corrects.double() / train_len

    # --- Val Phase ---
    model.eval()
    val_loss = 0.0
    val_corrects = 0

    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs = inputs.to(DEVICE, non_blocking=True)
            labels = labels.to(DEVICE, non_blocking=True)

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            _, preds = torch.max(outputs, 1)
            val_loss += loss.item() * inputs.size(0)
            val_corrects += torch.sum(preds == labels.data)

    val_loss = val_loss / val_len
    val_acc = val_corrects.double() / val_len

    scheduler.step()

    if val_acc > best_acc:
        best_acc = val_acc
        best_model_wts = copy.deepcopy(model.state_dict())

    time_elapsed = time.time() - start_time
    print(f"Epoch {epoch+1}/{EPOCHS} [{time_elapsed:.0f}s] - "
          f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} | "
          f"Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}")

print(f"\nTraining Complete. Best Val Accuracy: {best_acc:.4f}")

# ==========================================
# EXPORT MODEL & CLASSES
# ==========================================
# Load best weights
model.load_state_dict(best_model_wts)

# Save model weights
torch.save(model.state_dict(), "plant_disease_model.pth")
print("Saved model weights to plant_disease_model.pth")

# Save class names JSON
output_data = {
    "num_classes": num_classes,
    "classes": class_names,
    "model": "efficientnet_b2",
    "img_size": IMG_SIZE,
    "best_val_acc": float(best_acc)
}
with open("class_names.json", "w") as f:
    json.dump(output_data, f, indent=4)
print("Saved class list to class_names.json")

print("\nDONE! You can now copy `plant_disease_model.pth` and `class_names.json` to the backend models_weights folder.")
print("Then, run convert_onnx.py to generate the ONNX format model.")
