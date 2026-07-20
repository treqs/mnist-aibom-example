"""One-time setup: synthesize the raw MNIST-style dataset and upload it to S3.

This is NOT part of the tracked pipeline — it just seeds the bucket that
`fetch_data.py` later pulls from (through the roar S3 proxy) so the dataset
becomes a provenance-tracked input (source_type=s3, source_url=s3://...),
which is what earns the AI-BOM `downloadLocation` field.

Run once with valid AWS creds:
    ROAR_DEMO_BUCKET=treqs-mnist-aibom-demo python3 bootstrap_s3.py
"""
import csv
import os
import random

import boto3

BUCKET = os.environ["ROAR_DEMO_BUCKET"]
KEY = os.environ.get("ROAR_DEMO_KEY", "mnist_raw.csv")
REGION = os.environ.get("AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-2"))

# Synthesize a small, deterministic raw dataset.
os.makedirs("data", exist_ok=True)
random.seed(0)
with open("data/mnist_raw.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["pixel_sum", "label"])
    for _ in range(500):
        w.writerow([random.randint(0, 255 * 784), random.randint(0, 9)])

# Create the bucket (idempotent) and upload the raw dataset.
s3 = boto3.client("s3", region_name=REGION)
try:
    if REGION == "us-east-1":
        s3.create_bucket(Bucket=BUCKET)
    else:
        s3.create_bucket(
            Bucket=BUCKET,
            CreateBucketConfiguration={"LocationConstraint": REGION},
        )
    print(f"created bucket {BUCKET} in {REGION}")
except s3.exceptions.BucketAlreadyOwnedByYou:
    print(f"bucket {BUCKET} already exists (owned by you)")

s3.upload_file("data/mnist_raw.csv", BUCKET, KEY)
print(f"seeded s3://{BUCKET}/{KEY}")
