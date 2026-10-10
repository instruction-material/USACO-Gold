# 0-1 Knapsack learner

This native Java project develops a two-dimensional dynamic programming state and a traceback that chooses each item at most once. It is a supplemental transfer exercise after Fibonacci state design. The four-item dataset is written in `Main.java`; this demonstration reads no input file or terminal input. It is not an official contest submission format.

## Contract and prediction

The default weights are `[1, 3, 4, 5]`, values `[1, 4, 5, 7]`, and capacity `7`. Select distinct zero-based indices with total weight at most capacity and maximum total value. The optimum is `9`, attained by indices `1` and `2` with weight `3+4=7` and value `4+5=9`. Any optimal subset and either index order are valid. The reference prints the indices in traceback order `[2, 1]`.

For changed teaching datasets, keep positive integer weights, nonnegative values, equal array lengths and nonnegative capacity. The learner driver permits at most one million table cells and requires the sum of values to fit Java int. These are explicit limits for small learning experiments. The reference assumes valid edited constants and has no equivalent input validator. Both the runtime O(n*W) and the table storage O(n*W) must be estimated before increasing the number of items n or capacity W.

Define `dp[i][w]` as the best value using only the first i items with weight at most w. With no items or zero capacity the value is zero because weights are positive. Skipping an item uses the preceding row at w. Taking it uses its value plus the preceding row at the remaining capacity, when it fits. Every choice reads the preceding item row, so one item cannot be reused.

Traceback compares a cell with the preceding row. Equality permits skipping; a larger value means the current item is selected. Move to the preceding row after either choice, and subtract the selected weight only after a take. Stop when no positive value remains. Ties may give different optimal subsets.

## Learner tasks and walkthrough

The `starter/` contains a distinct driver with five marked tasks:

1. Define and allocate the table, with zero base cases.
2. Fill the skip/take recurrence from the preceding row.
3. Decide which traceback steps select an item.
4. Move past every considered item, including a selected item.
5. Return the terminal value and reconstructed indices without changing the input arrays.

The supplied driver validates parameters and the feasibility, uniqueness and reported value of the returned selection. It does not independently prove optimality; use a tiny subset oracle for that. Untouched tasks report unfinished work with exit status 2 and produce no answer. Keep a prediction and a saved learner attempt before inspecting the separate reference.

For an independent walkthrough or an instructor discussion, first enumerate the feasible subsets of the default dataset. Draw one table row, explain why taking an item cannot read the same row, trace the optimum to selected indices, then compare a changed case with the oracle. The checkpoints are the state sentence, a legal dependency order, a traceback invariant and evidence for optimality.

## Build, run and changed cases

In a working copy of `starter/` or `solution/`, use JDK 17 or newer:

```sh
javac -encoding UTF-8 Main.java
java Main
```

The completed reference prints maximum value 9 and indices `[2, 1]`. Edit the arrays and capacity in a copy when testing other cases; the reference also has `numItems`, which must match the arrays. The learner derives the item count from the arrays. Native commands work in PowerShell as written. The site IDE can save and export native Java projects; the program runs with the local JDK and has no Input-panel data contract.

Check empty arrays, capacity zero, no item fitting, repeated weights, zero values and a tie between optimal subsets. With one item of weight 2, value 3 and capacity 4, the result is value 3 and index 0 once. The reference's earlier repeated-index defect is corrected; its historical snapshot is preserved in Git history.

For small datasets, enumerate all subsets independently and compare the maximum feasible value. Also require distinct in-range indices, total weight within capacity and selected value equal to the reported optimum. Do not compare an optimal index list to one fixed ordering.

From the repository root, run `python3 tests/verify-knapsack-demo.py --javac javac --java java` for reference accuracy and `python3 tests/verify-dp-learner-packs.py --javac javac --java java` for both role contracts. Hosted acceptance repeats on JDK 17 and 21. The learner checks compile the untouched scaffold, retain unfinished behavior, validate parameters and exercise the supplied driver with a tiny independent oracle; they do not complete or grade a learner's DP algorithm.
