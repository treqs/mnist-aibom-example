#!/usr/bin/env bash
# Reproduce the pipeline and register it to GLaaS with a perfect (100/100) AI-BOM.
#
# Prerequisites:
#   - valid AWS creds in the environment (to read the S3 dataset via the proxy)
#   - a GLaaS login:            roar auth login
#   - repo scope set to an ORG project (supplies BOM supplier/author):
#                               roar scope use <org>/<project>
#   - the dataset seeded once:  ROAR_DEMO_BUCKET=... python3 bootstrap_s3.py
set -euo pipefail

ROAR="${ROAR:-roar}"
export ROAR_DEMO_BUCKET="${ROAR_DEMO_BUCKET:-treqs-mnist-aibom-demo}"
export ROAR_DEMO_KEY="${ROAR_DEMO_KEY:-mnist_raw.csv}"

# 1. Enable the S3 proxy so the dataset fetch is provenance-tracked (source_type=s3).
"$ROAR" proxy enable

# 1a. Keep AWS creds out of the lineage: boto3 reads ~/.aws/* during client init,
#     which roar would otherwise capture as a tracked input. Filter that path so
#     the published BOM never references credentials.
python3 - <<'PY'
import re
p = ".roar/config.toml"
s = open(p).read()
import os
aws = os.path.expanduser("~/.aws")
if "ignore_paths" not in s:
    if "[filters]" in s:
        s = re.sub(r"\[filters\]", f'[filters]\nignore_paths = ["{aws}"]', s, count=1)
    else:
        s += f'\n[filters]\nignore_paths = ["{aws}"]\n'
    open(p, "w").write(s)
    print("filters.ignore_paths -> ~/.aws")
PY

# 2. Tracked, chained pipeline: fetch(s3) -> preprocess -> train.
"$ROAR" run -- python3 fetch_data.py
"$ROAR" run -- python3 preprocess.py
"$ROAR" run -- python3 train.py

# 3. Attach the BOM-bearing labels to the model artifact.
"$ROAR" label set artifact model.pkl \
  description="MNIST CNN digit classifier — TReqs AI-BOM demo" \
  license.id=MIT \
  license.name="MIT License" \
  documentation.url="https://github.com/treqs/mnist-aibom-example/blob/main/MODEL_CARD.md" \
  model.name=mnist-cnn \
  model.version=1.0

# 4. Register the whole session under the active ORG scope.
"$ROAR" register -y

echo "Done. Open the session's /audit on glaas.ai to see the 100/100 AI-BOM."
