# Ordered tickets and lexicographic shortest paths: reference

Optional historical bridge practice after weighted shortest paths. It combines directed ticket portions with money-first, flight-count-second comparison. It complements core Dijkstra; it does not replace the Gold spine.

Source contract: [USACO, January 2015 Silver, problem 2](https://usaco.org/index.php?page=viewproblem2&cpid=512). The origin remains explicit even when this historical exercise appears in the Gold appendix.

## Contract

Read `cowroute.in`: `A B N`, then two lines for each route: `price stopCount` and the ordered city labels. There are 1..1000 routes, 1..100 stops per route, labels 1..1000, and prices 1..1000000000. A route has no repeated city. Buying a ticket permits any forward portion of that route for the same price; leaving and later boarding it again requires another ticket. Minimize total money, then flights among equal-money itineraries. Write `cowroute.out` as `money flights`, or `-1 -1` if unreachable. Use long money totals. Whitespace separates tokens; the learner driver checks all tokens and bounds before solving.

## Prediction

The official sample in `cowroute.in` is:

```text
3 4 3
3 5
1 2 3 4 5
2 3
3 5 4
1 2
1 5
```

Expected `cowroute.out`:

```text
2 2
```

One ticket costing 2 covers 3 to 5 to 4: two flights. The price-3 direct portion uses one flight but loses on money. A tied price-2 direct ticket would win on flights. Reverse travel along a route is not permitted.

## Tasks and walkthrough

1. Represent every forward portion by one ticket price and its number of flights; retain the best pair for repeated endpoints.
2. Define pair comparison and addition, minimizing money before flights and protecting unreachable sentinels.
3. Initialize distance pairs, visited flags and a zero pair at the starting city.
4. Select and relax vertices with the same pair ordering; return the destination pair or explicit unreachable output.

This is the preserved historical algorithm for comparison after a saved attempt. Its driver assumes a complete valid input within the stated contract. Exact original working bytes are in `../legacy/Main.java`. Only inaccurate comments are corrected in the maintained source; its parsing, arithmetic and algorithm statements are unchanged.

For independent study or an instructor walkthrough: predict the sample, explain the state and invariant, trace one transition, implement and save an attempt, and compare a changed tiny case against an independent model. Open the separate reference after the attempt; preserve the original attempt when retrying or comparing variants.

## State and reasoning

A vertex stores the best money/flights pair found so far. All ticket costs are positive, so settling the least unvisited pair is safe. A selected portion from stop i to j uses j-i flights but pays once. Lexicographic comparison is used both for direct portions and complete itineraries. An optimal itinerary has no repeated city: removing a positive-cost cycle improves money. Its flights therefore number at most 999; the historical unreachable test uses this fact.

## Build and run

Use JDK 17 or newer inside this role's working folder. These commands also work in PowerShell:

```sh
javac --release 17 -encoding UTF-8 Main.java
java Main
```

Keep `cowroute.in` beside `Main.java`; read `cowroute.out` afterward. The guarded learner parses the complete input, solves and validates the result before opening output, preserving a prior answer on unfinished or refused work. The site IDE can save and export native Java; this program requires native execution and is not run by the Input panel. Source acceptance and confirmed site imports are separate gates.

## Independent checks

Compare tiny itineraries with bounded boarding-by-boarding relaxation rather than another Dijkstra implementation. Test a money tie with unequal flight counts, reverse-only routes, unreachable destinations, start equal to destination, competing direct portions, repeated ticket purchases and a total above int. The full-limit construction uses 1000 routes, city 1000 and an eleven-billion ticket total. The dense reference takes O(1000^2 + sum(stopCount^2)) time and O(1000^2) space.

From the repository root run `python3 tests/verify-historical-algorithm-packs.py --javac javac --java java`. Hosted acceptance repeats with JDK 17 and 21. Temporary driver probes check supplied infrastructure only; they do not complete or grade the saved learner algorithm.
