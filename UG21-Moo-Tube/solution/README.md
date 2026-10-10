# MooTube preserved reference

Compare this completed reference after retaining a learner attempt. Its
`Main.java` remains the original migrated source, with no algorithm edits.
Discuss each difference in reasoning instead of copying the whole file.

## Prerequisites and input

Use this optional Gold practice after weighted disjoint sets and sorting. For
each video and threshold, count other videos reachable using only edges with
relevance at least that threshold. The supplied graph is a tree. Exclude the
starting video and preserve the original query order.

The native input is `mootube.in`. Its first line has `N Q`, with both between
1 and 100000. The next N-1 lines have one-based `p q relevance`; the last Q
lines have `threshold video`. Relevance and thresholds are between 1 and
1000000000. The tree guarantee is a problem precondition; the learner driver
checks line counts, token counts and scalar bounds, but does not prove it is a
tree. Internal video indices are zero-based. Write Q integer answers, one per
line, to `mootube.out`. Answers are between 0 and N-1 and fit in Java `int`.
These are the Gold problem limits, rather than the smaller Silver version.

Problem source: [USACO January 2018 Gold MooTube](https://usaco.org/index.php?page=viewproblem2&cpid=789).

## Trace and explain

The supplied four-video sample has edges 1-2 of weight 3, 2-3 of weight 2 and
2-4 of weight 4. Before running, predict each query: `(1,2)` gives 3, `(4,1)`
gives 0 and `(3,1)` gives 2. The expected answer file contains:

```text
3
0
2
```

Process thresholds 4, 3 and 1 in descending order. At 4 only edge 2-4 is
active, leaving video 1 alone. At 3 edge 1-2 joins that component, whose size
is now 3. At 1 all videos are joined. Explain why every edge at a threshold
must be added before answering an equal-threshold query, and why subtracting
one excludes the starting video. Store answers by their original query index.

## Native workflow

Use a JDK 17 or newer. Keep `Main.java`, this guide and `sample.in` together
after exporting this role from the site IDE. Save the learner attempt first.
Create `mootube.in` from the sample, then compile and execute from this folder:

```sh
cp sample.in mootube.in
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
cat mootube.out
```

In PowerShell, use `Copy-Item sample.in mootube.in` and
`Get-Content mootube.out` for the first and last commands. Input comes from
the named file, not a terminal prompt or the browser Input panel. The site
IDE saves and exports this native project; its Run action shows directions
rather than executing the Gold algorithm in a browser preview.

## Verify and explain

For tiny trees, independently traverse from each queried video using only
qualifying edges and count reached videos minus one. Compare that result to
the offline sweep. Include N=1, no eligible edges, equal weights and
thresholds, repeated queries, a star, a chain and mixed query order. Change
one edge weight or threshold, predict which answers change, then rerun.

Weighted union without path compression gives O(log N) root operations.
Sorting plus the sweep costs O(N log N + Q log Q + (N+Q) log N), with
O(N+Q) memory. The preserved reference has weighted union without path
compression; do not label it as a compressed DSU. Rebuilding reachability
for every query is useful as a tiny oracle but costs O(NQ) at the full limits.
Explain the active-edge invariant, the component-size invariant and the
reason the output ordering differs from the processing ordering.

This historical reference assumes valid contest input. It does not share
the learner driver's explicit input-refusal behavior. On a successful valid
run it writes the answer file and produces no terminal answer. Record
each test input separately before generating its output.
