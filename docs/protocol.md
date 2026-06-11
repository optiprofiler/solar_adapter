# SOLAR Adapter Protocol

This document defines the boundary between OptiProfiler wrappers and the SOLAR
executable.

## Upstream Command

Upstream SOLAR exposes a command-line interface:

```bash
solar pb_id x.txt -seed=S -fid=F -rep=R
```

where `x.txt` contains one point per line, with coordinate values separated by
spaces.

For the first OptiProfiler integration, use:

```bash
solar pb_id x.txt -seed=0 -fid=1.0 -rep=1
```

This selects a deterministic seed, truth fidelity, and one replication.

## Adapter-Level Function

The common adapter should expose a function equivalent to:

```text
evaluate(problem_id, x, seed=0, fidelity=1.0, replications=1)
    -> SolarEvaluation
```

where:

```text
SolarEvaluation.objectives    : vector of length p
SolarEvaluation.constraints   : vector of length m, interpreted as <= 0
SolarEvaluation.raw_stdout    : original command output
SolarEvaluation.returncode    : executable return code
SolarEvaluation.elapsed_sec   : wall-clock runtime
```

The adapter should raise a clear exception if:

- the executable is missing;
- the process times out;
- the output cannot be parsed;
- the problem id is unsupported by the current curated subset;
- a multiobjective problem is requested before policy support exists.

## Output Parsing

For SOLAR single-objective constrained instances, the README example shows one
line:

```text
-122505.5978 -10881140.57 -1512631.39776 -134 -4.5 0
```

The first value is the objective. The remaining values are constraints in the
SOLAR convention. The initial adapter should treat them as nonlinear inequality
constraints satisfying `c_i(x) <= 0`, after verifying this convention against
upstream documentation and smoke cases.

If a future SOLAR instance uses equality constraints or a different output
shape, it must be represented explicitly in metadata before being enabled.

## Reproducibility Defaults

Default benchmark mode:

- `seed = 0`
- `fidelity = 1.0`
- `replications = 1`
- no `-v` unless debugging
- one vector per call unless batching is explicitly implemented and tested

Do not use `-seed=diff` for default OptiProfiler benchmarks because it makes
the same `x` produce different outputs across calls.

## Runtime Isolation

SOLAR is an external executable, so hosted use should run it inside the same
sandbox/resource framework as solver jobs:

- process timeout per evaluation;
- memory and CPU limits;
- temporary input/output directory;
- no ambient writes outside the task directory;
- captured stdout/stderr;
- recorded executable path and upstream commit.

