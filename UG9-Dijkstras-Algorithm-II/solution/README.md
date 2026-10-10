# Matrix Dijkstra reference

Open this separate reference after retaining a learner attempt. It keeps
the historical matrix and lazy queue. Marked repairs use long distances,
safe queue comparisons, minimum parallel weights and explicit unreachable
output. `../legacy/Main.java` preserves the original bytes; the historical
sample input and output are unchanged.

With native JDK 17 or 21, the working directory's `dijkstra.in` contains
`N M` followed by exactly `M` undirected records `a b weight`. Vertices
are zero-based and source is 0. Teaching limits: `1 <= N <= 2000`,
`0 <= M <= 200000`, `0 <= weight <= 2147483647`. Parallel edges retain
their minimum; self-loops, zero weights and disconnected vertices are valid.
Matrix `-1` is absent, not zero. This historical reference expects valid
input; malformed-input and prior-answer protections belong to the learner.

From this folder:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
```

Read `dijkstra.out`, not standard output. For each destination 1 through
`N-1`, it contains `0 ... destination Distance: total` for a simple
minimum-cost route, or `Unreachable: destination`. Any tied optimum is valid;
`N=1` produces an empty file. The sample distances are 7, 9, 20, 20 and 11;
one path to vertex 4 is `0 2 5 4 Distance: 20`.

Explain why a fresh minimum-key pop finalizes a distance for nonnegative
weights, why stale states are skipped before row scans, and why strict
improvement avoids zero-cycle predecessor changes. Compare with the four
learner tasks without copying the whole reference. In an instructor
walkthrough, trace competing paths to vertex 3 and then compare matrix
cells scanned with adjacency-list edges visited.

Test parallel weights 1 then 9 in both orders, disconnected graphs, zero
cycles, tied routes and two 1500000000-weight edges (total 3000000000).
Check endpoints, each edge and cost, then compare separate Bellman-Ford
distances to establish optimality. This is optional representation practice,
not a road-crossing problem or a new required lesson. The loose time bound
is `O(M + N^2 log N + P)` and storage is `O(N^2)`, where `P` counts all
printed path vertices. Output may be quadratic; this reference streams lines.

Repository gate: `python3 tests/verify-matrix-dijkstra-pack.py --javac javac --java java`.
Hosted acceptance repeats actual JDK 17 and 21 for both roles. These checks
cover explicit teaching limits, not official contest bounds. The site IDE
saves/exports work; use the commands above to execute it. See the
[complete guide](https://github.com/instruction-material/USACO-Gold/blob/main/UG9-Dijkstras-Algorithm-II/README.md) for the sample paths and full comparison.
