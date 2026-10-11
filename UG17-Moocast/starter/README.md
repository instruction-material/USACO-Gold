# Moocast: connectivity threshold: learner

This is the unfinished learner. Implement the tasks before comparing with the separate reference.

Source contract: [USACO, December 2016 Gold, problem 1](https://usaco.org/index.php?page=viewproblem2&cpid=669). Historical curriculum placement is independent of the original contest division.

## Contract

Read `moocast.in`. N is 1..1000. Read N coordinate pairs with both coordinates in 0..25000. Spending X enables every direct transmission whose squared distance is at most X. Relays are allowed. Find the minimum integer X that lets a broadcast reach all cows. Write one integer followed by a newline in `moocast.out`.

## Prediction

The official sample included in this folder is:

```text
4
1 3
5 4
7 2
6 1
```

Expected `moocast.out`: `17`.

The official sample requires 17. At that threshold, edges between (1,3) and (5,4), between (5,4) and (6,1), and between (6,1) and (7,2) connect all cows. Any smaller threshold leaves the first cow isolated.

## Tasks and walkthrough

1. Model an undirected edge by squared coordinate distance; no square root is needed.
2. Connect every cow with minimum spanning-tree crossing-edge choices.
3. Update the cheapest edge linking each unchosen cow to the chosen set.
4. Return the greatest selected edge, rather than the sum; one cow needs zero power.

The learner has four marked algorithm tasks and is deliberately unfinished. Untouched work exits 2 before opening an answer file. Parsing and result bounds are supplied; they do not grade optimality. For independent study or an instructor walkthrough, record a prediction, trace a small case, implement and save an attempt, then compare two changed inputs with an independent model. Consult the separate reference after an attempt and explain any discrepancy. Preserve the first implementation; a later retry uses different data, a boundary case and a closed reference.

## State and reasoning

For a fixed X, connectivity depends only on edges whose squared length is at most X. If a minimum spanning tree has greatest edge w, X=w connects every cow. A smaller X separates the cut crossed by a greatest required tree edge, so it cannot connect all cows. A dense Prim implementation keeps minimum crossing squared distances; the answer is their maximum as cows are chosen, not their sum. Differences are at most 25000 and a squared diagonal is at most 1250000000, so the documented edge values fit int. A singleton or entirely coincident cows has answer zero.

O(N^2) time and O(N) auxiliary space without materializing every pair.

## Build and run

Use JDK 17 or newer inside this role's working folder. These commands also work in PowerShell:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java &&
java -ea -Xmx256m Main
task_course_status=$?
if [ "$task_course_status" -eq 0 ]; then cat moocast.out; else printf 'Build or run failed with exit status %s\n' "$task_course_status"; fi
```

On PowerShell:

```powershell
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
if ($LASTEXITCODE -eq 0) {
    java -ea -Xmx256m Main
    if ($LASTEXITCODE -eq 0) { Get-Content moocast.out }
    else { Write-Host "Run failed with exit status $LASTEXITCODE" }
} else { Write-Host "Compilation failed with exit status $LASTEXITCODE" }
```

Keep `moocast.in` beside Main.java. Run Java only after a successful compilation. Check exit status first; read `moocast.out` only after success with `cat moocast.out` or `Get-Content moocast.out`. Run the file-based Java program natively after exporting its ZIP; the browser Input panel does not supply its input file. The unfinished learner, missing input and refused input preserve an earlier answer because computation and basic result validation precede opening output. The historical reference assumes complete valid contract input; a previous answer is not evidence of a successful run. Learner and reference are independent source roles and should be opened only after confirming the source import.

## Independent checks

Collect distinct squared pair distances, test each threshold using flood-fill connectivity, and select the first connected threshold. This independent model does not build a spanning tree. Cover the official sample, coincident coordinates, a singleton, maximum diagonal coordinates and changed small sets. Full-size constructions include 1000 coincident cows (zero), 1000 cows on a line at spacing 25 (625), and a 20-by-50 grid at spacing 500 (250000).

From the repository root run `python3 tests/verify-spanning-interval-packs.py --javac javac --java java`. Hosted checks repeat with JDK 17 and 21. Temporary driver probes check the supplied parser and output guard only; the committed learner algorithms remain unfinished. Native acceptance and consent-based site import activation are separate gates.
