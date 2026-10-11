# Roadblock learner: isolate one road experiment

This optional task follows the core weighted-graph implementation lesson.
The file driver and a correct dense shortest-path helper are supplied. The
unfinished work in `solve` is shortest-path sensitivity, with special attention
to preserving the baseline and restoring each changed weight.

Read the [shared contract and sample](../README.md) before starting. Input comes
from `rblock.in` in this directory, and successful output goes to `rblock.out`.
The answer is the maximum increase, not the new total distance. `Problem.lengths`
stores the undirected matrix; `Problem.roads` retains the original records.
`ShortestPath` contains the current target distance and a new predecessor array.
Absent roads are -1, and input labels become zero-based indices.

## Input and answer contract

This folder is self-contained after export. Roadblock originated in February
2014 Silver and is used here as optional Gold practice after core weighted graphs.
Read `N M`, then exactly M records `A B length`, from `rblock.in`. There are
1..250 fields and 1..25000 roads; endpoints are in 1..N and lengths in
1..1000000. Roads are undirected, each undirected pair appears only once,
and every field is reachable. Travel from field 1 to field N. Double exactly
one road and write the greatest increase over the unchanged optimum as one
integer in `rblock.out`, not the changed route's total length.

The supplied driver accepts positive self-loops and coincident endpoints;
neither is explicitly excluded by the statement. A loop cannot improve a
shortest route, and coincident endpoints use the empty route of length zero.
Invalid or unfinished work exits with status 2 before opening the answer file.
Check the exit status before reading an earlier answer.

## Four learner tasks

1. Find the unchanged target distance with `shortestPath`. Follow its predecessor
   chain to preserve one chosen path before performing any trial. Handle a
   zero-road path when the endpoints coincide.
2. Select only the roads on that path. Explain the restriction: increasing a
   weight outside the path leaves an original optimal route available, while
   increasing a positive weight cannot make the optimum smaller. This argument
   includes ties; it does not require one unique shortest route.
3. For each selected road, double its old weight in both matrix directions,
   obtain the new shortest distance, and compare its increase with the best
   increase so far. Every comparison uses the original baseline.
4. Restore the old weight before another experiment. Use an exception-safe
   restoration boundary such as `try/finally`, and explain why modifying both
   directions or restoring with a remembered value matters.

Remove the refusal only after these tasks are implemented. Do not replace it
with the sample answer, a placeholder zero, or access to the reference role.
An untouched run deliberately exits with status 2 and preserves an earlier
answer. Invalid input and out-of-range returned values also fail before the
answer file is opened. A numerically plausible answer still needs algorithm tests.

## Run and check

Use JDK 17 or 21 from this directory, or export the learner workspace and run:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
cat rblock.out
```

Use the supplied input file. The Java Input preview does not feed this program.
Confirmed IDE imports must preserve learner and reference work separately.

The sample baseline is 6. Doubling road 3,4 gives a new optimum of 8 and increase
2. Predict the result before each run. Draw a two-route tie to see why doubling
a chosen-path road can yield increase zero. Draw a bridge to produce a positive
increase. Add a cheaper replacement path to test why the best route can change.

For a tiny independent oracle, double each input road in turn and use repeated
edge relaxation or Floyd-Warshall to recompute the best distance. Restore after
every trial and compare the maximum increase with your result. Keep the oracle
limited to small graphs so its cost does not masquerade as a full-bound solver.
Also test successive trials, maximum road lengths, reversed road records,
positive loops and coincident endpoints. The supplied driver accepts the last
two cases rather than inventing an additional statement restriction.

Trace the old weight, temporary symmetric entries, new route, delta and restored
entries. Show that the saved baseline path remains intact after later helper
calls. Then explain O(N²) time per dense helper call, at most N calls total, and
O(N²) storage. These checkpoints support an independent attempt or a guided
walk-through; the instructor can ask for predictions before each trial.

Finish with a small original graph and a delayed retry. Open the separate
reference only when comparing a completed attempt, its path proof and its tests.
