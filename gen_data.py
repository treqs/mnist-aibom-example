import csv, random
random.seed(0)
with open("data/mnist_raw.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["pixel_sum","label"])
    for _ in range(500): w.writerow([random.randint(0,255*784), random.randint(0,9)])
print("wrote data/mnist_raw.csv")
