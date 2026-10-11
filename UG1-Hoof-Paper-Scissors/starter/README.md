# Hoof, Paper, Scissors with a switch budget: learner

Optional Gold dynamic-programming application after prefix states and bounded choices. This exercise adds a remaining switch budget and a gesture dimension to an ordered sequence; it is distinct from grouping consecutive cows into teams.

Source contract: [USACO, January 2017 Gold, problem 2](https://usaco.org/index.php?page=viewproblem2&cpid=694).

## Contract

Read `hps.in`: N K, then N opponent gestures, each H, P or S. N is 1..100000; K is 0..20. Hoof beats scissors, scissors beats paper, and paper beats hoof; equal gestures tie. Choose Bessie's gesture for each round while changing it at most K times. Write the greatest possible number of wins as one integer in `hps.out`.

## Prediction

The unchanged official sample in `hps.in` is:

```text
5 1
P
P
H
P
S
```

Expected `hps.out`:

```text
4
```

Bessie can play scissors for rounds 1..4 and hoof for round 5: three wins against paper plus a win against scissors. The hoof opponent in round 3 is a loss. With K=0 the same sample permits three wins. A single opponent gesture permits one win even with a budget larger than the number of possible boundaries.

## Tasks and walkthrough

1. Define the meaning of every state dimension and initialize zero games.
2. Continue the current gesture with the same switch budget.
3. Compare changing from either other gesture, using one unit of budget.
4. Add this round's cyclic win and select the best final gesture.

The learner contains four marked algorithm tasks and is deliberately unfinished. Untouched work exits 2 without producing a new answer. The supplied parser and basic result bounds do not prove optimality.

For independent study or an instructor walkthrough, predict the sample, identify the state, trace the first three rounds, implement and save an attempt, then compare a changed small case with an independently enumerated gesture sequence. Consult the separate reference after an attempt; keep the original prediction and explain any correction.

## State and reasoning

One useful definition is dp[i][j][g]: the most wins in the first i rounds, with at most j switches, ending with literal Bessie gesture g. At zero rounds, every allowed budget has value zero. Keeping the gesture reads the preceding prefix at budget j; switching reads a different gesture at budget j-1 when j>0. Add one only if Bessie's gesture beats the opponent. A tie does not win. All values fit int because they lie in 0..N.

The historical reference instead labels a state by the opponent gesture it beats. Its labels H/P/S therefore correspond to Bessie's P/S/H. This is a one-to-one cyclic relabeling, so changing target is equivalent to changing Bessie's gesture. Equality of its target label with an opponent move counts a win, not a tie between literal gestures. Do not combine that equality test with states labeled by literal Bessie gestures.

The prefix order means every transition depends only on the preceding round. The full table uses O(N(K+1)) time and space with three gesture states. Rolling consecutive layers reduces auxiliary space to O(K+1), provided the current layer never overwrites a state still needed for that round. Compare the two representations after the first implementation works.

## Build and run

Use JDK 17 or newer in this role's working folder. These commands also work in PowerShell:

```sh
javac --release 17 -encoding UTF-8 Main.java
java Main
```

Keep `hps.in` beside `Main.java`; inspect `hps.out` afterward. The site IDE can save and export native Java. Run this file-based program natively; the browser Input panel does not supply `hps.in`. The historical reference also prints its answer to the terminal. The learner parses, computes and validates before opening output, so unfinished or refused work preserves a previous answer.

## Independent checks

Enumerate all actual H/P/S sequences for a short opponent list, count changes between adjacent rounds, reject those exceeding K, and count wins using the cyclic game rules. This verifies the answer without copying the DP recurrence or its relabeling. Cover all three one-round opponents, no switches, K larger than the number of boundaries, alternating opponents and the official sample.

Full-size constructions cover 100000 identical gestures, a zero-switch repeated cycle with an independently counted majority, and 21 constant runs that can all be beaten with exactly 20 changes. From the repository root run `python3 tests/verify-hps-pack.py --javac javac --java java`. Hosted checks repeat with JDK 17 and 21. Temporary tiny driver probes check supplied parsing/output only; the saved learner algorithm remains unfinished and is not graded by those probes. Source readiness and consent-based site imports are separate checks.
