#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
checkout_dir="$root/upstream/solar"

if [ ! -d "$checkout_dir" ]; then
    bash "$root/scripts/sync_solar.sh"
fi

python3 "$root/scripts/patch_solar_checkout.py" "$checkout_dir"
mkdir -p "$checkout_dir/bin"
make -C "$checkout_dir/src"
test -x "$checkout_dir/bin/solar"

echo "Built SOLAR executable: $checkout_dir/bin/solar"
