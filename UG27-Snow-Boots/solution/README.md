# Snow Boots preserved reference

This `Main.java` is the original migrated reference, preserved without
algorithm edits. Compare it only after retaining a learner attempt. It assumes
valid input in the advertised line layout and does not share the learner
driver's explicit refusal guarantees.

## Prerequisites and input

Use this optional practice after sorting and offline ordering. For each boot,
decide whether its depth limit and maximum forward step can connect the two
ends of a tiled path. Read N B, then N depths, then B depth/step pairs from
`snowboots.in`; write one 0 or 1 per boot, in original order, to `snowboots.out`.
N and B are at most 100000; depths are 0..1000000000, both endpoints have depth
zero, and each step is 1..N-1. The official header permits N=1, but B>=1 and
the step bounds have no valid boot in that case; the joint valid-input domain
therefore has N>=2. This is a derived constraint, not a changed problem limit.

Problem contract: [USACO February 2018 Gold Snow Boots](https://usaco.org/index.php?page=viewproblem2&cpid=813).

## Trace and explain

The sample depths are 0,3,8,5,6,9,0,0. A depth-zero boot can land only at
indices 0,6,7, whose widest gap is 6. Step 5 fails and step 6 succeeds.
At depth limit 6 the surviving indices are 0,1,3,4,6,7, with widest gap 2,
so step 2 succeeds. At limit 8 the deepest interior tile is removed,
creating a gap of 2, so step 1 fails. The sample answer file contains:

```text
0
1
1
0
1
1
1
```

Process boots by decreasing depth limit. Remove every tile that is strictly
too deep before answering a boot. Equal-depth tiles remain usable. Arrays
of previous/next surviving positions form a linked path; removing an interior
tile joins its surviving neighbors. The distance between those neighbors
updates the widest gap. A boot succeeds exactly when its maximum step can
span that gap. Keep original boot indices so processing order does not
become answer order. In a shared walkthrough, predict each removal, gap
update and restored answer before continuing.

## Native workflow

Keep `Main.java`, `README.md` and `sample.in` together after saving and
exporting the role. Use JDK 17 or newer in the extracted folder:

```sh
cp sample.in snowboots.in
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
cat snowboots.out
```

In PowerShell, use `Copy-Item sample.in snowboots.in` and
`Get-Content snowboots.out`. Native input comes from the named file.
The site IDE is used to edit, save and export this native project; its Java
teaching preview is not the acceptance gate for this algorithm. Follow the
pack's native commands when its confirmed import becomes available.

## Verify and explain

For tiny paths, independently mark reachable tiles for each boot: move only
forward by a distance at most its step, landing only on allowed depths.
Compare last-tile reachability with the offline gap sweep. Include two
endpoints, all-zero depths, a deep interior tile, equal depths, a gap exactly
equal to the step, a step one short, zero boot depth, repeated boots and
reordered boot records. Permuting boots must permute answers consistently.
Check why the endpoints never disappear, why the removal cursor remains
in bounds and why widening gaps cannot shrink after further removals.

Sorting and processing take O(N log N + B log B) time and O(N+B) storage.
The tiny reachability checker is independent and is not a full-limit
performance solution. Save predictions and an altered case, explain one
corrected mismatch, then retry later without copying the first attempt.

These source checks validate the supplied roles and driver. They do not
grade a student's completed algorithm. Protected contest work begins from
an empty file without these practice references.

On a successful valid run, read the named answer file. The original Snow Boots reference also
prints widest-gap diagnostics to the terminal, one per processed boot.
These are not the 0/1 answers and follow processing order. Use `snowboots.out`
for answers in original boot order.
