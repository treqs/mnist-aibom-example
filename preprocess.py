import csv
rows=list(csv.reader(open("data/mnist_raw.csv")))[1:]
with open("data/train.npz","w") as f:      # .npz -> classified 'data'
    for r in rows: f.write(f"{int(r[0])/(255*784):.4f},{r[1]}\n")
print("wrote data/train.npz")
