# Priority-queue Prim with a dense matrix: learner

A focused implementation comparison after the core matrix Prim checkpoint. The queue changes vertex selection; the matrix still changes storage and neighbor-scan costs. MST II here means a second implementation of MST construction, not the second-best spanning-tree problem.

## Contract

Read `prim.in`: `N M`, then M undirected edge lines `P Q W`. Vertices are zero-based. Teaching bounds are 1 <= N <= 2000, 0 <= M <= 200000, and 0 <= W <= 1000000000. The graph must be connected; N=1 and M=0 is valid. Parallel edges retain their cheapest weight and self-loops cannot join a tree. Write `prim.out`: one `vertex parent` line for each vertex 1 through N-1, then `Total Distance: TOTAL`. Root 0 has no printed parent. Use a long total. Any minimum tree is valid; tie-dependent parent choices may differ. The reference assumes valid tokens/bounds and refuses a disconnected graph before opening output.

## Prediction

The supplied six-vertex, nine-edge graph has minimum total 33. Compare the provided reference edges with an independent cut or spanning-tree enumeration; do not require identical parents when weights tie. A two-vertex graph with weights 1 then 9 on the same pair must use weight 1. A three-vertex chain of weight 1000000000 on each edge totals 2000000000; a four-vertex chain totals 3000000000.

## Tasks and walkthrough

1. Initialize keys, parents, visited state and the root queue entry.
2. Extract the cheapest key and ignore already-attached vertices.
3. Attach a fresh vertex and add its connecting key to a long total.
4. Relax neighbors using one edge weight and enqueue improved keys.

The distinct learner has four marked tasks. Untouched tasks exit 2 without producing an answer. The supplied driver validates parameters and feasible result structure; it does not prove algorithm optimality.

For independent work or an instructor walkthrough: predict the sample, state the invariant, trace one transition, save the attempt, and compare an independently checked changed case before opening the separate reference. Return to the same attempt for reflection; use changed small datasets for transfer practice.

## Build and run

Use JDK 17 or newer inside this role's working directory. These commands also work in PowerShell:

```sh
javac --release 17 -encoding UTF-8 Main.java
java Main
```

Keep `prim.in` in this role directory. The program writes `prim.out` only after the algorithm returns a valid feasible result. The site IDE saves and exports this native Java project; native execution is required, and its Input panel does not run this program.

## Independent checks

Check one vertex, zero-weight edges, ties, heavier parallel edges appearing last, self-loops, a disconnected graph and a total above int. Independently enumerate trees on small graphs and check N-1 real edges, connectivity, acyclicity and the reported sum. Preserve the previous answer on unfinished or refused runs. Queue staleness must not rescan matrix rows.

Storage is O(N^2 + M) for the matrix and worst-case queued improvements. With each vertex row scanned once, time is O(N^2 + M log M). A priority queue does not turn this dense representation into a sparse adjacency-list implementation.

From the repository root, run `python3 tests/verify-implementation-labs.py --javac javac --java java`. Hosted acceptance repeats with JDK 17 and 21. Driver probes validate supplied infrastructure in temporary copies; they do not complete or grade the saved learner algorithm.
