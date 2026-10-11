# Shortcut reference: route choices and traffic comparison

Use this optional application after weighted shortest paths and tree rooting.
Retain a learner attempt, route predictions and two changed cases before
comparing this reference. The same trace can be discussed with a course
facilitator or followed independently.

## Full input and output contract

Field 1 is the barn in a connected undirected graph. Each cow follows a shortest
usual route toward the barn. Equal-time routes prefer the smaller field label
at the first differing step, reading toward the barn. Add one trail of length T
from a chosen field to the barn. A cow takes it only if its existing route visits
that field and its remaining trip becomes shorter. Other cows do not reroute.

`shortcut.in` begins with `N M T`: N in 1..10000, M in N-1..50000 and T in
1..10000. The next line contains N cow counts in 0..10000. The next M lines
contain `a b time`, with endpoints in 1..N and times in 1..25000. All fields
must reach the barn. Parallel trails and positive loops are not excluded by
the statement; N=1, M=0 is valid. `shortcut.out` contains the maximum reduction
in total travel time. Use `long` totals; program field indices start at zero.

The sample answer is 40. Field 4 uses 4,2,1 rather than the tied 4,3,1 route;
field 5 uses 5,3,1 rather than 5,4,2,1. Only the five cows starting at field 5
encounter a shortcut placed there. Each saves 8 units. The original total of
101 becomes 61. Cows starting at field 4 do not change their usual route to
seek the new trail.

## Compare the model

For a field v, a lower-labelled valid next step determines the first difference
in the toward-barn lexicographic comparison. The selected suffix uses the same
rule. Positive weights make each parent strictly closer to the barn, creating
a rooted tree. Trace parent choices rather than comparing routes outward from
the barn.

The reference walks each origin's entire chosen parent path and adds that
origin's cows to every field encountered. For each candidate, it evaluates
`traffic[v] * max(0, distance[v] - T)` and retains the greatest total. Explain
why cows outside that subtree cannot use the new trail. Compare its repeated
path counting with an iterative subtree aggregation in the learner attempt.
Both must respect the same selected usual routes.

Check a single barn, no cows, a slow shortcut, equal shortest routes, changed cow
counts, reversed trail records, parallel trails and positive loops. On a tiny
graph, enumerate simple paths, choose the least `(time, field-label sequence)`
and simulate shortcut encounters without rerouting. Compare parents, traffic
and answers with the learner attempt. Separate small oracles from full-bound
cases and repeat later from an empty file.

The historical traffic loop costs the sum of all path depths, at most O(N²).
Its queue scans adjacency for each removal, including stale and tied entries;
queue cost depends on those removals and scanned degrees. The supplied learner
helper skips stale entries, and iterative tree aggregation avoids repeated
path walks. Passing the checked 10000-field and 50000-trail cases does not
constitute a formal judge-runtime guarantee.

## Native workflow and provenance

Keep Main.java, README.md and shortcut.in in one folder. The included
shortcut.out records the expected sample answer, not proof of a new run.
Use a native JDK 17 or newer:

```text
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
```

These commands also work in PowerShell. Check the exit status before reading
shortcut.out with `cat shortcut.out` or `Get-Content shortcut.out`. Save source
and custom inputs with the exported ZIP. The site IDE edits, saves and exports
this native file-I/O application; its browser preview does not run it or replace
shortcut.in.

The six reference edits replace generic-array adjacency storage with typed
lists so strict compilation succeeds. Route and traffic algorithms are
preserved; exact original bytes are archived outside this role under `legacy/`.
This historical reference assumes valid contract input. Refused-input and
unfinished-answer preservation checks apply to the separate learner driver.
Dedicated source checks do not grade completed learner submissions. Protected
mocks and live contests start from an empty file without practice packs.
