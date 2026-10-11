# Shortcut: traffic on a shortest-path tree

This optional Gold application follows weighted shortest paths and tree rooting.
The learner receives a shortest-route helper so the new work is selecting the
route tree, aggregating cow traffic and comparing shortcut savings. Preserve an
earlier attempt and change the cases when revisiting this pack. The project can
be completed independently or paused at each prediction with a course facilitator.

## Contract

The [January 2019 Gold problem](https://usaco.org/index.php?page=viewproblem2&cpid=899)
uses a connected undirected graph with the barn at field 1. Every cow follows
its shortest usual route toward the barn. Tied routes use the smaller field
label at their first differing position, read from the cow's field toward the
barn. Add one trail of length T from a chosen field to the barn. A cow uses it
only if its usual route visits that field and the trail shortens the remaining
trip. Cows do not reroute to reach the new trail.

`shortcut.in` contains:

| Record | Meaning and bounds |
| --- | --- |
| `N M T` | 1..10000 fields, N-1..50000 trails, T in 1..10000 |
| N cow counts | Each count is in 0..10000, in field-label order |
| M records `a b time` | Endpoints in 1..N; positive time in 1..25000 |

Every field must reach the barn. The statement does not exclude parallel trails
or positive self-loops; the learner driver accepts them. N=1 and M=0 is valid.
`shortcut.out` contains one integer: the greatest reduction in total travel time.
Use `long` for total traffic and savings; field labels become zero-based indices.

## Prediction and model

Before coding, draw every chosen route on the included sample. Field 4 chooses
4,2,1 over 4,3,1 when both take 8 time units. Field 5 chooses 5,3,1 over 5,4,2,1
when both take 10. A shortcut at field 5 saves 8 units for each of its five cows,
so the answer is 40. The four cows at field 4 keep their usual route even though
travelling through field 5 might become faster. The original total is 101; this
shortcut changes it to 61.

For a field v, choose the lowest-labelled neighbour that can begin a shortest
route toward the barn. This gives the first differing step in the lexicographic
comparison. Its suffix is selected by the same rule. Positive trail times make
distances strictly decrease along parent links, so the selected routes form a
tree rooted at the barn.

Traffic through v is its own cows plus the traffic through each child. Process
children before their parent. Cows in this subtree share the selected suffix
from v to the barn; cows outside it never encounter a shortcut at v. Evaluate
`gain(v) = traffic(v) * max(0, distance[v] - T)` for every field and retain the
greatest total, including zero when no shortcut helps.

## Four learner tasks

1. Call the supplied `shortestRoutes` helper, construct child lists and explain
   the direction of the tie rule. Retain the helper's distances and parents.
2. Accumulate traffic in `long` totals using an iterative postorder. A chain can
   contain 10000 fields; avoid depending on the default Java call-stack depth.
3. Evaluate savings for cows that encounter each candidate on their existing
   route. Use `long` before multiplication.
4. Return the greatest nonnegative total and explain ties and no-benefit cases.

The starter's `solve` remains unfinished. Untouched valid runs exit with status
2 and create no answer. Refused or unfinished work preserves an earlier answer
file. The numeric output guard is a range check, not a grader of learner logic.

## Independent checks and cost

Test a single barn, no cows, a long shortcut, a tied diamond, a changed cow
distribution, a reversed trail record, parallel trails and positive loops.
For graphs of at most eight fields, enumerate simple routes to the barn,
choose the minimum `(time, field-label sequence)`, and simulate which cows
encounter each shortcut. Compare selected parents, traffic and total saving.
Keep usual routes fixed when adding the trail. Save two custom cases and retry
later from an empty file. Exercise full teaching bounds separately.

The supplied lazy queue helper scans each adjacency list only for its current
distance, with O((N+M) log(M+1)) time and O(N+M) storage. An iterative tree
aggregation and candidate sweep add O(N) time and storage. Sorting fields by
descending distance is another valid order, adding O(N log N) time. Explain why
children have larger distances than their parent.

The historical reference traces every origin's parent path separately, costing
the sum of path depths, up to O(N²). It also scans adjacency for every queue
removal, including stale and tied entries. Its queue cost depends on those
removals and scanned degrees. Checked full-size cases are evidence for those
cases; they are not a formal judge-runtime guarantee.

## Native workflow and comparison

Begin with the separate [learner role](starter/README.md). Retain its source,
predictions and changed cases before opening the [reference role](solution/README.md).
Each role includes its own contract and commands and can be exported alone.
Use a native JDK 17 or newer with Main.java and shortcut.in in the same folder:

```text
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
```

These commands also work in PowerShell. Check the exit status before reading
shortcut.out with `cat shortcut.out` or `Get-Content shortcut.out`. An old answer
does not prove a successful new run. Keep source and inputs alongside the ZIP.
The site IDE saves and exports native Java packs; its browser preview does not
execute this file-I/O application. Site imports require separate acceptance.

The reference's six changed lines replace generic-array adjacency storage with
typed lists. Its route and traffic algorithms are preserved. Exact original
bytes remain under `legacy/`, which is excluded from role imports. Dedicated
native acceptance checks references and supplied drivers; it does not grade
completed learner submissions. Protected mocks and live contests begin from an
empty file without these practice starters or references.
