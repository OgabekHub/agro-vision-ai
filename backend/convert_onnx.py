import sys
import os
import json
import torch
import torch.nn as nn
from torchvision import models

def main():
    print("Starting conversion...")
    
    # Paths
    backend_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else "."
    weights_dir = os.path.join(backend_dir, "models_weights")
    model_path = os.path.join(weights_dir, "plant_disease_model.pth")
    classes_path = os.path.join(weights_dir, "class_names.json")
    onnx_path = os.path.join(weights_dir, "plant_disease_model.onnx")
    
    if not os.path.exists(model_path):
        print(f"Error: PyTorch model not found at {model_path}")
        return
        
    if not os.path.exists(classes_path):
        print(f"Error: Classes JSON not found at {classes_path}")
        return

    # Load classes
    with open(classes_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    classes = data.get("classes", data)
    num_classes = len(classes)
    print(f"Loaded {num_classes} classes.")

    # Reconstruct the PyTorch model
    print("Reconstructing PyTorch model...")
    model = models.efficientnet_b2(weights=None)
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(model.classifier[1].in_features, num_classes),
    )

    # Load weights
    print("Loading PyTorch weights...")
    state = torch.load(model_path, map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    model.eval()

    # Create dummy input (1, 3, 224, 224)
    dummy_input = torch.randn(1, 3, 224, 224)

    # Export to ONNX
    print("Exporting model to ONNX...")
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        verbose=False,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )
    
    if os.path.exists(onnx_path):
        size_mb = os.path.getsize(onnx_path) / (1024 * 1024)
        print(f"✅ Success! ONNX model exported to {onnx_path} ({size_mb:.2f} MB)")
    else:
        print("❌ Export failed!")

if __name__ == "__main__":
    main()
