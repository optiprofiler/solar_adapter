#!/usr/bin/env bash
set -euo pipefail

repo_url="https://github.com/bbopt/solar.git"
branch="master"
sync_method="${SOLAR_SYNC_METHOD:-auto}"
git_timeout_sec="${SOLAR_GIT_TIMEOUT_SEC:-180}"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
upstream_dir="$root/upstream"
checkout_dir="$upstream_dir/solar"
manifest="$upstream_dir/manifest.json"

mkdir -p "$upstream_dir"
rm -rf "$checkout_dir"

upstream_json="$(python3 "$root/scripts/check_upstream.py")"
upstream_commit="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["commit"])' <<<"$upstream_json")"
upstream_commit_date="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["committed_at"])' <<<"$upstream_json")"
upstream_subject="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["message"])' <<<"$upstream_json")"
archive_url="https://github.com/bbopt/solar/archive/${upstream_commit}.zip"
archive_path="$upstream_dir/solar-${upstream_commit}.zip"

clone_upstream() {
    python3 - "$git_timeout_sec" git -c http.version=HTTP/1.1 clone \
        --depth 1 --branch "$branch" "$repo_url" "$checkout_dir" <<'PY'
import subprocess
import sys

timeout_sec = int(sys.argv[1])
cmd = sys.argv[2:]
try:
    raise SystemExit(subprocess.run(cmd, timeout=timeout_sec).returncode)
except subprocess.TimeoutExpired:
    print(
        f"Command timed out after {timeout_sec}s: {' '.join(cmd)}",
        file=sys.stderr,
    )
    raise SystemExit(124)
PY
}

fetch_archive() {
    echo "Using GitHub source archive for SOLAR upstream"
    extract_dir="$upstream_dir/archive-extract"
    rm -rf "$checkout_dir" "$extract_dir"
    mkdir -p "$extract_dir"
    curl --http1.1 -L --fail --connect-timeout 30 --max-time 900 \
        -o "$archive_path" "$archive_url"
    unzip -q "$archive_path" -d "$extract_dir"
    extracted_root="$(find "$extract_dir" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
    if [ -z "$extracted_root" ]; then
        echo "SOLAR source archive did not contain a top-level directory" >&2
        exit 3
    fi
    mv "$extracted_root" "$checkout_dir"
    rm -rf "$extract_dir"
}

case "$sync_method" in
    auto)
        if ! clone_upstream; then
            echo "git clone failed or timed out; falling back to GitHub source archive"
            fetch_archive
        fi
        ;;
    git)
        clone_upstream
        ;;
    archive)
        fetch_archive
        ;;
    *)
        echo "Unsupported SOLAR_SYNC_METHOD: $sync_method" >&2
        exit 2
        ;;
esac

if [ -d "$checkout_dir/.git" ]; then
    checkout_commit="$(git -C "$checkout_dir" rev-parse HEAD)"
    if [ "$checkout_commit" = "$upstream_commit" ]; then
        commit="$upstream_commit"
        commit_date="$upstream_commit_date"
        subject="$upstream_subject"
    else
        commit="$checkout_commit"
        commit_date="$(git -C "$checkout_dir" show -s --format=%cI HEAD)"
        subject="$(git -C "$checkout_dir" show -s --format=%s HEAD)"
    fi
else
    commit="$upstream_commit"
    commit_date="$upstream_commit_date"
    subject="$upstream_subject"
fi

python3 - "$manifest" "$repo_url" "$branch" "$commit" "$commit_date" "$subject" <<'PY'
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

manifest, repo_url, branch, commit, commit_date, subject = sys.argv[1:]
manifest_path = Path(manifest)
previous = {}
if manifest_path.exists():
    try:
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        previous = {}

previous_upstream = previous.get("upstream", {})
if (
    previous_upstream.get("commit") == commit
    and previous_upstream.get("commit_date") == commit_date
    and previous_upstream.get("commit_subject") == subject
):
    synced_at = previous.get("synced_at")
else:
    synced_at = None

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
    "synced_at": synced_at or datetime.now(timezone.utc).isoformat(),
    "policy": {
        "strategy": "track-upstream-latest-with-recorded-commit",
        "vendor_source": False,
        "commit_upstream_checkout": False,
    },
}
manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY

echo "Synced SOLAR upstream commit: $commit"
