# Time is Mooney: bounded-time graph DP

Optional applied practice after directed graph modeling and dynamic-programming
state design. This is USACO 2020 January Gold, problem 1. Unlike a shortest-path
problem, a profitable trip may revisit cities: time, city and accumulated
reward define the state, while the quadratic trip cost bounds useful time.

## Contract

[Official problem](https://usaco.org/index.php?page=viewproblem2&cpid=993).
The working directory's `time.in` contains `N M C`, then N city rewards, then
M directed roads `a b`. Bounds: `2 <= N <= 1000`, `1 <= M <= 2000`,
`1 <= C <= 1000`, and `0 <= reward[i] <= 1000`. City 1's reward is zero.
Road endpoints are distinct and numbered `1..N`. The starter converts endpoints
to zero-based indices. The graph need not provide a route back to city 1.

Start at city 1 on day 0. Each road takes one day; arrival earns that city's
reward, including on repeated visits. Finish at city 1. A trip lasting T days
pays **one total cost** `C*T*T`, not that cost on each road. `time.out` contains
one integer and a newline: the maximum net profit. Taking no trip earns zero.
Successful runs do not print answers to standard output.

The included official sample has rewards 0,10,20 on the directed cycle
1-to-2-to-3-to-1 and C=1. One cycle earns 30 minus 9 = 21; two cycles earn
60 minus 36 = 24; three earn 90 minus 81 = 9. The answer is 24. A directed
road to a profitable city without any return route still produces answer 0.

## Independent work or a shared walkthrough

Keep an initial prediction and starter attempt before opening the reference.
With a course facilitator, pause at the same state, transition and return-trip
checkpoints. Complete the four marked tasks in `solve`:

1. Bound useful time. Gross reward is at most `1000*T`; because C>=1, net
   profit is nonpositive for T>=1000. Testing days through 1000 includes every
   possible profitable trip and the no-trip option. An unexplained cutoff
   would not be a valid general argument for arbitrary reward/cost bounds.
2. Define the maximum **gross** reward for each reachable day/city pair. Start
   only day 0, city 1 at zero; mark other states unreachable. Explain why
   unreachable zeroes would invent paths.
3. For each directed a-to-b road, move from the previous day's reachable a
   state to the next day's b state, adding b's reward. Use a fresh layer;
   updating the current layer in place could traverse several roads in one day.
4. Compare returns to city 1 after subtracting C*T*T. Keep answer 0. A large
   gross reward in a different city is not a completed trip.

The historical reference uses a priority queue ordered by increasing day and
then decreasing gross reward. Its full day/city table records the same state
and return condition. Compare that schedule with explicit day layers; graph
cycles are permitted, while the day coordinate always increases.

## Native build and run

Use JDK 17 or newer with `time.in` beside `Main.java`. From either extracted
role directory:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
```

The commands also work in PowerShell. Read `time.out` only after success, with
`cat time.out` or `Get-Content time.out`. Check exit status first: unfinished
starter work exits 2 and preserves an earlier answer. The supplied driver
checks records, bounds, directed endpoints and the zero reward at city 1;
it does not establish correctness of a completed learner algorithm. The
historical reference expects valid input. Keep old source and inputs when
changing a case.

The site IDE edits, saves and exports this Java program. Its preview does not
run the file-based graph DP, and its Input panel does not replace `time.in`.
Starter and reference use separate saved projects. Protected mock sets and
active contests start from empty files without these practice packs.

## Test and explain

Try no return route, all zero rewards, a two-city cycle, a high cost, unequal
directed roads, multiple ways to reach the same day/city state and a better
trip that repeats a cycle. Choose a tiny reward/cost case with a useful horizon
of at most eight days; enumerate walks through that horizon and
compare only walks that return to city 1; this uses a different schedule from
the reference queue. Check the full city/road/reward bounds separately.

A layered implementation takes O(H*(N+M)) time and O(N+M) memory with two
day layers, for H<=1000. Keeping all layers costs O(H*N+M) memory. Explain
the reference's queue overhead and why nonnegative rewards bounded by 1000
and the cost bound keep stored rewards and C*T*T within Java int range.
Record a state trace, source changes and two changed cases, then reconstruct
the recurrence from an empty file in a later session.

The reference repair changes only four adjacency-list lines to typed lists
that compile without raw-type or unchecked warnings. The priority-queue
algorithm is retained. `legacy/Main.java` preserves the original bytes.
