# Roadblock: shortest-path sensitivity

This optional application follows the core weighted-graph lesson. A shortest-path
routine is supplied in the learner role so the new work is about choosing useful
experiments, explaining why they suffice, and restoring each changed road.
Roadblock was a February 2014 Silver problem; its role here is additional Gold
graph practice. It does not replace the core shortest-path implementation project.

The [official problem](https://usaco.org/index.php?page=viewproblem2&cpid=398)
defines a connected undirected network. Travel starts at field 1 and ends at
field N. Double exactly one road and maximize the increase in the best route's
length. Return that increase, rather than the new route length.

## Contract and model

`rblock.in` begins with `N M`, followed by M records `A B length`.
Use 1..250 fields, 1..25000 roads, endpoints in 1..N and lengths in
1..1000000. An undirected pair has only one road, and every field is reachable.
`rblock.out` contains one integer: the greatest increase over the unchanged
network. Field labels become zero-based array indices inside the program.

The learner driver checks these records before calling `solve`. It also accepts
positive self-loops and coincident start/end fields, which the statement does
not explicitly exclude. A positive loop cannot improve a shortest route; when
start and end coincide, the empty route has length zero. These boundary cases
still require completing the learner work, rather than bypassing its refusal.

Both roles use a matrix: `lengths[a][b]` and `lengths[b][a]` describe the same
road, and -1 means no road. Save a chosen baseline path before running a trial:
a later shortest-path computation may produce a different predecessor path.

## Roles and native workflow

- [Learner role](starter/README.md): checked file driver, supplied dense
  shortest-path helper, and four unfinished sensitivity tasks.
- [Instructor reference](solution/README.md): the preserved historical program,
  sample answer, invariants and questions for comparing implementations.

Use JDK 17 or 21. From one role's directory:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
cat rblock.out
```

Keep `Main.java` and `rblock.in` in the same working directory. This is a native
file-I/O project; the Java Input preview is not its input source. Compile and run
locally, or export the imported role as a ZIP and use the same commands. Confirm
an IDE import when the site offers it, work in the learner role first, and keep
the reference in its separate saved workspace. Source-pack availability alone
does not establish that the site import has been accepted yet.

An untouched learner exits with status 2 and a task message. It does not create
an answer or overwrite an earlier one. A completed learner writes only after
the input and returned numeric range have been checked; that range check is
not a correctness grade. The historical reference expects valid contract input.

## Predict, trace, implement, verify

For the included sample, trace the baseline route 1,3,4,5: its length is 6.
Doubling road 3,4 changes the best route to 1,3,5 of length 8, so the increase
is 2. Doubling a road on a tied best route might cause no increase at all.

Before coding, draw the chosen path and explain why an unchanged path rules out
every road outside it. Then complete the four marked tasks in `solve`: retain
the baseline path, select its roads, compute each single-road change, and restore
the original matrix before another trial. Make a table with the road, old weight,
trial distance, increase and restored weight. Work through it independently or
pause at each column with an instructor.

Verify a single connecting road, equal alternate routes, a bridge, a replacement
route, reversed endpoint records, positive loops and coincident endpoints.
For tiny graphs, use an independent check that doubles every input road and
recomputes distances, even roads outside the selected path. Compare the maximum
increase. Include two successive trials that would expose leaked modifications.

The supplied dense helper uses O(N²) time per call and O(N²) matrix storage.
One baseline and at most N-1 path-road trials give O(N³) time overall. Explain
the bound using positive weights and a simple chosen path. The historical
reference uses a priority queue and may rescan stale entries; do not assume it
has the supplied helper's operation bound. Its separate guide explains that
comparison.

Completion means correct contract output, the candidate-path proof including
ties, isolated and restored trials, independent test evidence, and an explained
cost bound. Save a fresh graph for a delayed retry before opening the reference.
