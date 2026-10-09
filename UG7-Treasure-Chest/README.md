# Treasure Chest: plan against an optimal opponent

This supplemental interval-DP project uses the USACO December 2010 Silver task within the existing Gold practice sequence. Contest division and teaching placement differ: here the purpose is to model adversarial choices, justify an interval state and compress its memory. Prerequisites are arrays, recurrence dependencies and basic DP. It is not a required mock-contest replacement.

The [original USACO statement is reproduced by this archive](https://ac.nowcoder.com/acm/problem/24756). The programs are newly authored teaching material, not a recovered legacy solution. The older `solution/treasure.out` is preserved byte for byte; its input is missing, so it is not an acceptance fixture or the expected answer for the supplied practice input.

## Contract and example

Read `treasure.in`: N from 1 through 5000, then N coin values from 1 through 5000. Two players alternate taking exactly one coin from either end of the remaining line. Both maximize their own total. The first player moves first. Write that player's greatest achievable total to `treasure.out`.

The supplied practice input lists 30, 25, 10, 35 and has answer 60. Run in a separate working directory when preserving the historical output file; a successful run writes a fresh output in its current directory. The learner and reference use the same input contract.

## Predict, implement, explain

1. Enumerate both first moves on a short line. For each choice, continue with an opponent who also chooses optimally. Taking the larger visible coin is not a general strategy.
2. Define a state for the current player's score advantage over the opponent on the remaining interval. With one coin, its value is the advantage.
3. Taking either end earns that coin, then changes whose advantage the shorter interval describes. Derive both candidates and choose the better one.
4. Complete `maximumFirstPlayerTotal` in `starter/main.cpp`. The file driver is supplied; the untouched learner reports its TODO and writes no answer.
5. Fill intervals in increasing length. For a rolling vector, identify the two old states needed by each update and prove why the left index must increase.
6. Recover the first player's total from the sum of all coins and the final advantage. Explain why the result is an integer; advantage and wealth are different quantities.
7. Test a single coin, equal coins, odd and even lengths, reversed lines, and a greedy trap such as 8, 15, 3, 7. Compare small games with complete alternating game-tree search.

The reference takes O(N squared) time and O(N) total storage, including the input. A full N-by-N 64-bit table needs about 200 MB at N = 5000. The rolling-vector dependency proof is part of the task.

## Run, check and submit

From either role directory, compile `c++ -std=c++20 -Wall -Wextra -Wpedantic main.cpp -o treasure`, then run `./treasure`. Input and output use the current directory. In the site IDE, inspect the newly written output file after Run. Compare the separate reference after making and testing an independent attempt.

Submit source, independently predicted short-game outcomes and an explanation of the state, both players' choices, update order and memory use. Optional work continues the saved attempt. Repository acceptance checks complete short game trees, 5000-coin cases, malformed input, byte preservation of the unmatched historical output and the untouched learner.
