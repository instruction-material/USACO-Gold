# USACO Gold

Source material for the Gold course. These C++20 projects provide separate learner and completed-reference packs with fixtures and assignment guides:

- [Fibonacci dynamic programming](UG1-Dynamic-Programming-with-Fibonacci/README.md): core state definition, base cases, transition and evaluation order.
- [Marathon Gold](UG5-Marathon/README.md): optional point-update and range-query practice using mutable checkpoints and sum/maximum segment trees. This implements the 2014 Gold contract.

Each guide explains the contract, predictions, learner tasks, examples, independent checks, and native build command. Start with the `starter/` pack, retain the learner attempt, and compare the separate `solution/` reference after an attempt. The other course folders retain their existing material.

Repository acceptance: `python3 tests/verify-gold-packs.py --compiler c++ --mode ordinary`. Use `--mode sanitized` for address and undefined-behavior checks. The pinned hosted workflow repeats both modes with GCC and Clang. Checks compile both roles, execute actual file I/O, compare independent models, cover the advertised limits, and require untouched learner tasks to remain unfinished.

## Native Java packs

The following guides provide native Java learner and reference roles with
separate contracts and verification steps:

- [Gold setup checkpoint](UG0-Contest-Contract/README.md): standard input/output and 64-bit totals before algorithm lessons.
- [0-1 Knapsack demonstration](UG2-0-1-Knapsack/README.md): small edited datasets, optimal subsets and single-use traceback.
- [Fruit Feast](UG40-Fruit-Feast/README.md): optional before/after-water reachability with native file input and output.
- [Dijkstra shortest paths](UG9-Dijkstras-Algorithm/README.md): priority-queue distances, path validation and unreachable vertices.
- [Minimum spanning tree](UG14-MST/README.md): Prim's algorithm, predecessor edges and a 64-bit tree total.
- [Fenwick tree](UG22-Binary-Indexed-Tree-Fenwick-Tree/README.md): point updates, prefix sums and range sums.
- [MooTube](UG21-Moo-Tube/README.md): optional weighted DSU and descending offline-query practice.
- [CircleCross](UG24-Why-Did-the-Cow-Cross-the-Road-III/README.md): optional interval and Fenwick crossing practice.
- [Snow Boots](UG27-Snow-Boots/README.md): optional descending-depth sweep and surviving-path gap practice.
- [Balanced Photo](UG23-Balanced-Photo/README.md): optional taller-side counts and strict imbalance checks.
- [Sleepy Cow Sorting](UG25-Sleepy-Cow-Sorting/README.md): optional optimal front-move plans and a growing sorted suffix.
- [Out of Sorts, Gold](UG26-Out-of-Sorts/README.md): optional bidirectional sweeps, stable ties and cut counts.

Each role guide is usable independently and includes native build/run
commands, predictions and changed-case checks. Retain the learner attempt
before consulting its separate reference. These programs run natively; the
site IDE saves and exports them and provides build directions.

The source manifest records the current structural inventory, including
remaining placeholder roles. A source file's presence is not proof of
algorithm correctness or an accepted site import. Use each pack's dedicated
acceptance before promoting its import action.

DP role acceptance: `python3 tests/verify-dp-learner-packs.py --javac javac --java java`. This compiles both learner scaffolds, checks their drivers and preserved answers, and repeats independent reference checks. The tiny driver probes do not complete learner algorithms.
