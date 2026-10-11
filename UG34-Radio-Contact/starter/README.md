# Learner: Radio Contact: Coordinating Two Fixed Paths

This exported learner role leaves the algorithm tasks unfinished.

This required capstone models two progress counters rather than searching for new spatial routes. The paths are fixed; the program chooses when each traveler advances. A written state model, an unfinished learner and a separate reference support either independent study or an instructor walkthrough.

## Contract

Read `radio.in`: N and M, the first start x/y pair, the second start x/y pair, then direction strings of lengths N and M. N and M range from 1 to 1000. Directions are N, E, S and W. Every position, including every later path position, stays within coordinates 0 through 1000. Each tick advances the first traveler, the second traveler, or both, without changing either path's order. Charge squared Euclidean distance after the move, exclude initial-position energy, and stop when both paths finish. Write the minimum total to `radio.out`.

The [official Radio Contact contract](https://usaco.org/index.php?page=viewproblem2&cpid=598) specifies those bounds. The original sample fixtures remain available in both roles.

## Prediction

```text
2 7
3 0
5 0
NN
NWWWWWN
```

Expected output:

```text
28
```

Before coding, list both position sequences, including their initial positions. Distinguish a position index from a wall-clock tick. Several ticks may pass while one index stays fixed. A completed path's traveler may remain at its final position while the other finishes.

## State and reasoning

A state (i,j) means that i first-path moves and j second-path moves have finished. The coordinates at that state are already supplied in `Input.firstPath` and `Input.secondPath`. The provided `energy(input,i,j)` returns the squared distance using long arithmetic.

Initialize the initial state's cost to zero. A noninitial state can come from a first-only move, a second-only move or a simultaneous move, whenever those predecessor indices exist. Add the energy at the destination state to a feasible predecessor cost. Processing increasing indices ensures each needed predecessor is available. A transition advancing neither index cannot improve a nonnegative-cost schedule and would create an unnecessary cycle.

The answer belongs at (N,M). Handle states on both axes: they describe one traveler moving while the other remains at its initial position. Do not charge the initial separation, substitute ordinary distance for squared distance, or charge both travelers separately for a simultaneous tick.

A full table uses O(N*M) time and O(N*M) memory; a rolling-row extension can reduce memory after the full-table version is explained. At the official coordinate bounds, each tick costs at most 2000000. Advancing both travelers whenever possible finishes a prefix in max(i,j) ticks, bounding each optimal state by 2000000000. One candidate transition costs at most 2002000000, which still fits signed int. The preserved int reference is therefore valid for this contract; the learner uses long to make numeric intent explicit.

## Tasks and walkthrough

The parser builds both position arrays and validates counts, direction lengths, letters, all positions and trailing input. The distance helper and file handling are provided. `minimumEnergy(Input input)` remains unfinished.

1. Define the state values, feasible base cases and table evaluation order.
2. Compare every legal predecessor, including axis states and simultaneous moves.
3. Add destination energy and return the cost when both paths finish.

For a walkthrough, draw a small progress grid, trace its first row and column, and explain the three incoming transitions of an interior cell. Predict a changed path before comparing the completed reference. The supplied learner contains no schedule solver. An untouched run exits with status 2, writes no new answer and preserves any existing answer.

## Independent checks

- Both travelers starting together and taking E have optimal cost zero.
- Starting at (0,0) and (2,0), with paths E and W, gives zero by moving simultaneously.
- Starting at (0,0) and (0,2), both taking E, gives 4. Charging initial energy would incorrectly increase it.
- For tiny paths, enumerate every sequence of first-only, second-only and simultaneous moves that finishes both paths. Sum destination squared distances for each schedule and choose the minimum. This checks the table using an independent exhaustive model.
- At length 1000, starts (0,0) and (1000,1000), paths E repeated 1000 and W repeated 1000 remain inside the contract. Compare the full table with a separate rolling-row oracle. A path moving east from x=1000 is invalid and cannot demonstrate an overflow defect.

Keep changed-case predictions and expected results outside the program. Explain why waiting helps or hurts in each tiny case. Preserve the learner attempt before comparing the reference.

## Build and run

Use a native JDK 17 or newer. Keep this role's `Main.java` and `radio.in` together, then enter that folder. Compile only this role. On macOS or Linux:

```sh
javac --release 17 -Xlint:all -Werror Main.java && java -ea -Xmx256m Main && cat radio.out
```

In PowerShell:

```powershell
javac --release 17 -Xlint:all -Werror Main.java
if ($LASTEXITCODE -eq 0) { java -ea -Xmx256m Main }
if ($LASTEXITCODE -eq 0) { Get-Content -LiteralPath radio.out }
```

The display command runs only after success. An old answer file does not establish that an unfinished or failed run succeeded. The provided learner rejects missing or malformed input before writing. The reference expects contract-valid input and writes 28 for the sample. Save source edits, preserve expected results separately and rerun after intentional input changes.

The site workspace saves and exports native Java source when its verified resource import is enabled. Its Java preview is not a complete JDK. Native source acceptance and actual site import/export acceptance remain separate gates.

## Reference and provenance

The original reference algorithm, initial-state handling and samples are unchanged. Exact earlier committed placeholder guides are preserved under the pack's `legacy/` directory. Consult the reference after deriving the states and predicting changed cases. An unfinished learner is a project scaffold, not a completed student solution.
