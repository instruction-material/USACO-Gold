# Gold native setup checkpoint

This is the required setup project before advanced Gold algorithms. It
checks the native input/output contract and 64-bit totals separately from
MooTube, disjoint sets and offline sorting.

Start with `starter/`, predict its supplied sample, complete the total task
and keep the learner attempt. Compare `solution/` after an attempt. Each
role includes a complete standalone guide and the same sample. Both use
JDK 17 or newer and standard input/output; they do not use `mootube.in` or
`mootube.out`. The site IDE saves and exports native Java and displays build
directions when Run is selected.

The guides specify N from 0 to 200000, values from -1000000000 to 1000000000,
the use of `long`, the expected sample total 2999999990, changed-case checks
and failure behavior. The unfinished learner produces no answer even at
N=0. Parse the whole input before writing an answer.

Acceptance: `python3 tests/verify-setup-pack.py`. The existing dedicated
workflow exercises both exported roles on JDK 17 and 21, signed totals,
maximum positive/negative bounds, malformed and trailing input, retained
files, and unfinished-work behavior.
