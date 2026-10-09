# Marathon Gold: mutable checkpoints and range aggregates

This optional range-structure project follows the [official 2014 December Gold Marathon statement](https://usaco.org/current/index.php?page=viewproblem2&cpid=495). It belongs with point updates and range queries. The separate Bronze and Silver contest variants have different contracts; this pack implements the Gold version. The new C++20 starter and reference are independently authored.

## Input and output contract

Read `marathon.in`: N and Q, N checkpoint coordinates, then Q commands in order. N and Q are between 1 and 100,000, and each coordinate is between -1000 and 1000. `U I X Y` changes checkpoint I. `Q I J` requests the shortest sub-route from I through J, allowing at most one interior checkpoint to be skipped. Indices in the file are one-based and I <= J. Endpoints cannot be skipped. Write one answer per query to `marathon.out`. Distances use the Manhattan metric.

## Model and range conventions

The implementation converts checkpoint indices to zero-based storage. Edge i connects points i and i+1. The full sub-route from a through b is the sum of edges in `[a, b)`. Skipping an interior point i saves `distance(i-1,i) + distance(i,i+1) - distance(i-1,i+1)`, which is nonnegative by the triangle inequality. Therefore subtract the largest allowable saving, obtained from gain indices in `[a+1, b)`. A route with one or two checkpoints has no interior point to skip.

Use one segment tree for edge sums and another for maximum gains. Zero is the identity for both because all values here are nonnegative. Changing one checkpoint affects only the two incident edges and the gains of that point and its two neighbors. Boundary checks prevent accesses before the first or after the last point. A prefix array would require rebuilding after updates; a sum-only Fenwick tree does not directly supply the needed range maximum under arbitrary replacements.

## Guided implementation

1. Trace the official sample in the included fixture. Its three query outputs are 11, 8, and 8.
2. Draw the two trees' meanings and translate one-based input into half-open tree ranges. Explain why the query excludes endpoint gains.
3. Complete the learner tasks in `starter/main.cpp`: assign a tree leaf and rebuild ancestors, aggregate a half-open range, and refresh the affected values after a checkpoint update. File handling, storage allocation, distance calculation, and the route formula are provided.
4. Test a single checkpoint, adjacent endpoints, repeated coordinates, collinear routes, an update to the first or last checkpoint, and repeated updates followed by queries. For a small route enumerate every allowable skipped point and compare total distances directly.
5. Explain O(N log N) initialization for this starter's repeated point assignments, O(log N) per update or query, and O(N+Q) driver storage including buffered answers. An optional extension can build tree levels bottom-up in O(N).

The full input limit requires a logarithmic data structure. `solution/` supplies a completed reference for checking the invariants after an attempt. The [official Gold analysis](https://usaco.org/current/data/sol_marathon_gold.html) offers another derivation; compare ideas and boundaries instead of replacing an unfinished learner attempt.

## Build and run

From `starter/` (or `solution/`), compile with `c++ -std=c++20 -Wall -Wextra -Wpedantic main.cpp -o marathon` and run `./marathon`. Read and write files in the current directory. The untouched starter stops with a TODO message and creates no answer file. Remove stale `marathon.out` before checking a new attempt.

The acceptance check executes real file I/O against a direct route-enumeration oracle for small cases and a separate maximum-size fixture. Ordinary and address/undefined-behavior sanitizer modes check both roles; the learner tasks remain incomplete.
