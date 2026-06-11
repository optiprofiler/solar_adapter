#!/usr/bin/env python3
"""Report the current upstream bbopt/solar default-branch revision."""

from __future__ import annotations

import json
import urllib.request


API_URL = "https://api.github.com/repos/bbopt/solar/commits/master"


def main() -> int:
    with urllib.request.urlopen(API_URL, timeout=30) as response:
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

