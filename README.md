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
- [Dijkstra shortest paths](UG9-Dijkstras-Algorithm/README.md): priority-queue distances, path validation and unreachable vertices.
- [Minimum spanning tree](UG14-MST/README.md): Prim's algorithm, predecessor edges and a 64-bit tree total.
- [Fenwick tree](UG22-Binary-Indexed-Tree-Fenwick-Tree/README.md): point updates, prefix sums and range sums.
- [MooTube](UG21-Moo-Tube/README.md): optional weighted DSU and descending offline-query practice.
- [CircleCross](UG24-Why-Did-the-Cow-Cross-the-Road-III/README.md): optional interval and Fenwick crossing practice.
- [Snow Boots](UG27-Snow-Boots/README.md): optional descending-depth sweep and surviving-path gap practice.

Each role guide is usable independently and includes native build/run
commands, predictions and changed-case checks. Retain the learner attempt
before consulting its separate reference. These programs run natively; the
site IDE saves and exports them and provides build directions.

The source manifest records the current structural inventory, including
remaining placeholder roles. A source file's presence is not proof of
algorithm correctness or an accepted site import. Use each pack's dedicated
acceptance before promoting its import action.
