# Dijkstra: nonnegative weighted paths

This required USACO Gold Unit 2 project is an authored algorithm demonstration,
not an official contest problem with an invented problem number. The original
Juni example's undirected edges, source vertex 0, file names and reachable-path
output are retained. The current pack adds a complete learner scaffold, explicit
unreachable output, numeric bounds, and a priority queue aligned with the unit.
The original matrix implementation is preserved byte-for-byte under `legacy/`.

## Prerequisites and contract

Prior concepts are adjacency lists, arrays, priority queues, graph paths and
nonnegative edge weights. `dijkstra.in` starts with `N M`, followed by exactly
`M` lines `P Q W`. Vertices are zero-based and each edge works in both directions.
Practice limits are `1 <= N <= 2000`, `0 <= M <= 200000`, and
`0 <= W <= 1000000000`. These are explicit limits for this maintained
demonstration, not attributed historical contest limits. Parallel edges,
self-loops, isolated vertices and zero-weight edges are permitted. Negative
weights, malformed or extra records, out-of-range vertices and missing files
are refused before an earlier answer can be replaced.

`dijkstra.out` has one line per destination, in order 1 through N-1. A reachable
line lists its source-to-destination vertices followed by `Distance: value`.
An unreachable destination uses `Unreachable: i`. With N=1 the answer file is
empty. Equal-cost paths need not have one unique vertex sequence; verify the
endpoints, real edges and total weight. The supplied reference uses strict
improvements and a distance-then-vertex queue order for reproducibility.

## Reasoning and learner tasks

`distance[v]` is the best discovered path cost; `previous[v]` identifies the
vertex immediately before v on that path. Start every estimate at infinity,
every predecessor at -1, and source 0 at cost 0. Only discovered finite states
enter the queue. The minimum current estimate can become final because a path
through an unprocessed vertex cannot become cheaper using nonnegative edges.
Zero weights still satisfy that argument. A negative edge would invalidate it.

Implement the four tasks in `shortestPaths` without replacing the supplied
parser or path-output contract: initialize state, pop the cheapest queue entry,
discard a stale entry whose saved cost differs from the current estimate, and
relax edges with a strict comparison. Enqueue an improved cost and save its
predecessor together. Leave infinity and -1 unchanged for unreachable vertices.
Do not enqueue infinity, add a weight to an infinity sentinel, update on equal
cost, or rely on 32-bit integers for path totals. The maximum simple-path cost
under this practice contract is 1999 billion, which fits `long`.

The untouched starter deliberately reports unfinished work and produces no
answer. Reading a reference is a separate action from completing these tasks.

## Worked example and instructor walkthrough

The supplied graph has edges 0-1:10, 0-2:3, 2-1:4, 1-3:2, 2-3:9 and 3-4:0.
After processing source 0, the queue contains estimates 10 for vertex 1 and 3
for vertex 2. Predict the next vertex before popping it. Processing vertex 2
improves vertex 1 to 7 and discovers vertex 3 at 12. Processing vertex 1 improves
vertex 3 to 9. Vertex 3 discovers vertex 4 at 9 through the zero-weight edge. The old
entries for vertex 1 at 10 and vertex 3 at 12 are discarded when they are
later removed from the queue.

The expected sample output is:

```text
0 2 1 Distance: 7
0 2 Distance: 3
0 2 1 3 Distance: 9
0 2 1 3 4 Distance: 9
```

Independently, pause before each pop and relaxation to predict queue contents,
the distance array and any predecessor change. With an instructor, compare
those predictions before executing the next step. Then remove every edge from
source 0 and explain why the queue empties while other vertices remain
unreachable. This is the required project; the optional copy is a changed-case
retry of the same pack, rather than a second identical graded submission.

## Verification and complexity

Keep tests for a single vertex, no edges, disconnected components, duplicate
edges whose cheaper occurrence comes first, equal shortest paths, zero-weight
cycles, a stale queue entry and a three-edge billion-weight chain. The chain's
distance is 3000000000, beyond a signed 32-bit integer. Use Bellman-Ford on
small nonnegative graphs as an independent distance oracle, then check that
each returned predecessor route has no cycle and uses edges totaling that cost.
Do not require an arbitrarily chosen tie path when several paths are optimal.

For this multigraph, lazy queue operations take O((N+M) log(N+M)) time and
O(N+M) memory. Let P be the total size of all printed paths. Reconstructing
and preparing the output adds O(P) time and O(P) memory; a chain can make P
quadratic in N. Infinity values are never added to weights. The archived
matrix scan is not the active reference and must not be used to claim the
current queue complexity or disconnected-case correctness.

## Native Java workflow

Use an installed JDK 17 or newer. Copy one role into a separate working folder;
keep earlier attempts and the reference in different folders. From that role:

```sh
javac -encoding UTF-8 Main.java
java Main
```

Inspect `dijkstra.out`, change `dijkstra.in`, predict the new paths, and rerun.
The site IDE can be used for confirmed editing, saving and exporting when its
course import is enabled. Its Java teaching runtime does not execute this
file-I/O/priority-queue program; use the exported files with a native JDK.
Do not interpret a source preview or successful import as native execution.
No account, IDE plugin, network input, or live contest assistance is needed.
The pack's native verification command is
`python3 tests/verify-dijkstra-pack.py` from the source repository root.
