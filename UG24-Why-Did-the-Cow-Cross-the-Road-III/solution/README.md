# CircleCross preserved reference

This `Main.java` is the original migrated reference, preserved without
algorithm edits. Compare it only after retaining a learner attempt. It assumes
valid input in the advertised line layout and does not share the learner
driver's explicit refusal guarantees.

## Prerequisites and input

Use this optional practice after Fenwick point updates, prefix sums and sorting.
Count pairs of chords whose endpoints alternate around a circle. Labels 1..N
each occur twice. Read N (1..50000), then one label on each of the next 2N lines
from `circlecross.in`; write the crossing count to `circlecross.out`.

Problem contract: [USACO February 2017 Gold CircleCross](https://usaco.org/index.php?page=viewproblem2&cpid=719).

## Trace and explain

For the included sample, the sequence is 3, 2, 4, 4, 1, 3, 2, 1. Zero-based
intervals are cow 3: [0,5], cow 2: [1,6], cow 4: [2,3] and cow 1: [4,7].
The crossing pairs are (3,2), (3,1) and (2,1), so the answer is 3. The short
cow-4 interval is nested and crosses none of those paths. Predict this before
running. Adjacent endpoints 1,1,2,2 give zero; nesting 1,2,2,1 also gives zero;
alternation 1,2,1,2 gives one. Check these distinct cases independently.

Pair first and second positions, then process by increasing first position.
Before processing a cow, the Fenwick tree marks only previously processed
cows' exits. A marked exit strictly inside the current interval identifies
an alternating pair. Count these exits and mark the current exit afterward.
All endpoints are distinct, so inclusive `prefix(exit) - prefix(entry)`
counts the same interior range here. Explain why nested and disjoint pairs
contribute nothing, and why each crossing is counted once. In a shared
walkthrough, pause at the same interval, prefix and update predictions.

## Native workflow

Keep `Main.java`, `README.md` and `sample.in` together after saving and
exporting the role. Use JDK 17 or newer in the extracted folder:

```sh
cp sample.in circlecross.in
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
cat circlecross.out
```

In PowerShell, use `Copy-Item sample.in circlecross.in` and
`Get-Content circlecross.out`. Native input comes from the named file.
The site IDE is used to edit, save and export this native project; its Java
teaching preview is not the acceptance gate for this algorithm. Follow the
pack's native commands when its confirmed import becomes available.

## Verify and explain

Build an independent tiny checker: for each unordered pair, count whether
one cow's first endpoint lies inside the other's interval and its second
lies outside. Compare it with the Fenwick sweep. Include a single cow,
adjacent and nested pairs, all pairs alternating, mixed labels and a cyclic
rotation of the sequence. Change a sequence, predict the changed pairs and
retain both attempts. Reversing or rotating the circular order preserves
crossings; arbitrary relabeling also preserves the answer.

The sweep and sorting take O(N log N) time and O(N) storage. A pairwise
checker takes O(N squared), so use it only for tiny cases. At N=50000, the
maximum is N(N-1)/2 = 1249975000, which fits Java int; the learner driver
uses long arithmetic for its bound and accumulated answer. Do not claim
that the original reference requires long for these published limits.

These source checks validate the supplied roles and driver. They do not
grade a student's completed algorithm. Protected contest work begins from
an empty file without these practice references.

On a successful valid run, read the named answer file. The terminal is silent.
