#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
checkout_dir="$root/upstream/solar"

if [ ! -d "$checkout_dir" ]; then
    bash "$root/scripts/sync_solar.sh"
fi

if [ -n "${PYTHON:-}" ]; then
    python_bin="$PYTHON"
elif command -v python3 >/dev/null 2>&1; then
    python_bin="python3"
else
    python_bin="python"
fi

case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*)
        exe_ext=".exe"
        make_args=(EXEEXT="$exe_ext" LIBS="-lm")
        ;;
    *)
        exe_ext=""
        make_args=(EXEEXT="$exe_ext")
        ;;
esac

"$python_bin" "$root/scripts/patch_solar_checkout.py" "$checkout_dir"
mkdir -p "$checkout_dir/bin"
make -C "$checkout_dir/src" "${make_args[@]}"
test -f "$checkout_dir/bin/solar$exe_ext"

echo "Built SOLAR executable: $checkout_dir/bin/solar$exe_ext"
