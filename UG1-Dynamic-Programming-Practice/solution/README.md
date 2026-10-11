# Dynamic programming implementation practice: reference

A focused implementation lab after Fibonacci state design. It compares rolling contiguous-sum state, a grid table and recursive 0-1 choices. It complements the separate iterative knapsack exercise; it is not a contest input format.

## Contract

No input file or terminal input is read. Edit the constants in a working copy. The three output lines are the maximum contiguous-subarray sum with an empty subarray allowed, the number of top-left to bottom-right grid paths using right/down steps, and the maximum value of a subset of distinct items within capacity. Each item is `[weight, value]`; the recursive index names the last available zero-based item, or -1 when none remain. Zero-weight items are allowed and can be taken once even at capacity zero.

Teaching bounds: at most 2000 subarray values, each from -1000000 to 1000000; grid rows and columns from 1 to 15; at most 20 items, nonnegative weights/values at most 1000000, and capacity from 0 to 1000000. These keep array/grid totals in int and bound the exponential reference to at most 2^20 subsets. The reference assumes valid edited constants; the learner driver validates them.

## Prediction

The default array `[5,-5,6,2,3]` has optimum 11. A 3-by-2 grid has 3 paths. Items `[[1,5],[2,3],[4,5],[2,3],[5,2]]` at capacity 10 have optimum 16, using the first four items (weight 9). The output is `11`, `3`, `16`, one number per line.

## Tasks and walkthrough

1. Define the rolling state and empty-subarray base case.
2. Define grid boundary counts and a legal evaluation order.
3. Terminate recursive knapsack only after every item is considered.
4. Compare skip/take branches that both move to the preceding item.

This role is a completed reference for comparison after a saved attempt. Its original source bytes remain in `../legacy/Main.java`; only the documented small correctness or trace-control repairs change the maintained program.

For independent work or an instructor walkthrough: predict the sample, state the invariant, trace one transition, save the attempt, and compare an independently checked changed case before opening the separate reference. Return to the same attempt for reflection; use changed small datasets for transfer practice.

## Build and run

Use JDK 17 or newer inside this role's working directory. These commands also work in PowerShell:

```sh
javac --release 17 -encoding UTF-8 Main.java
java Main
```

This demonstration reads no terminal input, input file or command-line argument. Edited constants are its dataset; output appears on the terminal. The site IDE saves and exports this native Java project; native execution is required, and its Input panel does not run this program.

## Independent checks

Check an empty/all-negative subarray, a single-row/column grid, no items, no fitting item, a single item of weight 1 and value 5, and zero-weight positive-value items at capacity zero. Independently enumerate contiguous intervals and item subsets; enumerate tiny grid walks or use the binomial coefficient. Confirm input arrays remain unchanged. The original reference skipped item zero; its smallest correction also handles zero-weight items at capacity zero.

Maximum subarray takes O(A) time and O(1) storage. Grid DP takes O(R*C) time/storage. Recursive knapsack takes O(2^K) worst-case time and O(K) call-stack space, without memoization. State repeated `(index,capacity)` calls before proposing memoization as an extension.

From the repository root, run `python3 tests/verify-implementation-labs.py --javac javac --java java`. Hosted acceptance repeats with JDK 17 and 21. Driver probes validate supplied infrastructure in temporary copies; they do not complete or grade the saved learner algorithm.
