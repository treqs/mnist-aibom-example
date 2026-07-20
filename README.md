# mnist-aibom-example — perfect AI-BOM score demo

A multi-step, git-tracked, labeled **roar** pipeline engineered to score
**100/100** on the glaas.ai AI-BOM audit. See `~/aibom-perfect-recipe.md` for the
field-by-field map.

## Why S3?

The AI-BOM's `downloadLocation` field is only populated when an input artifact
carries a real `source_url`. roar writes that **only for S3 objects fetched
through its proxy** (`source_type=s3`) — plain `https`/`gs` downloads and
`roar get` do *not* populate it. So the dataset is hosted in S3 and pulled via
the roar proxy; that single step is what turns a 97.5 into a 100.

## Reproduce

Prerequisites: `roar` installed, valid AWS creds in the environment, a GLaaS
login, and this repo's scope pointed at an **organization** project (org scope
supplies the BOM's supplier/author).

```bash
# 0. one-time: seed the S3 bucket with the raw dataset
export ROAR_DEMO_BUCKET=treqs-mnist-aibom-demo
python3 bootstrap_s3.py

# 1. log in and point this repo at your org project scope
roar auth login
roar scope use <org>/<project>

# 2. run the tracked pipeline + label + register (see run_all.sh)
./run_all.sh
```

Then open the registered session's `…/dag/<session>/audit` on glaas.ai — every
one of the 28 fields is present (Advanced profile, 100/100).

## Pipeline

| Step | Script | Output | AI-BOM contribution |
|------|--------|--------|---------------------|
| fetch | `fetch_data.py` | `data/mnist_raw.csv` | source-tracked S3 input → `downloadLocation` |
| preprocess | `preprocess.py` | `data/train.npz` | chained job → `dependencies`, task I/O |
| train | `train.py` | `model.pkl` | model component + hashes |

Labels on `model.pkl` (`description`, `license.id`/`license.name`,
`documentation.url`, `model.*`) supply the component description, licenses,
documentation URL, and component properties. Git remote + commit supply
`gitCommit`/`gitRepo`/`gitBranch` and `vcsUrl`. Registering under an org scope
supplies `supplier`/`author`.
