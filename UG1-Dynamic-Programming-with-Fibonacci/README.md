# Dynamic programming foundations: Fibonacci

This core foundation project makes the dynamic-programming state and evaluation order explicit. It is a course-authored exercise with a newly supplied C++20 learner pack and independently authored reference.

## Contract and state

Read one index n from `fibonacci.in`, where 0 <= n <= 92. Write F(n) to `fibonacci.out`. Define F(0)=0, F(1)=1, and F(k)=F(k-1)+F(k-2) for k >= 2. The driver rejects indices outside the contract before creating an answer file.

Let `state[k]` represent F(k). Initialize the two base cases, then evaluate increasing indices so both dependencies are already known. An array of n+1 entries handles n=0 without writing entry 1. Signed 64-bit storage holds F(92)=7540113804746346429; F(93)=12200160415121876738 exceeds its maximum. Restricting the input prevents signed overflow.

## Guided implementation

1. Draw the repeated subproblems in a naive recursive computation of F(5). Explain why the same state is recomputed.
2. Write a state definition, base cases, transition, and evaluation order before editing `starter/main.cpp`.
3. Complete the marked helper and run the supplied n=10 fixture, which should produce 55.
4. Check n=0, 1, 2, 10, and 92. Trace the table for a small index. Compare a short recursive version only on small inputs; it is unsuitable as a full-scale reference.
5. Explain O(n) time and O(n) space for the table. As an optional extension, keep only the two most recent states, preserving the same base-case and overflow boundaries.

The provided reader and writer remain unchanged during the learner task. `solution/` is a separate completed reference for reviewing the state invariant after an attempt. The optional Fibonacci worksheet reuses this core project to compare recursion, tabulation, and memory use; it does not require another starter import.

## Build and run

From `starter/` (or `solution/`), compile with `c++ -std=c++20 -Wall -Wextra -Wpedantic main.cpp -o fibonacci` and run `./fibonacci`. Input and output files use the current directory. The untouched starter reports its unfinished helper and creates no output. Remove stale `fibonacci.out` before a fresh run.

The acceptance check runs all 93 valid indices through actual file I/O against an independent integer combinatorics oracle. It also checks that invalid indices and the untouched learner starter cannot create an answer file.
