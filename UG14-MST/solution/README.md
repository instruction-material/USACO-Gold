# Solution role

Complete reference: trace and explain the tree before comparing a learner attempt.

# Minimum spanning trees with Prim

This required USACO Gold Unit 3 checkpoint is an authored algorithm demonstration.
It preserves the original example's undirected graph, source vertex 0, matrix
scan, `prim.in` and `prim.out`, and child-parent output. The historical program
is retained byte-for-byte under `legacy/`. These practice bounds and refusal
rules are explicit additions, not attributed historical contest limits.

## Prerequisites and input

Use arrays, graph edges, weighted paths and visited-state reasoning. A spanning
tree connects every vertex without a cycle. A minimum spanning tree minimizes
the sum of its selected edge weights; it need not give shortest paths from 0.

The first line of `prim.in` contains exactly `N M`. The next M lines each contain
`P Q W`, an undirected edge between zero-based vertices P and Q. The maintained
practice contract is `1 <= N <= 2000`, `0 <= M <= 200000`, and
`0 <= W <= 1000000000`. Parallel edges, self-loops and zero weights are allowed.
The matrix retains the cheapest parallel edge in either input order. Self-loops
cannot connect a new vertex and never become tree edges. Nonnegative weights are
a limit of this pack's input contract; Prim's cut argument also works with
negative weights in a representation that supports them.

A disconnected graph has no spanning tree and is refused. Invalid bounds,
endpoints, malformed or extra records and missing input are also refused.
These failures and the untouched starter leave an earlier `prim.out` unchanged.
They do not produce a new answer when none exists. An actual write failure can
still fail at the filesystem boundary; keep earlier saved attempts separately.

## Output and learner tasks

For a connected graph, `prim.out` contains N-1 lines in vertex order 1 through
N-1, each `vertex parent`, followed by `Total Distance: value`. The historical
label is retained, but the value is the total weight of the tree, not a path
distance. With N=1 there are no edge lines and the total is zero. Ties can have
different optimal trees. This reference selects the lowest-index unvisited
vertex when costs tie and changes a predecessor only for a strict improvement.

Implement four tasks in `minimumTree` while keeping the supplied input parser
and output validator:

1. Initialize the best connecting costs to infinity, parents to -1 and visited
   flags to false. Set vertex 0's cost to zero.
2. Select an unvisited vertex with the smallest connecting cost. Refuse the
   graph when no finite candidate exists; infinity cannot be added to the total.
3. Mark that vertex visited and add its selected edge cost using `long`.
4. For each unvisited neighbor with an edge, compare that edge's own weight
   against its best cost. On a strict improvement, update its cost and parent.

Return `new Result(previous, total)` after all vertices have been selected.
The supplied output validator checks real parent edges, a cycle-free route to
root 0 and agreement between the selected edges and total. It does not prove
minimality; the independent oracle checks supply that separate evidence.

## Trace and explain

The included sample uses edges 0-1:10, 0-2:3, 2-1:4, 1-3:2, 2-3:9, 3-4:0
and 0-4:20. After root 0, vertex 2 joins with cost 3. It offers vertex 1 an edge
of weight 4. That estimate is 4, rather than the cumulative path cost 7 used by
Dijkstra. Vertex 1 then joins, offering vertex 3 an edge of weight 2. Vertex 3
joins and offers vertex 4 an edge of weight 0. The total is 3+4+2+0 = 9.

```text
1 2
2 0
3 1
4 3
Total Distance: 9
```

Independently, pause before each selection and predict the visited set, costs,
parents and total. With an instructor, compare predictions at the same points.
Explain the cut between visited and unvisited vertices: choosing a cheapest
crossing edge preserves the possibility of an optimal tree. A chosen edge adds
one new vertex, so it cannot make a cycle. Remove all edges touching vertex 0
and explain the refusal before opening the output. Compare the three-vertex
graph 0-1:10, 0-2:6, 1-2:5 with shortest-path reasoning: its MST total is 11,
even though its path from 0 to 1 costs 11 rather than the direct path cost 10.

## Verification and limits

Test N=1, disconnected vertices, a cycle, equal-cost alternatives, zero weights,
self-loops and parallel weights 1 then 9, followed by their reversed order.
A four-vertex billion-weight chain totals 3000000000; an `int` cannot hold it.
The maximum tree total for this contract is 1999000000000, which fits `long`.
Verify N-1 real edges, connectivity, acyclicity, edge-weight sum and minimality.
Compare with independent Kruskal/union-find on small graphs, and enumerate every
spanning tree on tiny graphs. Do not require one arbitrary tie tree.

The matrix version takes O(N squared + M) time including input and output
validation, and O(N squared) memory. An adjacency-list/heap implementation is a
separate extension; changing the data structure should follow a measured need.
This required checkpoint is one authored demonstration, not a second generic
studio exercise or an invented official contest problem.

## Native workflow

Use JDK 17 or newer. Copy one role to a separate folder, keeping the learner
attempt and complete reference separate. From that folder run:

```sh
javac -encoding UTF-8 Main.java
java Main
```

Inspect `prim.out`, change `prim.in`, predict the new result and rerun. The
untouched starter reports unfinished work rather than supplying an answer.
Until a confirmed site import is enabled, use the source role directly.
An editor import, source preview or ZIP download is not native execution.
This matrix/file-I/O program requires a native JDK rather than the website's
Java teaching preview. No account or network input is required. From the source
repository root, run `python3 tests/verify-mst-pack.py` for independent native
checks on both roles and the preserved historical examples.
