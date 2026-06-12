# Mapping SOLAR to OptiProfiler Problems

OptiProfiler problem libraries provide two language-specific functions:

Python:

```python
solar_load(problem_name) -> optiprofiler.opclasses.Problem
solar_select(options) -> list[str]
```

MATLAB:

```matlab
solar_load(problem_name) -> problem struct/class accepted by OptiProfiler
solar_select(options) -> cell array of names
```

This repository starts with the common executable protocol and metadata. Python
and MATLAB wrappers can later be split into `solar_python` and `solar_matlab`
while sharing the same protocol.

## Problem Metadata

Each enabled SOLAR problem needs a metadata record:

```text
name              OptiProfiler-facing name, e.g. SOLAR1_MAXNRG_H1
pb_id             SOLAR integer problem id
description       short scientific description
n                 dimension
m_objectives      objective count
m_constraints     constraint count
x0                starting point used by OptiProfiler
xl, xu            finite/infinite bounds, if known
constraint_kind   initially nonlinear_ub
deterministic     true/false under seed=0, fid=1, rep=1
enabled           whether OptiProfiler may select it
reason_disabled   if disabled
```

Only enabled, single-objective records should be returned by `solar_select` in
the first implementation.

## Python `Problem` Construction

SOLAR should be represented as a nonlinearly constrained `Problem`:

```python
from optiprofiler.opclasses import Problem

state = SolarProblemState(metadata, executable)

problem = Problem(
    name=metadata["name"],
    fun=state.fun,
    x0=metadata["x0"],
    xl=metadata.get("xl"),
    xu=metadata.get("xu"),
    cub=state.cub if metadata["m_constraints"] > 0 else None,
)
```

No linear constraints should be invented unless SOLAR metadata explicitly
separates them. At the adapter boundary, SOLAR constraints are initially treated
as nonlinear inequalities `cub(x) <= 0`.

## Adapter Oracle Cache and OptiProfiler Accounting

OptiProfiler may call:

```python
problem.fun(x)
problem.cub(x)
```

for the same `x`. A naive wrapper would launch SOLAR twice. The adapter should
cache the most recent raw SOLAR oracle result:

```python
class SolarProblemState:
    def __init__(self, metadata, executable):
        self.metadata = metadata
        self.executable = executable
        self._last_x = None
        self._last_eval = None

    def _eval(self, x):
        if same_vector(x, self._last_x):
            return self._last_eval
        result = run_solar(self.executable, self.metadata["pb_id"], x)
        self._last_x = copy(x)
        self._last_eval = result
        return result

    def fun(self, x):
        return float(self._eval(x).objectives[0])

    def cub(self, x):
        return self._eval(x).constraints
```

This cache must be private to the adapter oracle. It is only an executable
acceleration layer and must not change OptiProfiler's evaluation accounting.

In particular:

- `fun(x)` must not call the OptiProfiler-visible `cub(x)` or `ceq(x)`.
- `cub(x)` must not call the OptiProfiler-visible `fun(x)` or `ceq(x)`.
- A SOLAR executable call made while answering `fun(x)` may cache objective and
  constraint numbers internally, but OptiProfiler should see only a function
  evaluation.
- If OptiProfiler later asks `cub(x)` at the same point, `cub(x)` may reuse the
  adapter cache instead of rerunning SOLAR; OptiProfiler should see only the
  constraint evaluation it explicitly requested.
- The cache should be per problem object, not global across tasks or solver
  runs.

This distinction matters because OptiProfiler's `Problem` / featured problem
layer records objective and constraint histories separately. SOLAR's executable
is a joint oracle, but the adapter must preserve OptiProfiler's public
`fun`/`cub`/`ceq` semantics.

The wrapper must also avoid expensive simulator calls while the `Problem`
constructor is only inferring output dimensions. Shape-probe shortcuts may
return a correctly sized placeholder, but only inside the adapter boundary.
They must not append objective or constraint histories and must not leak into
normal user evaluations.

## Runtime Contents

The language-specific repositories should use the generated slim runtime from
`scripts/export_runtime.sh`. They should include the source needed to rebuild
SOLAR, the license/provenance files, and the generated OptiProfiler metadata.
They should not include upstream's large `tests/` directory, upstream `.git`
history, generated object files, or generated binaries.

The intended lifecycle is:

1. `solar_adapter` syncs and records an upstream commit.
2. `solar_adapter` validates metadata against the executable.
3. `scripts/export_runtime.sh` produces a slim runtime.
4. `solar_python` and `solar_matlab` vendor that runtime source and build the
   executable locally or in CI.

## Selection

`solar_select(options)` should filter metadata by OptiProfiler's standard
fields:

- `ptype`
- `mindim`, `maxdim`
- `minb`, `maxb`
- `minlcon`, `maxlcon`
- `minnlcon`, `maxnlcon`
- `mincon`, `maxcon`
- `excludelist`

Since the initial SOLAR mapping treats constraints as nonlinear inequalities,
most enabled SOLAR instances will have `ptype == "n"` except the unconstrained
instance.

## Integer Variables

SOLAR's metadata distinguishes real variables (`R`) from integer/categorical
variables (`I`). Several enabled scalar instances are mixed-integer. Upstream
SOLAR rejects noninteger values for these coordinates, which is a poor fit for
continuous DFO solvers that naturally propose real-valued trial points.

The first wrapper policy is:

1. keep `x0`, `xl`, and `xu` visible to OptiProfiler in the original dimension;
2. immediately before calling the SOLAR executable, round every `I` coordinate
   to the nearest integer;
3. clip rounded integer coordinates to their finite integer bounds;
4. cache and account evaluations under OptiProfiler's usual `fun`/`cub`
   semantics, without adding extra visible evaluations.

This policy makes mixed-integer SOLAR instances runnable by continuous solvers,
but it must be reported as a wrapper-level rounding rule. It should not be
confused with a native continuous benchmark. A strictly continuous DFO subset
should use only the pure-real SOLAR instances, currently SOLAR 6 and SOLAR 10.

## Stochastic and Fidelity Policy

The first adapter version should avoid changing OptiProfiler's feature model.
Do not expose stochastic replications, `seed=diff`, or non-truth fidelity as
ordinary `plain` problems.

Later options:

- expose `fid < 1` as a separate problem-library configuration;
- expose stochastic instances under a dedicated feature or benchmark family;
- keep multiobjective SOLAR instances out of standard scalar DFO profiles until
  a multiobjective policy exists.
