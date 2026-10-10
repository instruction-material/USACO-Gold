# Sleepy Cow Sorting: reference pack

## Prerequisites and input

This optional Gold ordering practice follows sorting and Fenwick point updates/prefix sums. It reinforces a diagnosed gap or provides a changed-case retry; it is not an additional prerequisite for the required course spine. If already completed in the core unit, preserve that attempt and change the cases.

Read N (1..100000), then one line containing a permutation of 1..N. One command removes only the first cow and inserts it after k remaining cows, with 1 <= k <= N-1. Read sleepy.in. Write the minimum command count K, followed by K legal move distances, to sleepy.out. Any optimal sequence is accepted. A sorted row, including N=1, needs K=0 and no move tokens.

Problem contract: [USACO Sleepy Cow Sorting](https://usaco.org/index.php?page=viewproblem2&cpid=898).

## Trace and explain

Keep the longest strictly increasing suffix. Cows in this suffix can remain in relative order; every earlier cow must eventually move, giving a lower bound equal to the prefix length. Move each prefix cow once into the growing sorted suffix to attain that bound. Mark suffix values in a Fenwick tree. For original prefix position i, the insertion distance is the number of unprocessed prefix cows after it plus the number of already inserted values smaller than this cow. Update its value after recording the move.

For 1,2,4,3 the suffix is [3], so K=3. Commands 2,2,3 give [2,4,1,3], then [4,1,2,3], then [1,2,3,4]. Explain both why three moves suffice and why fewer cannot work. The untouched learner must still stop on already sorted input: it does not silently complete the zero-move case.

The supplied sample answer is:

```text
3
2 2 3
```

## Marked learner tasks

1. Find the first position of the longest increasing suffix.
2. Implement Fenwick value updates.
3. Implement inclusive prefix sums, with prefix(-1)=0.
4. Seed the suffix values and retain the original prefix order.
5. Produce each insertion distance, then mark that value in the growing suffix.

The preserved historical Java reference stores zero-based values and queries an inclusive prefix at the current value before marking it. Because the permutation is unique and that value is still absent, this counts strictly smaller inserted values. The reference need not end its final move line with a newline. On K=0 it writes only the count line; token-based validation accepts no move tokens. The learner writes an explicit blank move line when completed with K=0.

## Native workflow

Start with the learner, retain its first attempt, and consult the independently saved reference after tracing and testing. A shared walkthrough pauses at the same predictions as independent study: interpret the contract, draw the state, predict a case, implement, check, explain a mismatch, then retry later with changed input.

Use JDK 17 or newer. Confirm the site's IDE import, save and download the ZIP, extract it, and run from that extracted folder. The browser Run action gives native directions; its input panel does not replace a native file.

```sh
cp sample.in sleepy.in
javac -encoding UTF-8 Main.java
java Main
cat sleepy.out
```

In PowerShell use `Copy-Item sample.in sleepy.in` and `Get-Content sleepy.out`. Check the exit status before reading an output as a new result. The supplied learner parses the full stated line/token layout and scalar constraints before opening output. Missing input, malformed input, extra nonblank records, and unfinished tasks exit with status 2 and preserve previous output. CRLF, within-line whitespace and trailing blank lines are accepted. An output-filesystem failure is a separate I/O error. The historical reference assumes valid contest input; do not extend the learner's rejection guarantees to it. Keep prior source and input before changing a case.

## Verify and explain

Check one cow, an already sorted row, the sample, a reversed row, and a small value buried near the end. Apply every reported move to a copy of a tiny row: remove its first value and insert at the reported zero-based position in the remaining list. Require legal distances, a sorted final row and the minimum number of moves. A tiny breadth-first search over permutations is an independent minimum oracle; it accepts any optimal sequence. Do not compare all correct solutions with a single expected move list. For N=100000 in reverse order, K=N-1 and the moves N-1,N-2,...,1 are a useful full-limit fixture. Fenwick processing takes O(N log N) time and O(N) memory. The learner driver checks output structure and bounds, not optimality or full algorithm correctness.

Record a sample prediction, a complete trace, the first attempt, two changed cases and one explained correction. Protected contests and mocks begin from an empty file without these practice packs. The source acceptance validates supplied roles and the learner driver; it does not grade a student's completed algorithm or make the tiny independent probe a full-limit Gold solver.

From the repository root, run `python3 tests/verify-fenwick-practice-packs.py --javac javac --java java`. Hosted acceptance repeats the native checks on JDK 17 and 21 before any site import is enabled for this pack.
