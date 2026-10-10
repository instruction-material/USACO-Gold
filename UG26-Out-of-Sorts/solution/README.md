# Out of Sorts, Gold bidirectional sweeps: reference pack

## Prerequisites and input

This optional Gold ordering practice follows sorting and Fenwick point updates/prefix sums. It reinforces a diagnosed gap or provides a changed-case retry; it is not an additional prerequisite for the required course spine. If already completed in the core unit, preserve that attempt and change the cases.

This is the Gold modified bubble algorithm: each iteration prints moo, makes one forward adjacent-swap sweep, then one backward sweep, then checks adjacent pairs for sortedness. It runs at least once. Read N (1..100000), then N values, one per line, from sort.in; values are 0..1000000000 and duplicates are allowed. Write the iteration count to sort.out.

Problem contract: [USACO Out of Sorts, Gold bidirectional sweeps](https://usaco.org/index.php?page=viewproblem2&cpid=837).

## Trace and explain

Track original positions while ordering values stably. Equal values retain their original order, since the simulated algorithm swaps only a strictly inverted pair. After marking the original positions of the smallest k ordered values, query how many marks lie in the first k original positions. Their difference is the number of desired left-side values still on the right of this cut. The maximum cut requirement, with a minimum of one iteration, gives the number of complete forward/backward sweeps. Explain both directions and why this is a cut count, not maximum single-element displacement.

The sample sorted positions are 0,4,3,2,1; the cut requirements are 0,1,2,1, so the answer is 2. A direct first iteration changes [1,8,5,3,2] to [1,5,3,2,8] in the forward sweep and [1,2,5,3,8] in the backward sweep. The second iteration sorts it. A sorted row, all equal values, or one element still prints moo once.

The supplied sample answer is:

```text
2
```

## Marked learner tasks

1. Pair each value with its original position and retain stable order for ties.
2. Implement Fenwick position updates.
3. Implement inclusive prefix sums.
4. Mark the smallest k values and query marks left of each cut.
5. Take the maximum cut requirement, starting the answer at one.

The unchanged Java reference uses a stable object sort comparing values, marks original positions, and queries each inclusive prefix. Its subtraction comparator is safe within the published nonnegative range, whose difference fits int. Preserve tie order when translating the reference; do not substitute the Silver maximum-displacement formula.

## Native workflow

Start with the learner, retain its first attempt, and consult the independently saved reference after tracing and testing. A shared walkthrough pauses at the same predictions as independent study: interpret the contract, draw the state, predict a case, implement, check, explain a mismatch, then retry later with changed input.

Use JDK 17 or newer. Confirm the site's IDE import, save and download the ZIP, extract it, and run from that extracted folder. The browser Run action gives native directions; its input panel does not replace a native file.

```sh
cp sample.in sort.in
javac -encoding UTF-8 Main.java
java Main
cat sort.out
```

In PowerShell use `Copy-Item sample.in sort.in` and `Get-Content sort.out`. Check the exit status before reading an output as a new result. The supplied learner parses the full stated line/token layout and scalar constraints before opening output. Missing input, malformed input, extra nonblank records, and unfinished tasks exit with status 2 and preserve previous output. CRLF, within-line whitespace and trailing blank lines are accepted. An output-filesystem failure is a separate I/O error. The historical reference assumes valid contest input; do not extend the learner's rejection guarantees to it. Keep prior source and input before changing a case.

## Verify and explain

Build a tiny independent simulator with the exact forward sweep, backward sweep and final adjacency check. Check the sample, one element, sorted/reversed arrays, all equal values, repeated minima/maxima, and [2,1,1], which finishes in one Gold iteration. Equal values never swap; an unstable tie ordering can invent movement. Random tiny arrays must include duplicates. For 100000 descending distinct values, the answer is 50000; for 100000 equal values it is 1. The Fenwick solver takes O(N log N) time and O(N) memory. The direct simulator is only a tiny oracle. The similarly named Silver one-direction problem has a different iteration rule and answer formula.

Record a sample prediction, a complete trace, the first attempt, two changed cases and one explained correction. Protected contests and mocks begin from an empty file without these practice packs. The source acceptance validates supplied roles and the learner driver; it does not grade a student's completed algorithm or make the tiny independent probe a full-limit Gold solver.

From the repository root, run `python3 tests/verify-fenwick-practice-packs.py --javac javac --java java`. Hosted acceptance repeats the native checks on JDK 17 and 21 before any site import is enabled for this pack.
