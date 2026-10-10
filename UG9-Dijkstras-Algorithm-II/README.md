# Dijkstra II: compare graph representations

Optional practice after the core Gold shortest-path lesson. The core pack
uses adjacency lists; this pack keeps a dense matrix and a lazy priority
queue to study the same invariant with a different storage cost. It is a
representation comparison, not a second required Dijkstra lesson or a
solution to the USACO road-crossing problem.

## Contract

Use native JDK 17 or 21. The working directory's `dijkstra.in` contains
`N M`, followed by exactly `M` lines `a b weight`. The graph is undirected,
vertices are `0` through `N-1`, and the source is `0`. Teaching limits:
`1 <= N <= 2000`, `0 <= M <= 200000`, `0 <= weight <= 2147483647`.
These are explicit teaching limits, not official contest bounds. Parallel
records retain their minimum weight; self-loops, zero weights and disconnected
vertices are allowed. Matrix `-1` means absent; zero is a real edge.

`dijkstra.out` has one line per destination `1` through `N-1` in that order.
A reachable line lists a simple path from 0 to that destination followed by
`Distance: total`; any minimum-cost path is valid when routes tie. An
unreachable line is `Unreachable: destination`. For `N=1`, the answer file is
empty. Successful runs do not print answers to standard output. Store
totals in `long`: `(N-1) * 2147483647` exceeds `int` and fits in `long`.

The unchanged six-vertex sample has distances 7, 9, 20, 20, 11. One valid
set of paths is:

```text
0 1 Distance: 7
0 2 Distance: 9
0 2 3 Distance: 20
0 2 5 4 Distance: 20
0 2 5 Distance: 11
```

## Independent work or an instructor walkthrough

Start in `starter/`, retain predictions and code attempts, and open the
separate `solution/` after an attempt. Draw the sample matrix and predict
which row is scanned first. Explain how a queued entry becomes stale and
why scanning that stale entry's entire row wastes work. Count matrix cells
examined versus adjacency-list edges visited on a chain, star and dense graph.

Complete the four tasks in `shortestPaths`: initialize distances and
predecessors; seed the priority queue; poll and skip stale entries; scan the
current row and relax on strict improvement. The provided driver validates
input, collapses parallel records, checks predecessor chains and path edge
sums, and writes only after those checks pass. Path consistency does not
prove optimality; use separate Bellman-Ford distances or hand calculations.

For a guided session, explain each prediction before changing code, trace
one relaxation and one stale entry, and justify the same shortest-path
invariant used by the core adjacency-list implementation. In review, compare
examined neighbors, storage and printed path size. The reference preserves
the historical matrix algorithm with small marked repairs.

## Native build and run

From either role folder with `dijkstra.in` beside the program:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
```

Read `dijkstra.out` after success. The untouched learner exits 2 with a task
message, produces no answer and preserves an earlier answer. Missing or
malformed input, negative weights, out-of-range vertices, size violations,
extra records and unexpected arguments are refused before writing. The
historical reference expects valid input; it does not claim the learner
driver's malformed-input protections. The site IDE saves and exports Java
files; execute them natively with the commands above.

## Changed cases and cost

Try parallel records `0 1 1` then `0 1 9`, and reverse their order: the
distance to 1 must remain 1. Two 1500000000-weight edges must yield
3000000000. Add an isolated vertex, tied routes and a zero-weight cycle.
Validate every returned edge and its summed cost; accept any tied optimum.

Fresh queue pops scan at most `N` rows of `N` cells. The loose worst-case
time bound is `O(M + N^2 log N + P)`, where `M` counts input records and
`P` counts printed path vertices. Matrix and queue storage use `O(N^2)`;
the learner additionally retains `O(P)` answer characters/vertices before
writing. Sparse graphs still pay matrix allocation and row-scan costs.
Compare the core adjacency-list bound `O((N+M) log(N+M) + P)`. Printing
every destination path can itself require quadratic output.

From the repository root:

```sh
python3 tests/verify-matrix-dijkstra-pack.py --javac javac --java java
```

Acceptance compiles both actual roles, compares reference distances with
independent Bellman-Ford relaxation, validates any returned path, covers
teaching limits and refused learner inputs, and checks supplied drivers with
small oracle probes without completing the learner algorithm. Hosted gates
use actual JDK 17 and 21. This is a teaching-contract gate, not a formal
contest judge verdict. `legacy/` preserves the original reference bytes and
is excluded from role imports and active source counts.
