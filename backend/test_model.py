import sys
sys.path.insert(0, '.')
from app.core.local_model_service import predict

with open('test_leaf.jpg', 'rb') as f:
    img_bytes = f.read()

result = predict(img_bytes)
if result:
    print("=== TAHLIL NATIJASI ===")
    print(f"O'simlik : {result['plant_name']}")
    print(f"Kasallik : {result['disease_name']}")
    print(f"Aniqlik  : {result['confidence']*100:.1f}%")
    print(f"Og'irlik : {result['severity']}")
    print(f"Sog'lom  : {result['is_healthy']}")
    print(f"Tavsif   : {result['description']}")
    print("Top-3 taxminlar:")
    for t in result['top3']:
        print(f"  {t['class']}: {t['prob']*100:.1f}%")
else:
    print("Xato: natija yo'q")
