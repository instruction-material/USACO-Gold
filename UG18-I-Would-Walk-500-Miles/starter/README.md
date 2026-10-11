# Maximum-spacing groups from an implicit complete graph: learner

Optional clustering application after MST cut reasoning. The goal is the largest possible minimum distance between groups, rather than the smallest total tree cost. It keeps the historical implicit-graph approach; the derived formula is a later comparison.

Source contract: [USACO, US Open 2019 Gold, problem 2](https://usaco.org/index.php?page=viewproblem2&cpid=946). The origin remains explicit even when this historical exercise appears in the Gold appendix.

## Contract

Read `walk.in` as `N K`, with 2 <= K <= N <= 7500. Cows have labels 1..N. For x < y their distance is `(2019201913*x + 2019201949*y) mod 2019201997`. Form exactly K nonempty groups and maximize the least distance between cows belonging to different groups. Write that spacing to `walk.out`. Evaluate multiplication and addition in long arithmetic before the modulo.

## Prediction

The official sample in `walk.in` is:

```text
3 2
```

Expected `walk.out`:

```text
2019201769
```

Distances for pairs (1,2), (1,3), (2,3) are 2019201817, 2019201769 and 2019201685. Grouping {1} and {2,3} yields spacing 2019201769. For three singleton groups the spacing is 2019201685. The historical Prim list includes a root zero, which is not a connecting edge.

## Tasks and walkthrough

1. Generate the symmetric distance with one-based labels and long intermediate products.
2. Build an MST by selecting the cheapest unattached key and relaxing implicit neighbors.
3. Keep the N-1 real connecting weights separate from the root zero, or account explicitly for its list position.
4. Remove K-1 largest connecting edges and identify the smallest removed weight as the maximum spacing.

The learner has four marked algorithm tasks and remains deliberately unfinished. Untouched work exits 2 without writing an answer. The supplied parser and output guards check input and basic result shape; they do not prove reachability or optimality.

For independent study or an instructor walkthrough: predict the sample, explain the state and invariant, trace one transition, implement and save an attempt, and compare a changed tiny case against an independent model. Open the separate reference after the attempt; preserve the original attempt when retrying or comparing variants.

## State and reasoning

The ascending MST construction joins the nearest remaining components. After N-K connecting edges there are K components; the next connecting weight is their spacing. Any attempted partition with larger spacing would need to keep every smaller connection inside a group, leaving fewer than K available groups once that next connection is included. Equivalently remove K-1 largest MST edges. With N-1 real weights sorted ascending the spacing index is N-K; the historical length-N list includes the root zero and therefore uses N-K+1. This is the (K-1)th largest real edge, not the Kth largest.

## Build and run

Use JDK 17 or newer inside this role's working folder. These commands also work in PowerShell:

```sh
javac --release 17 -encoding UTF-8 Main.java
java Main
```

Keep `walk.in` beside `Main.java`; read `walk.out` afterward. The guarded learner parses the complete input, solves and validates the result before opening output, preserving a prior answer on unfinished or refused work. The site IDE can save and export native Java; this program requires native execution and is not run by the Input panel. Source acceptance and confirmed site imports are separate gates.

## Independent checks

Enumerate every unlabelled partition for tiny N and compute the smallest cross-group distance directly. Test N=2, K=2, K=N, one-based labels and products larger than int. Full-bound checks cover N=7500 with K=2 and K=N. The historical implementation takes O(N^2 + N log N) time and O(N) space. Only after implementing and checking this approach, derive the closed-form spacing by simplifying the edge formula and proving the resulting MST structure.

From the repository root run `python3 tests/verify-historical-algorithm-packs.py --javac javac --java java`. Hosted acceptance repeats with JDK 17 and 21. Temporary driver probes check supplied infrastructure only; they do not complete or grade the saved learner algorithm.
