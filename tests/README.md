# Test Plan

The first executable tests should be added after `scripts/sync_solar.sh` can
clone and build upstream SOLAR reliably in CI.

Initial smoke tests:

1. Run `scripts/check_upstream.py` and verify it returns JSON with an upstream
   commit.
2. Run `scripts/sync_solar.sh`.
3. Build upstream with `make` in `upstream/solar/src`.
4. Evaluate upstream README example:

   ```bash
   upstream/solar/bin/solar 1 upstream/solar/tests/1_MAXNRG_H1/x0.txt
   ```

5. Verify `solar_adapter.runner.parse_solar_output` maps the example output to
   one objective and five inequality constraints.

Full `solar -check` may take 10-20 minutes and should be a separate CI job, not
part of every lightweight pull request.

