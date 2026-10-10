# UG2 0 1 Knapsack

Canonical source repository: `USACO-Gold`

This project was migrated from the legacy direct-source layout on 2026-05-14. The migrated reference remains under `solution/`. Its original snapshot is retained in Git history; the current reference includes the verified traceback correction below.

## Structure

- `solution/` contains the migrated source files.
- `starter/` is present to keep the course wrapper shape consistent; add a distinct starter snapshot there when one is available.

## Reference demonstration

The reference uses the four hardcoded weight/value entries and capacity 7; it does not read a contest input file. Compile with JDK 17 or newer using `javac -encoding UTF-8 Main.java`, then run `java Main` inside `solution/`. The default maximum is 9, with item indices 2 and 1.

Each table cell holds the best value with weight at most its capacity. Traceback moves to the preceding item after either skipping or selecting it, so a 0-1 item cannot be selected twice. Changing to one item with weight 2, value 3 and capacity 4 previously printed value 3 but selected index 0 twice; the corrected traceback selects it once.

For small changed datasets with positive integer weights and nonnegative values whose sums fit Java int, independently enumerate subsets and check distinct indices, total weight within capacity, and selected value equal to the printed optimum. Any optimal subset is valid. This demonstration does not establish general contest limits or input validation. The learner role remains a documented source backlog item; no new site import is enabled by this correction.

Run `python3 tests/verify-knapsack-demo.py --javac javac --java java` from the repository root. Hosted checks repeat on JDK 17 and 21.
