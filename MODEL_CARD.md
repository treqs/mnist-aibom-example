# Model Card — mnist-cnn (TReqs AI-BOM demo)

> A tiny, synthetic model used to demonstrate a **complete, 100/100 AI-BOM**
> generated automatically by roar + GLaaS. It is not intended for real use.

## Model details
- **Name:** mnist-cnn
- **Version:** 1.0
- **Type:** machine-learning-model
- **License:** MIT
- **Owner / supplier:** TReqs (registered under the `treqs` organization scope)
- **Source repo:** https://github.com/treqs/mnist-aibom-example

## Intended use
Demonstration only. The pipeline synthesizes a small MNIST-style dataset, so the
"model" carries no real predictive value — the point is the **provenance**, not
the accuracy.

## Training data
- **Dataset:** synthetic MNIST-style records (`pixel_sum`, `label`), 500 rows.
- **Source of record:** pulled from S3 through the roar proxy, so the AI-BOM
  captures a real `downloadLocation` (`s3://<bucket>/mnist_raw.csv`).

## Lineage / provenance
Captured automatically by roar across three chained steps:
1. `fetch_data.py` — download the raw dataset from S3 (tracked input).
2. `preprocess.py` — normalize to `data/train.npz`.
3. `train.py` — produce `model.pkl`.

Every input, output, hash, dependency, git commit, and the S3 download location
is recorded with no code changes — then GLaaS renders it as a CycloneDX AI-BOM.

## AI-BOM completeness
All 28 fields across the five categories (required, metadata, component,
lineage, external references) are present → **100 / 100 (Advanced profile)**.
See `README.md` and `~/aibom-perfect-recipe.md` for the field-by-field map.
