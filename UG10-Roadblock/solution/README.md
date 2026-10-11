# Roadblock instructor reference

This role preserves the historical reference program and original sample input.
The maintained source has not been rewritten to resemble the learner helper.
Use it to compare a completed sensitivity exercise after the core shortest-path
lesson. Roadblock's historical origin is February 2014 Silver, while this course
uses it as optional Gold weighted-graph application.

The [shared guide](../README.md) gives the official contract, workflow, sample,
learner tasks and independent test suggestions. This reference reads `rblock.in`
and writes the maximum increase to `rblock.out`. It expects valid problem input;
the learner role adds checked input and unfinished-work refusal.

## Input and answer contract

This exported folder includes the full contract. Read `N M`, then exactly M
records `A B length`, from `rblock.in`: 1..250 fields, 1..25000 roads, endpoints
in 1..N and lengths in 1..1000000. Roads are undirected, each undirected pair
appears only once, and every field is reachable. Travel from field 1 to field N.
Double exactly one road and write the greatest increase over the unchanged
optimum as one integer in `rblock.out`, not the changed route's total length.
Positive self-loops and coincident endpoints are accepted boundary cases in
the learner driver. A positive loop cannot improve a route, and coincident
endpoints have an empty route with distance zero.

Keep earlier source, inputs and answers before changing a case. Check the
native exit status before reading an answer. This historical reference expects
valid contract input; the learner's input and numeric range guards are not a
correctness grade for an implemented algorithm.

From this directory, with JDK 17 or 21:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
cat rblock.out
```

The included sample produces 2. Its baseline route 1,3,4,5 costs 6; changing
road 3,4 makes the best route 1,3,5 cost 8. The original sample input is kept
unchanged, including its file layout. The sample output is supplied alongside it.
Keep any confirmed reference IDE import separate from the saved learner attempt.
Use native compilation after export; the Java Input preview is not this file
program's input source.

## Reasoning and comparison

`dijkstra` fills target distances and predecessor fields in the original matrix.
The program copies one baseline path before later calls replace `prev`. It
doubles a path road in both directions, reruns the shortest-path computation,
retains the largest resulting distance, restores the road and finally subtracts
the unchanged baseline.

Ask for the candidate-road proof before tracing the loop. If a road is outside
one selected optimal path, that path survives at its old cost after the change.
Increasing a positive edge cannot reduce the optimum, so such a road cannot
increase it. The argument remains valid when several optimal routes tie.
Testing a path road can still give increase zero when another optimum survives.

Check that every trial changes exactly one road, both directions agree, all
trials use the same baseline, and original weights are restored before the next
iteration. Positive weights make the chosen predecessor path simple, with at
most N-1 roads. A positive self-loop cannot improve a route; coincident endpoints
give distance and increase zero. Neither case needs an invented input ban.

The learner's supplied dense helper costs O(N²) per run, giving O(N³) overall
and O(N²) storage. This preserved reference instead scans a matrix row for each
priority-queue removal and retains stale queue entries. If one run removes Q
entries, its scan/queue cost is bounded by O(QN + Q log(Q+1)), in addition to
initialization. Apply that bound separately to its repeated runs; do not label
the original as the optimized dense helper. Measured full-size cases are test
evidence, not a formal judge-runtime guarantee.

For independent verification, use a tiny all-road perturbation oracle and a
different distance method. Check the official sample, a single road, tied routes,
a bridge, replacement routes, successive restoration trials and numeric bounds.
The dedicated native gate also checks dense 250-field/25000-road fixtures,
warning-free compilation, the supplied learner helper, refused inputs and saved
answers. It does not complete or grade the learner algorithm.

After discussion, close this role and retry on a new graph. Compare the path
proof, restored state and independent evidence, rather than source similarity.
