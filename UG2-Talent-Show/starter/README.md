# Ratio optimization with clamped minimum-weight DP: learner

Optional advanced DP application after 0-1 choices and binary-search invariants. It optimizes a ratio subject to a minimum weight, rather than maximizing value below a capacity. It keeps the feasibility-DP problem intact.

Source contract: [USACO, US Open 2018 Gold, problem 3](https://usaco.org/index.php?page=viewproblem2&cpid=839). The origin remains explicit even when this historical exercise appears in the Gold appendix.

## Contract

Read `talent.in`: `N W`, then N lines `weight talent`. There are 1..250 cows; W is 1..1000; each weight is 1..1000000 and each talent is 1..1000. The total available weight reaches W. Select a subset with total weight at least W and maximize total talent divided by total weight. Write the floor of 1000 times that ratio to `talent.out`. Each cow may be selected once. Use integer and long arithmetic, with no floating-point rounding.

## Prediction

The learner `talent.in` contains the official sample below. The reference keeps its historical 150-cow `talent.in` and `talent.out` (expected `26706`) unchanged; its separately named `official-sample.in` contains the official sample. To run that sample in the reference, copy it to `talent.in` in a disposable working copy first.

Official sample:

```text
3 15
20 21
10 11
30 31
```

Expected `talent.out`:

```text
1066
```

The weight-10 cow alone has ratio 11/10 but misses the weight threshold. Combining it with the weight-20 cow gives 32/30; flooring 1000 times that ratio yields 1066. A cow heavier than W is still permitted. A DP state at W means total weight at least W, not weight exactly W.

## Tasks and walkthrough

1. For a proposed scaled ratio r, initialize unreachable states and the zero-weight empty choice.
2. Process each cow once, tracking the largest transformed score and clamping all weights above W to W.
3. Decide feasibility from the threshold state and explain the score `sum(1000*talent - r*weight)`.
4. Binary-search the greatest feasible integer ratio using a feasible lower bound and an infeasible exclusive upper bound.

The learner has four marked algorithm tasks and remains deliberately unfinished. Untouched work exits 2 without writing an answer. The supplied parser and output guards check input and basic result shape; they do not prove reachability or optimality.

For independent study or an instructor walkthrough: predict the sample, explain the state and invariant, trace one transition, implement and save an attempt, and compare a changed tiny case against an independent model. Open the separate reference after the attempt; preserve the original attempt when retrying or comparing variants.

## State and reasoning

A selected subset has scaled ratio at least r precisely when its transformed score is nonnegative. For the same clamped weight, a larger score dominates a smaller score. All threshold-or-heavier states have identical future eligibility, so they can share state W. Separate previous/next rows ensure each cow is used once. Feasibility is monotone as r increases because all weights are positive. The greatest feasible integer r is the required floor. The reference row i includes cows 0 through i; its first-cow initialization is a special first row. A zero lower bound is feasible, and 250*1000*1000+1 is a safe exclusive upper bound.

## Build and run

Use JDK 17 or newer inside this role's working folder. These commands also work in PowerShell:

```sh
javac --release 17 -encoding UTF-8 Main.java
java Main
```

Keep `talent.in` beside `Main.java`; read `talent.out` afterward. The guarded learner parses the complete input, solves and validates the result before opening output, preserving a prior answer on unfinished or refused work. The site IDE can save and export native Java; this program requires native execution and is not run by the Input panel. Source acceptance and confirmed site imports are separate gates.

## Independent checks

Independently enumerate subsets on small inputs and compare exact integer ratios. Cover a single overweight cow, exact threshold equality, first-cow use, states above W, unattainable intermediate weights and floor boundaries. Full-bound checks use 250 cows, W=1000 and individual weights of a million. The historical two-dimensional reference takes O(N*W*log R) time and O(N*W) space, where R is the binary-search bound. A rolling-row implementation may reduce memory after its one-use invariant is established.

From the repository root run `python3 tests/verify-historical-algorithm-packs.py --javac javac --java java`. Hosted acceptance repeats with JDK 17 and 21. Temporary driver probes check supplied infrastructure only; they do not complete or grade the saved learner algorithm.
