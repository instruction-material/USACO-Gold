# Fruit Feast reference

This native Java reference assumes valid [USACO Fruit Feast](https://usaco.org/index.php?page=viewproblem2&cpid=574) input. Its historical snapshot remains in Git history; the current version corrects the water-transition explanation and makes the diagnostic trace optional. No completed learner pack or site IDE import is implied.

## Contract and reasoning

Read one line containing T, A and B from `feast.in`. Fullness stays between 0 and T, where T is at most 5000000 and both fruit sizes are between 1 and T. Eating adds either fruit size. Water is optional, can be used once, and changes fullness x to floor(x/2). Write the greatest reachable fullness as one integer to `feast.out`.

The two boolean states distinguish fullness before and after water. Positive fruit sizes allow the eating transitions to be processed in increasing fullness order. A target fullness t just after drinking can come from previous fullness 2*t or 2*t+1. The second phase also considers eating after water. The final backward scan considers both states because water need not be used.

For T=8, A=5 and B=6, eating 6, drinking to reach 3, then eating 5 reaches 8. Without water, the reachable values are 0, 5 and 6. After water, 0, 2 and 3 provide starting values for further eating. Explain these states before inspecting the loops.

## Native run and optional trace

Use JDK 17 or newer in a working copy of this folder. Preserve existing inputs and answers before changing cases. For the official sample:

```sh
printf '8 5 6\n' > feast.in
javac -encoding UTF-8 Main.java
java Main
cat feast.out
```

The answer is `8`; the normal run produces no terminal diagnostics. In PowerShell, create this ASCII input with `Set-Content -Encoding ascii feast.in '8 5 6'`, then use `Get-Content feast.out` to read the answer.

For a small-state walkthrough, use `java Main --trace`. This prints each fullness considered in the water phase while keeping the answer in `feast.out`. The trace grows to T+1 lines, so use it for a deliberately small case. It is not the answer stream.

## Check and explain

Check T=1, equal fruit sizes, a case helped by water, a case requiring no water, and a case in which both fruit sizes exceed T/2. For tiny limits, independently explore states `(fullness, waterUsed)`: add either fruit when capacity permits and halve fullness only before water has been used. Compare the greatest visited fullness with the answer file.

The supplied verifier checks twelve such small cases, three large cases with independent expected values, and the explicit sample trace. It also checks that reference source and existing course inputs remain unchanged during verification. These cases support the reference correction; they do not grade a learner implementation or establish a formal judge runtime or memory guarantee. The reference assumes valid input rather than providing a validated learner driver.

From the repository root, run `python3 tests/verify-fruit-feast-reference.py --javac javac --java java`. Hosted checks repeat on JDK 17 and 21.
