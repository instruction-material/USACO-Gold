# Matrix Dijkstra learner

Optional representation practice after the core adjacency-list lesson.
Retain predictions and a learner attempt before comparing the reference.
Complete only the four TODOs in `shortestPaths`: initialize long distances
and predecessors, seed the queue, skip stale states, and scan matrix rows
with strict-improvement relaxation. Return `Result(distance, previous)`.
The supplied `State` compares 64-bit keys without overflowing subtraction.

The working directory's `dijkstra.in` contains `N M`, then exactly `M`
undirected edges `a b weight`. Vertices are zero-based and source is 0.
Teaching limits: `1 <= N <= 2000`, `0 <= M <= 200000`,
`0 <= weight <= 2147483647`. Minimum parallel weights are retained;
self-loops, zero weights and disconnected vertices are supported.
`graph.weight[a][b] == -1` means absent, while zero is a real edge.

`dijkstra.out` has one line per destination 1 through `N-1`:
`0 ... destination Distance: total`, or `Unreachable: destination`.
Any simple minimum-cost tied route is valid; `N=1` produces an empty file.
The sample's distances are 7, 9, 20, 20 and 11. Two 1500000000-weight edges
must have a positive 3000000000 total.

Draw the sample matrix and predict the first two queue pops before coding.
Explain stale entries and compare scanned matrix cells on a sparse chain
with adjacency-list edges visited. During an instructor walkthrough, trace
a predecessor update, justify strict improvement for zero-weight ties,
and explain why sparse graphs still pay `O(N^2)` matrix storage.

From this folder with JDK 17 or 21:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
```

The untouched scaffold exits 2 and preserves an earlier answer. The supplied
driver refuses malformed/missing input, negative weights, size violations,
invalid vertices, extra records and arguments before writing. It validates
every predecessor chain and edge sum before opening the answer file, but
does not establish minimum distances. Check independently with Bellman-Ford
or hand calculations, not output shape alone.

Try parallel edges in both orders, isolated vertices, zero cycles, ties and
large totals. Time is `O(M + N^2 log N + P)` and storage is `O(N^2 + P)`
including retained answer lines, where `P` is printed path size. Save/export
work in the site IDE and run Java natively. Repository acceptance:
`python3 tests/verify-matrix-dijkstra-pack.py --javac javac --java java`.
The [complete guide](../README.md) gives sample paths and the comparison.
