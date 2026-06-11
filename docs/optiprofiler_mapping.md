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

## Shared Evaluation Cache

OptiProfiler may call:

```python
problem.fun(x)
problem.cub(x)
```

for the same `x`. A naive wrapper would launch SOLAR twice. The adapter should
cache the most recent `x` and parsed result:

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

This cache should be per problem object, not global across tasks.

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

## Stochastic and Fidelity Policy

The first adapter version should avoid changing OptiProfiler's feature model.
Do not expose stochastic replications, `seed=diff`, or non-truth fidelity as
ordinary `plain` problems.

Later options:

- expose `fid < 1` as a separate problem-library configuration;
- expose stochastic instances under a dedicated feature or benchmark family;
- keep multiobjective SOLAR instances out of standard scalar DFO profiles until
  a multiobjective policy exists.

