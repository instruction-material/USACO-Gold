# Superbull: maximum score: learner

This is the unfinished learner. Implement the tasks before comparing with the separate reference.

Source contract: [USACO, February 2015 Silver, problem 3](https://usaco.org/index.php?page=viewproblem2&cpid=531). Historical curriculum placement is independent of the original contest division.

## Contract

Read `superbull.in`. N is 1..2000. Read N distinct positive team IDs, each at most 2^30-1. A game scores the XOR of its IDs and eliminates one participant. Choose N-1 games ending with one survivor to maximize total points. Write one integer followed by a newline in `superbull.out`.

## Prediction

The official sample included in this folder is:

```text
4
3
6
9
10
```

Expected `superbull.out`: `37`.

The sample permits 37 points. Games joining 3 to 9, 6 to 9, and 6 to 10 score 10, 15, and 12; choose eliminations consistent with a final survivor.

## Tasks and walkthrough

1. Explain why a sequence of elimination games forms a spanning tree.
2. Choose maximum XOR crossing edges, or negate weights consistently for a minimum-key formulation.
3. Include each team once and update its best connection to the chosen set.
4. Accumulate all selected game scores in long; a single team needs zero games.

The learner has four marked algorithm tasks and is deliberately unfinished. Untouched work exits 2 before opening an answer file. Parsing and result bounds are supplied; they do not grade optimality. For independent study or an instructor walkthrough, record a prediction, trace a small case, implement and save an attempt, then compare two changed inputs with an independent model. Consult the separate reference after an attempt and explain any discrepancy. Preserve the first implementation; a later retry uses different data, a boundary case and a closed reference.

## State and reasoning

Each elimination game joins a removed team to a survivor, producing a tree. Conversely, removing tree leaves toward a root realizes any spanning tree as an elimination sequence. The maximum spanning tree therefore gives the greatest score. A dense Prim implementation stores each unchosen team's best edge to the chosen set, selects the greatest key, and updates keys with XOR. The historical reference negates XOR weights and selects the minimum key. Do not interpret these keys as shortest-path distances. Use long for the sum; every edge fits int but 1999 scores may not.

O(N^2) time and O(N) auxiliary space without constructing every complete-graph edge.

## Build and run

Use JDK 17 or newer inside this role's working folder. These commands also work in PowerShell:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java &&
java -ea -Xmx256m Main
task_course_status=$?
if [ "$task_course_status" -eq 0 ]; then cat superbull.out; else printf 'Build or run failed with exit status %s\n' "$task_course_status"; fi
```

On PowerShell:

```powershell
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
if ($LASTEXITCODE -eq 0) {
    java -ea -Xmx256m Main
    if ($LASTEXITCODE -eq 0) { Get-Content superbull.out }
    else { Write-Host "Run failed with exit status $LASTEXITCODE" }
} else { Write-Host "Compilation failed with exit status $LASTEXITCODE" }
```

Keep `superbull.in` beside Main.java. Run Java only after a successful compilation. Check exit status first; read `superbull.out` only after success with `cat superbull.out` or `Get-Content superbull.out`. Run the file-based Java program natively after exporting its ZIP; the browser Input panel does not supply its input file. The unfinished learner, missing input and refused input preserve an earlier answer because computation and basic result validation precede opening output. The historical reference assumes complete valid contract input; a previous answer is not evidence of a successful run. Learner and reference are independent source roles and should be opened only after confirming the source import.

## Independent checks

Independently enumerate the remaining-team subsets: for every possible game add its XOR score and choose either eliminated participant, then recurse. This models actual elimination choices rather than Prim. Cover a singleton, two teams, the official sample, changed distinct IDs and totals above 32-bit range. A full-size construction uses IDs 1..1999 plus 2^30-1. Every small ID has its uniquely greatest edge to that last team, so the forced star score is 1999*(2^30-1)-1999*2000/2.

From the repository root run `python3 tests/verify-spanning-interval-packs.py --javac javac --java java`. Hosted checks repeat with JDK 17 and 21. Temporary driver probes check the supplied parser and output guard only; the committed learner algorithms remain unfinished. Native acceptance and consent-based site import activation are separate gates.
