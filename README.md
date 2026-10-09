# USACO Gold

Source material for the Gold course. These C++20 projects provide separate learner and completed-reference packs with fixtures and assignment guides:

- [Fibonacci dynamic programming](UG1-Dynamic-Programming-with-Fibonacci/README.md): core state definition, base cases, transition and evaluation order.
- [Marathon Gold](UG5-Marathon/README.md): optional point-update and range-query practice using mutable checkpoints and sum/maximum segment trees. This implements the 2014 Gold contract.

Each guide explains the contract, predictions, learner tasks, examples, independent checks, and native build command. Start with the `starter/` pack, retain the learner attempt, and compare the separate `solution/` reference after an attempt. The other course folders retain their existing material.

Repository acceptance: `python3 tests/verify-gold-packs.py --compiler c++ --mode ordinary`. Use `--mode sanitized` for address and undefined-behavior checks. The pinned hosted workflow repeats both modes with GCC and Clang. Checks compile both roles, execute actual file I/O, compare independent models, cover the advertised limits, and require untouched learner tasks to remain unfinished.
