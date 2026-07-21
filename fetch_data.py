"""Tracked pipeline step 1: fetch the raw dataset from S3.

Run under `roar run` with the S3 proxy enabled (`roar proxy enable`). roar
injects AWS_ENDPOINT_URL so this boto3 GetObject flows through the proxy, which
records the resulting artifact with source_type=s3 and
source_url=s3://<bucket>/<key>. That provenance is what produces the AI-BOM
`downloadLocation` external reference on glaas.ai.
"""
import os

import boto3

BUCKET = os.environ["ROAR_DEMO_BUCKET"]
KEY = os.environ.get("ROAR_DEMO_KEY", "mnist_raw.csv")

os.makedirs("data", exist_ok=True)
boto3.client("s3").download_file(BUCKET, KEY, "data/mnist_raw.csv")
print(f"fetched s3://{BUCKET}/{KEY} -> data/mnist_raw.csv")
