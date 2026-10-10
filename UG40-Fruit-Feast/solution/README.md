# Fruit Feast reference

This optional state-design project follows the unit's basic DP examples. It models unlimited fruit choices and one optional water transition. Use the distinct `starter/` for an attempt, then compare the preserved `solution/` reference. Each role guide provides the full contract and native commands independently.

## Contract, limits and sample

The [official USACO Gold Fruit Feast statement](https://usaco.org/index.php?page=viewproblem2&cpid=574) specifies one line `T A B` in `feast.in`, where `1 <= T <= 5000000` and `1 <= A, B <= T`. Starting at fullness zero, eating either fruit adds its size without exceeding T. Water can be used at most once and changes fullness x to floor(x/2). It is optional. Write the greatest reachable fullness as one integer followed by a newline to `feast.out`.

The sample in `sample.in` is `8 5 6`; its answer is 8. Eat the fruit of size 6, drink to reach 3, then eat the fruit of size 5. Before water, only 0, 5 and 6 are reachable. Halving them seeds 0, 2 and 3, after which eating can reach 8. A valid solution also retains the before-water maximum because some cases need no water.

## States, tasks and walkthrough

Keep separate reachable states before and after water. Positive fruit sizes permit eating transitions in increasing fullness order. Seed the second phase by halving every reachable first-phase fullness, then allow only eating in that phase. In the preserved reference's equivalent target-based formulation, a post-water fullness t can come from pre-water fullness 2*t or 2*t+1.

The `starter/` leaves five algorithm tasks unfinished:

1. Allocate the before-water states and mark fullness zero.
2. Extend those states by eating either fruit.
3. Seed after-water states by integer halving.
4. Extend the seeded second phase by eating, with no second water transition.
5. Return the greatest reachable fullness across both phases.

The supplied driver validates the header and bounds, rejects extra input, and opens `feast.out` only after the solver succeeds. Untouched tasks exit with status 2 and preserve an existing answer file. The reference assumes valid contest input; its algorithm and existing sample files are unchanged by the learner restoration. Keep predictions and an attempt before consulting it.

Independently or with an instructor, list the sample's reachable states before coding. Explain why a positive fruit size permits ascending iteration and why the water-used flag must survive a transition. Predict a no-water case and a case helped by water, trace them, then compare the result with a small state-search oracle. Explain how the two phases prohibit a second drink.

The expected algorithm uses O(T) time and O(T) states. The learner can use two flat boolean arrays. The reference retains its historical two-column Java array representation, whose object overhead differs. Dedicated checks exercise the full limit with a local 256 MiB heap gate; this is verification evidence rather than an official judge resource guarantee.

## Native run and answer preservation

Use JDK 17 or newer in a working copy of the selected role. Preserve existing course inputs and answers before copying a case:

```sh
cp sample.in feast.in
javac -encoding UTF-8 Main.java
java Main
cat feast.out
```

In PowerShell use `Copy-Item sample.in feast.in` and `Get-Content feast.out`; the Java commands remain the same. The sample reference answer is 8 and its normal run writes no diagnostics to the terminal. The site IDE saves and exports this native Java pack; file input and execution use the local JDK.

The reference supports `java Main --trace` for a deliberately small walkthrough. It prints T+1 fullness values considered in its water phase while preserving the answer file. The learner driver takes no arguments. Avoid the reference trace at large T because it is diagnostic output rather than the answer stream.

## Independent checks

Check T=1, equal fruit sizes, a case helped by water, a case requiring no water, and fruits larger than T/2. For tiny limits, explore states `(fullness, waterUsed)` independently: add either fruit when it fits, and halve fullness only when water has not been used. Compare the greatest visited fullness with the answer file. A sample alone cannot validate an algorithm.

From the repository root run `python3 tests/verify-fruit-feast-reference.py --javac javac --java java` for the reference and `python3 tests/verify-dp-learner-packs.py --javac javac --java java` for the role contracts. Hosted checks repeat on JDK 17 and 21. Learner acceptance verifies compilation, refused inputs, untouched tasks, answer preservation and the supplied file driver using tiny independent probes. It does not complete the learner algorithm or grade a submitted solution.
