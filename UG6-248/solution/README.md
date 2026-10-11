# 248: adjacent merge intervals: reference

This is the historical reference. Compare it after an independent attempt; preserve valid input and inspect this run's exit status and answer together.

Source contract: [USACO, US Open 2016 Gold, problem 3](https://usaco.org/index.php?page=viewproblem2&cpid=647). Historical curriculum placement is independent of the original contest division.

## Contract

Read `248.in`. N is 2..248. Read N positive tile values, each in 1..40. A move replaces two adjacent equal tiles x with one tile x+1. Find the greatest tile value achievable anywhere in the sequence. Write one integer followed by a newline in `248.out`.

## Prediction

The official sample included in this folder is:

```text
4
1
1
1
2
```

Expected `248.out`: `3`.

Merge the second and third 1s in the sample to obtain 1,2,2, then merge the adjacent 2s to obtain 1,3. The best tile is 3 even though the whole sequence does not collapse.

## Tasks and walkthrough

1. Define which contiguous intervals can collapse to one tile and a sentinel for impossible intervals.
2. Initialize every singleton interval from its original tile.
3. Visit increasing interval lengths and test every split with equal, possible child tiles.
4. Track the greatest tile from any interval; the entire sequence need not collapse.

The learner has four marked algorithm tasks and is deliberately unfinished. Untouched work exits 2 before opening an answer file. Parsing and result bounds are supplied; they do not grade optimality. For independent study or an instructor walkthrough, record a prediction, trace a small case, implement and save an attempt, then compare two changed inputs with an independent model. Consult the separate reference after an attempt and explain any discrepancy. Preserve the first implementation; a later retry uses different data, a boundary case and a closed reference.

## State and reasoning

Let dp[left][right] describe a single tile produced by collapsing that inclusive interval, with zero for an impossible collapse. All input values are positive, making zero a safe sentinel. Singletons keep their input value. For each increasing interval length, compare splits into two already-computed intervals; equal nonzero child tiles merge into that value plus one. Preserve a greatest answer over every interval, not only dp[0][N-1]. The invariant sum(2^tile) is unchanged by a merge and ensures a collapsible interval has a unique final value. The bound 248*2^40 is less than 2^48, so any produced tile is at most 47.

O(N^3) time and O(N^2) auxiliary space; int suffices for tile values.

## Build and run

Use JDK 17 or newer inside this role's working folder. These commands also work in PowerShell:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java &&
java -ea -Xmx256m Main
task_course_status=$?
if [ "$task_course_status" -eq 0 ]; then cat 248.out; else printf 'Build or run failed with exit status %s\n' "$task_course_status"; fi
```

On PowerShell:

```powershell
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
if ($LASTEXITCODE -eq 0) {
    java -ea -Xmx256m Main
    if ($LASTEXITCODE -eq 0) { Get-Content 248.out }
    else { Write-Host "Run failed with exit status $LASTEXITCODE" }
} else { Write-Host "Compilation failed with exit status $LASTEXITCODE" }
```

Keep `248.in` beside Main.java. Run Java only after a successful compilation. Check exit status first; read `248.out` only after success with `cat 248.out` or `Get-Content 248.out`. Run the file-based Java program natively after exporting its ZIP; the browser Input panel does not supply its input file. The unfinished learner, missing input and refused input preserve an earlier answer because computation and basic result validation precede opening output. The historical reference assumes complete valid contract input; a previous answer is not evidence of a successful run. Learner and reference are independent source roles and should be opened only after confirming the source import.

## Independent checks

For small sequences, enumerate all reachable sequences by applying every legal adjacent equal merge, and take the greatest tile present. This models actual moves rather than interval DP. Cover the official sample, no legal merge, an all-equal run, changed order and a best tile from a proper subinterval. Full-size constructions include 248 tiles of value 40 (47), 248 alternating 1/2 values (2), and 248 increasing cyclic 1..40 values (40).

From the repository root run `python3 tests/verify-spanning-interval-packs.py --javac javac --java java`. Hosted checks repeat with JDK 17 and 21. Temporary driver probes check the supplied parser and output guard only; the committed learner algorithms remain unfinished. Native acceptance and consent-based site import activation are separate gates.
