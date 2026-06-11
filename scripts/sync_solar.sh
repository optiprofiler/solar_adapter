#!/usr/bin/env bash
set -euo pipefail

repo_url="https://github.com/bbopt/solar.git"
branch="master"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
upstream_dir="$root/upstream"
checkout_dir="$upstream_dir/solar"
manifest="$upstream_dir/manifest.json"

mkdir -p "$upstream_dir"
rm -rf "$checkout_dir"

git clone --depth 1 --branch "$branch" "$repo_url" "$checkout_dir"

commit="$(git -C "$checkout_dir" rev-parse HEAD)"
commit_date="$(git -C "$checkout_dir" show -s --format=%cI HEAD)"
subject="$(git -C "$checkout_dir" show -s --format=%s HEAD)"

python3 - "$manifest" "$repo_url" "$branch" "$commit" "$commit_date" "$subject" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

manifest, repo_url, branch, commit, commit_date, subject = sys.argv[1:]
payload = {
    "upstream": {
        "name": "bbopt/solar",
        "url": repo_url,
        "branch": branch,
        "commit": commit,
        "commit_date": commit_date,
        "commit_subject": subject,
        "license": "LGPL-2.1",
    },
    "synced_at": datetime.now(timezone.utc).isoformat(),
    "policy": {
        "strategy": "track-upstream-latest-with-recorded-commit",
        "vendor_source": False,
        "commit_upstream_checkout": False,
    },
}
Path(manifest).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY

echo "Synced SOLAR upstream commit: $commit"

