# Minimum-cost irrigation with eligible squared lengths: learner

Optional historical bridge practice after minimum spanning trees. The graph is implicit in coordinates and excludes pipes that are too short. It transfers the MST cut invariant without introducing a different spanning-tree objective.

Source contract: [USACO, March 2014 Silver, problem 1](https://usaco.org/index.php?page=viewproblem2&cpid=415). The origin remains explicit even when this historical exercise appears in the Gold appendix.

## Contract

Read `irrigation.in`: `N C`, then N coordinate pairs. There are 1..2000 distinct points, each coordinate lies in 0..1000, and C lies in 1..1000000. A pipe is eligible when its squared Euclidean length is at least C, including equality. Its cost is that squared length. Connect all points at minimum total cost, or write `-1` to `irrigation.out` if impossible. One point costs zero. Use a long total; a square root is never needed.

## Prediction

The official sample in `irrigation.in` is:

```text
3 11
0 2
5 0
4 3
```

Expected `irrigation.out`:

```text
46
```

The three squared lengths are 29, 17 and 10. The cutoff excludes 10; the other two connect all points and total 46. Increasing the cutoff to 30 makes this graph disconnected. A two-point pipe of squared length 25 is permitted at cutoff 25 and refused at 26.

## Tasks and walkthrough

1. Initialize cheapest connecting keys, visited state and a zero root key.
2. Select the cheapest unattached point and distinguish an infinite key from completion.
3. Attach a point and accumulate its connecting key using a long total.
4. Generate squared lengths on demand and relax only eligible pipes to unvisited points.

The learner has four marked algorithm tasks and remains deliberately unfinished. Untouched work exits 2 without writing an answer. The supplied parser and output guards check input and basic result shape; they do not prove reachability or optimality.

For independent study or an instructor walkthrough: predict the sample, explain the state and invariant, trace one transition, implement and save an attempt, and compare a changed tiny case against an independent model. Open the separate reference after the attempt; preserve the original attempt when retrying or comparing variants.

## State and reasoning

A key is the cheapest eligible pipe from the current tree to a point outside it. Selecting the least key preserves the cut property. The cutoff is a lower bound, so reversing the comparison creates a different graph. Infinite remaining keys prove disconnection. Coordinates make individual squares fit int within this contract, but the tree total can exceed int; long intermediate differences also make the numeric intent explicit.

## Build and run

Use JDK 17 or newer inside this role's working folder. These commands also work in PowerShell:

```sh
javac --release 17 -encoding UTF-8 Main.java
java Main
```

Keep `irrigation.in` beside `Main.java`; read `irrigation.out` afterward. The guarded learner parses the complete input, solves and validates the result before opening output, preserving a prior answer on unfinished or refused work. The site IDE can save and export native Java; this program requires native execution and is not run by the Input panel. Source acceptance and confirmed site imports are separate gates.

## Independent checks

Independently enumerate edge subsets on tiny point sets, then check connectivity and the least sum. Cover cutoff equality, one point, disconnection, widely spaced points and a full 2000-point construction. One full construction has two rows a thousand units apart and a known MST total 1999000999. Another uses two small opposite-corner clusters; singleton-cut reasoning yields a tree total above int. The dense reference computes edges as needed in O(N^2) time and O(N) extra space.

From the repository root run `python3 tests/verify-historical-algorithm-packs.py --javac javac --java java`. Hosted acceptance repeats with JDK 17 and 21. Temporary driver probes check supplied infrastructure only; they do not complete or grade the saved learner algorithm.
