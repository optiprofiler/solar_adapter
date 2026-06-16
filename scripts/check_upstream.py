#!/usr/bin/env python3
"""Report the current upstream bbopt/solar default-branch revision."""

from __future__ import annotations

import json
import os
import urllib.request


API_URL = "https://api.github.com/repos/bbopt/solar/commits/master"


def main() -> int:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "optiprofiler-solar-adapter",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(API_URL, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)

    commit = payload["sha"]
    committed_at = payload["commit"]["committer"]["date"]
    message = payload["commit"]["message"].splitlines()[0]

    print(json.dumps({
        "repository": "bbopt/solar",
        "branch": "master",
        "commit": commit,
        "committed_at": committed_at,
        "message": message,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
