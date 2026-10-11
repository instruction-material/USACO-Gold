# Disjoint sets and Kruskal cycle decisions: reference

A dedicated DSU exercise following the core MST checkpoint. Find/union component invariants justify why a candidate edge creates a cycle. Compare Kruskal sorting with the existing Prim cut frontier; path compression is an optional extension, not a prerequisite of the reference.

## Contract

Read `kruskal.in`: `N M`, then M undirected `P Q W` edges, with zero-based vertices. Teaching bounds are 1 <= N <= 200000, 0 <= M <= 200000, and 0 <= W <= 1000000000. Require a connected graph; one vertex with no edges is valid. Parallel edges and self-loops are permitted. Write `kruskal.out` as N-1 selected endpoint pairs, one per line, with no total line. Any minimum tree and tie order are valid. Accumulate edge weights in long when checking its cost. The reference assumes valid tokens/bounds and refuses disconnection before opening output. Its trace is opt-in with `java -Dcourse.trace=true Main`.

## Prediction

The supplied six-vertex graph has optimum 33. One valid reference output selects edges 2-5 (2), 3-4 (6), 0-1 (7), 0-2 (9), and 4-5 (9). Follow the component count 6,5,4,3,2,1. Size is meaningful only at a representative root; values stored at former roots can be stale.

## Tasks and walkthrough

1. Follow parent links to a component representative.
2. Join different roots by size, updating the winning size and count once.
3. Sort a copy of the edge list and initialize singleton components.
4. Accept only edges between different components, ending with N-1 edges or refusing disconnection.

This role is a completed reference for comparison after a saved attempt. Its original source bytes remain in `../legacy/Main.java`; only the documented small correctness or trace-control repairs change the maintained program.

For independent work or an instructor walkthrough: predict the sample, state the invariant, trace one transition, save the attempt, and compare an independently checked changed case before opening the separate reference. Return to the same attempt for reflection; use changed small datasets for transfer practice.

## Build and run

Use JDK 17 or newer inside this role's working directory. These commands also work in PowerShell:

```sh
javac --release 17 -encoding UTF-8 Main.java
java Main
```

Keep `kruskal.in` in this role directory. The program writes `kruskal.out` only after the algorithm returns a valid feasible result. The site IDE saves and exports this native Java project; native execution is required, and its Input panel does not run this program.

## Independent checks

Check repeated union, union within one component, ties, zero weights, parallel edges, self-loops, one vertex and disconnection. Independently enumerate tiny spanning trees and compare the minimum selected weight; do not require one fixed optimal edge ordering. Check that every selected edge came from input and that the result connects all vertices. Preserve an earlier answer when a task is unfinished or input is refused. Use the optional trace only for small graphs.

Union by size without path compression bounds parent depth by O(log N). Sorting and DSU work take O(M log M + M log N) time and O(N+M) space. The supplied output validator also uses O(N+M) time/space. Explain amortized near-constant operations only after implementing path compression; do not attribute them to the preserved reference.

From the repository root, run `python3 tests/verify-implementation-labs.py --javac javac --java java`. Hosted acceptance repeats with JDK 17 and 21. Driver probes validate supplied infrastructure in temporary copies; they do not complete or grade the saved learner algorithm.
