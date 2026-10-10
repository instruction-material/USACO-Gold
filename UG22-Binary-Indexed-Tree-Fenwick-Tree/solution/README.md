# Fenwick point updates and prefix/range sums: reference

This complete reference preserves the historical demonstration's zero-based public indices and lowbit update/query loops, adds signed 64-bit sums and a validated practice driver, and includes explicit closed-range subtraction. Compare it only after an independent attempt and prediction trace.

## Prerequisites and input

Use arrays, signed integers, loops, ordinary prefix sums and zero-based closed ranges. This is an authored Gold Unit 4 data-structure practice contract, not an official contest statement. The original fixed-array demonstration is retained separately under `legacy/`.

Read UTF-8 text from standard input. The first line has exactly `N Q`; the second has exactly N initial values. Then provide exactly Q operation lines:

- `ADD index delta` adds delta to the current value at that zero-based index. It does not assign a new value.
- `PREFIX index` reports the inclusive sum from index 0 through index. `PREFIX -1` reports the empty prefix, zero.
- `RANGE left right` reports the inclusive sum over the closed interval, with `0 <= left <= right < N`. Reversed or empty ranges are refused.

The maintained practice bounds are `1 <= N <= 200000`, `0 <= Q <= 200000`, and absolute initial values and individual update deltas at most 1000000000. Updates and range endpoints must be in `[0, N-1]`; prefix indices must be in `[-1, N-1]`. Negative values and negative deltas are valid. Malformed records, missing input, out-of-bounds indices and extra nonblank records are refused. Harmless trailing blank lines are permitted. These are authored practice limits, not historical contest limits.

Print one integer per PREFIX or RANGE, in operation order; ADD prints nothing. Use `long` for tree cells and sums. Across the entire input, the absolute value of any sum is at most `(N+Q)*1000000000`, at most 400000000000000, safely within signed 64-bit arithmetic. The driver validates all input before processing it and prints only after every operation succeeds. Refused input prints no answer and exits with status 2. This program does not create an answer file; shell redirection is a separate operation.

## Trace and explain

Internal slot zero is unused. Internal slot `i > 0` stores the sum of the original zero-based indices `[i-lowbit(i), i-1]`, where `lowbit(i) = i & -i`. Explain how an update visits every block containing its index and how a prefix query partitions its interval into disjoint blocks. Convert the public index by adding one before a lowbit loop. An update starting at internal zero cannot advance.

For the sample array, `PREFIX 5` visits internal slots 6 and 4, contributing 9 and 10, so it prints 19. `RANGE 2 5` subtracts the prefix at 1, producing 14. `ADD 2 5` changes the original value -1 to 4 and visits internal slots 3, 4 and 8. The next prefix is 24. Trace every remaining sample operation before execution.

Sample output:

```text
19
14
24
3
0
9
33
```

Independently predict the visited slots, changed cell values and printed sum. With an instructor, pause at those same steps and compare the invariant before continuing. Explain when a static prefix array would suffice, when repeated point updates justify a Fenwick tree, and when a different merge operation requires another structure. Coordinate compression, inversion counting, segment trees and range updates are later extensions, not features of this point-update/sum contract.

## Native workflow

Use a native JDK 17 or newer. Save or download the three project files, extract them together, and run from that directory:

```sh
javac -encoding UTF-8 Main.java
java Main < sample.in
```

Change sample.in, write the expected output first, and rerun. The site Java teaching preview does not execute this input-driven data structure; use native execution to validate it. Do not treat a previously redirected output file as evidence of a new successful run.

## Verify and explain

Check one value, zero operations, an empty prefix, the first and last indices, negative values, cancellation and repeated additive updates. For an assignment from old to new, first derive delta = new - old; passing new directly to ADD is incorrect. Sum two billion-weight values to expose a 32-bit accumulator. Test malformed input and invalid indices, especially an ADD at -1 and an index N.

Use a plain array as an independent oracle: apply each addition directly and sum the requested slice. Exhaust tiny arrays and ranges; compare seeded update/query traces without copying lowbit logic into the oracle. Explain why range subtraction works for sums and why it does not provide a general range-minimum structure.

The tree itself uses O(N) memory. Building it with repeated additions takes O(N log N), and each update, prefix or range query takes O(log N). The complete driver takes O((N+Q) log N) time and O(N+Q) memory because it retains validated commands and answer text before printing. An optional linear-time build is a separate extension after the current invariant is explained.
