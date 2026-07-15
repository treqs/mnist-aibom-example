import hashlib
data=open("data/train.npz","rb").read()
sig=hashlib.sha256(data).hexdigest()[:16]
open("model.pkl","w").write(f"mnist-cnn weights (demo) trained_on={len(data)}B sig={sig}\n")
print("wrote model.pkl")
