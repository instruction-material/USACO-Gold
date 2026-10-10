# Balanced Photo: reference pack

## Prerequisites and input

This optional Gold ordering practice follows sorting and Fenwick point updates/prefix sums. It reinforces a diagnosed gap or provides a changed-case retry; it is not an additional prerequisite for the required course spine. If already completed in the core unit, preserve that attempt and change the cases.

Read N (1..100000), followed by N distinct heights, one per line. Heights are 0..1000000000. A cow is unbalanced when the larger count of taller cows on its left or right is strictly greater than twice the smaller count. Read bphoto.in and write one total to bphoto.out.

Problem contract: [USACO Balanced Photo](https://usaco.org/index.php?page=viewproblem2&cpid=693).

## Trace and explain

Process cows from tallest to shortest. A Fenwick tree marks original positions of cows already processed, so it contains exactly the taller cows. Query the marked positions strictly left of the current position; taller-right is the processed count minus taller-left. Decide the strict inequality before marking the current position. Heights are distinct, so there is no equal-height batch.

For the sample, height 34 has (L,R)=(0,1), height 5 has (4,1), and height 2 has (5,0): these three are unbalanced. Height 6 has (1,2), which is exactly the factor-two boundary and is balanced. The tallest cow has (0,0), also balanced. Predict these counts before coding.

The supplied sample answer is:

```text
3
```

## Marked learner tasks

1. Retain original positions and order cows by decreasing height.
2. Implement zero-based Fenwick point updates through one-based storage.
3. Implement inclusive prefix sums.
4. Calculate taller-left and taller-right before inserting the current cow.
5. Count only strict factor-two violations, then insert the current position.

The unchanged historical Java reference sorts negated heights and maps each distinct height to its original index. Its inclusive prefix includes the current index, but that position is still unmarked, so it equals the strict-left count. The tracked sample input remains unchanged. The historical answer file contained a nonnumeric control byte; its original byte is retained in the audit evidence and the current sample answer is corrected to 3. An included answer file is an example, not evidence of a successful new run.

## Native workflow

Start with the learner, retain its first attempt, and consult the independently saved reference after tracing and testing. A shared walkthrough pauses at the same predictions as independent study: interpret the contract, draw the state, predict a case, implement, check, explain a mismatch, then retry later with changed input.

Use JDK 17 or newer. Confirm the site's IDE import, save and download the ZIP, extract it, and run from that extracted folder. The browser Run action gives native directions; its input panel does not replace a native file.

```sh
cp sample.in bphoto.in
javac -encoding UTF-8 Main.java
java Main
cat bphoto.out
```

In PowerShell use `Copy-Item sample.in bphoto.in` and `Get-Content bphoto.out`. Check the exit status before reading an output as a new result. The supplied learner parses the full stated line/token layout and scalar constraints before opening output. Missing input, malformed input, extra nonblank records, and unfinished tasks exit with status 2 and preserve previous output. CRLF, within-line whitespace and trailing blank lines are accepted. An output-filesystem failure is a separate I/O error. The historical reference assumes valid contest input; do not extend the learner's rejection guarantees to it. Keep prior source and input before changing a case.

## Verify and explain

Check one cow (0), increasing and decreasing distinct heights (N-1), zero and the maximum height, and an exact factor-two boundary. For tiny arrays, count all taller cows on each side directly in O(N squared); compare every contribution, not only the final total. Applying a strictly increasing height transformation or reversing the row preserves the total. Duplicates are invalid here. The sorted sweep takes O(N log N) time and O(N) memory; all side counts and the doubled smaller side fit int for the advertised N.

Record a sample prediction, a complete trace, the first attempt, two changed cases and one explained correction. Protected contests and mocks begin from an empty file without these practice packs. The source acceptance validates supplied roles and the learner driver; it does not grade a student's completed algorithm or make the tiny independent probe a full-limit Gold solver.

From the repository root, run `python3 tests/verify-fenwick-practice-packs.py --javac javac --java java`. Hosted acceptance repeats the native checks on JDK 17 and 21 before any site import is enabled for this pack.
