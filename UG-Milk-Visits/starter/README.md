# Milk Visits learner role

Complete the four marked tasks in `solve`; the file driver is supplied.

# Milk Visits: offline tree-path queries

Optional applied practice after Gold tree rooting and Euler-tour ancestry.
This is USACO 2019 December **Gold**, problem 2, not the two-type Silver
version. Its purpose is to combine ancestor intervals with state that follows
the current root-to-farm path, rather than repeat a dynamic-programming unit.

## Contract

[Official problem](https://usaco.org/index.php?page=viewproblem2&cpid=970).
Read `milkvisits.in` from the current role directory: `N M`, then one line
with N cow types, then N-1 undirected tree edges, then M queries `A B C`.
Official bounds are `1 <= N, M <= 100000`; all farm IDs, cow types and query
types lie in `1..N`. The edges form a connected tree. Query endpoints may
coincide. The driver converts IDs and types to zero-based indices internally.

Write `milkvisits.out` as exactly M bits in query order, followed by a newline.
Bit i is 1 when at least one farm on the **inclusive** A-to-B path has type C,
otherwise 0. There are no spaces between bits. Successful runs do not print
the answer to standard output. The two official sample answers are `10110`
and `0110`.

## Independent work or a shared walkthrough

Use the starter first. Draw a rooted tree with two branches, label entry and
exit times, and list the active path before coding. Keep the first prediction
and attempt before opening the separate reference. A walkthrough uses the
same checkpoints, with pauses to predict what enters and leaves each stack.

Complete the four marked tasks in `solve`:

1. Generate pre/post times with explicit traversal frames. Under the reference
   convention, u is an ancestor of v, including itself, when
   `pre[u] <= pre[v] && post[u] >= post[v]`.
2. Attach each query to both endpoints. During the second traversal, maintain
   the current root path, vertex depths and a stack of active farms per type.
3. At endpoint x, find the last active farm p of the desired type. If p=x,
   that query is true. Otherwise let w be the child immediately after p on
   the active path toward x. When the other endpoint lies outside w's subtree,
   its path to x passes through p, so mark the query true. Retain true answers
   when processing the second endpoint. When both endpoint checks are false,
   explain why neither side of the path to their lowest common ancestor
   contains the desired type. No explicit LCA computation is required.
4. Pop x from both the path and its type stack on exit. Explain why retaining
   a farm from a completed sibling branch creates a false positive.

For the first sample, the 1-to-4 path is 1,2,4: its types are all 1. The
5-to-5 query contains only farm 5, whose type is 2. For the second sample,
4-to-6 goes through 4,3,2,5,6; type 1 exists in the tree but is absent on this
path. Trace that case to distinguish an ancestor from a farm on the query path.

## Native build and run

Use JDK 17 or newer, with `milkvisits.in` beside `Main.java`. From the extracted
starter or reference directory:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
```

These commands also work in PowerShell. After a successful run, read the
answer with `cat milkvisits.out` or `Get-Content milkvisits.out`. Check the exit
status first. The untouched starter exits 2 and preserves an earlier answer;
that old answer does not demonstrate a successful new run. The starter checks
the input record counts, bounds and tree connectivity before writing. It
checks result length, not whether a completed learner algorithm is correct.
The historical reference expects valid contract input.

The site IDE is for editing, saving and exporting Java. Its preview does not
execute this file-based program; the browser Input panel does not replace
`milkvisits.in`. Starter and reference use separate saved projects. Protected
mock sets and active contests start from an empty file without these packs.

## Test, explain and compare

Try one farm, identical endpoints, an absent type, a matching endpoint, a
matching lowest common ancestor, repeated types, a star and a chain. Build an
independent small-tree oracle by finding the path with BFS and examining its
types. This checks a different algorithm from the reference's ancestor test.
At full scale, use a 100000-farm chain with unique types and 100000 queries:
for numbered farm types, query A B C is true exactly when C lies between A
and B. Do not increase the JVM stack to hide a recursive traversal defect.

Each edge is visited a constant number of times and each query is inspected
at its endpoints: expected O(N+M) time with the reference's hash-based visited
sets, O(N+M) memory. Explicit frames may occupy O(N) heap space on a chain.
Contrast this with O(NM) independent path searches. Record a state trace, an
explanation of both endpoint checks, source changes and two changed cases;
then rewrite the algorithm from an empty file in a later session.

The reference changes only the two recursive traversal bodies to explicit
enter/exit frames. [the original source](https://github.com/instruction-material/USACO-Gold/blob/main/UG-Milk-Visits/legacy/Main.java) preserves the original bytes. The query
algorithm and its data structures remain the historical implementation.
