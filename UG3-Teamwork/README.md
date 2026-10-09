# Teamwork: choosing the final team in a prefix DP

This optional dynamic-programming project implements the [2018 December Gold problem](https://usaco.org/index.php?page=viewproblem2&cpid=863). The separate C++20 starter and reference retain the existing official input fixture.

## Contract

Read `teamwork.in`: N and K, then N cow skills in arrival order. N is 1 through 10,000, K is 1 through 1,000, and each skill is 1 through 100,000. Partition the cows into consecutive teams of size at most K. Each member receives the maximum skill of its team. Write the maximum total to `teamwork.out`. The supplied sample's result is 84.

## State, prediction and implementation

Define `best[i]` as the best total for exactly the first i cows, with `best[0]=0`. A final team of size s contributes s times the maximum of its skills and leaves the first i-s cows optimally arranged. Consider every s from 1 through min(K,i). Extending the team backward updates its maximum in constant time; rescanning each candidate team would add an avoidable factor of K.

1. Trace the sample's teams of sizes 3, 1 and 3. Compare at least one alternative partition.
2. Write the state definition, base case and final-team transition, then complete `bestTeamwork` in `starter/main.cpp`.
3. Test K=1, one cow, K larger than N, identical skills, and a high-skilled cow near a team boundary. Enumerate all partitions for small inputs rather than assuming a greedy grouping is correct.
4. Explain O(NK) time and O(N) space, and why the specified limits make this feasible. Keep signed 64-bit arithmetic in the provided interface.

The file driver is supplied; the learner helper remains unfinished. The completed `solution/` pack is a review reference after an attempt. This exercise supplements the foundation recurrence and does not change the Fibonacci core project.

## Run and verify

From the selected role directory, compile with `c++ -std=c++20 -Wall -Wextra -Wpedantic main.cpp -o teamwork`, then run `./teamwork`. Files use the current directory. The untouched starter reports its TODO and creates no output; remove stale output before checking an attempt. Independent acceptance enumerates legal small partitions and checks both full N/K limits through actual file I/O.
