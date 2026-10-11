# Shortcut learner: selected routes and cow traffic

This optional application follows weighted shortest paths and tree rooting.
The supplied `shortestRoutes` helper selects routes; complete the four marked
tree-traffic tasks in `solve`. Work independently or pause at each prediction
with a course facilitator. Preserve prior work and change the cases on a retry.

## Full input and output contract

The barn is field 1 in a connected undirected graph. Each cow takes its shortest
usual route toward the barn. Ties prefer the smaller field label at the first
differing step when reading toward the barn. Add one trail of length T from a
chosen field to the barn. Cows use it only when their existing route encounters
that field and the remaining trip becomes shorter. Do not reroute other cows.

`shortcut.in` starts with `N M T`: N in 1..10000, M in N-1..50000 and T in
1..10000. The next line contains N cow counts, each in 0..10000. Exactly M
following records contain `a b time`, with endpoints in 1..N and positive times
in 1..25000. Every field reaches the barn. Parallel trails and positive loops
are accepted because the statement does not exclude them. N=1, M=0 is valid.
`shortcut.out` contains one integer, the greatest reduction in total cow travel
time. Use `long` for traffic and savings. Indices in the program start at zero.

## Predict, implement and explain

On the sample, field 4 chooses 4,2,1 over the equal-time route 4,3,1. Field 5
chooses 5,3,1 over 5,4,2,1. A shortcut at field 5 saves 8 units for each of its
five cows, giving 40. Cows from field 4 keep their original route and do not
detour toward the new shortcut. The original total is 101; the new total is 61.

1. Build child lists from the supplied parent array. Explain why the tie rule
   compares the next step toward the barn and why positive weights prevent cycles.
2. Compute each field's traffic from its own cows and its children's traffic.
   Use an iterative postorder so a 10000-field chain does not depend on recursion.
3. Evaluate `traffic[v] * max(0, distance[v] - T)` for cows that meet the shortcut
   on their usual route. Multiply in `long` and keep those routes fixed.
4. Return the greatest total saving and justify zero-benefit and tied-route cases.

Do not replace the supplied input driver or helper. `solve` is intentionally
unfinished. Untouched valid runs exit with status 2 and produce no answer file.
Refused or unfinished runs preserve earlier output. The range guard does not
grade whether a completed algorithm is correct.

## Check and revisit

Check a single barn, zero cows, a shortcut slower than every suffix, a tied
diamond, changed cow counts, reversed trail records, parallel trails and loops.
For tiny graphs, enumerate simple routes to the barn, select the least
`(time, field-label sequence)`, and simulate which cows meet each candidate on
their unchanged route. Compare parents, subtree traffic and savings. Keep the
oracle small and exercise teaching bounds separately. Save two changed cases
and a trace before comparing a reference; finish with a later empty-file retry.

The supplied helper costs O((N+M) log(M+1)) time and O(N+M) storage. Iterative
tree aggregation and the candidate sweep add O(N) time and storage. Sorting by
descending distance is an alternative O(N log N) order. Explain why every child
has greater distance than its parent. Source checks validate drivers and
helpers, not a completed learner submission.

## Save and run

Keep Main.java, README.md and shortcut.in together. Retain source and custom
inputs when downloading a ZIP. Use a native JDK 17 or newer:

```text
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
```

The commands also work in PowerShell. Check the exit status, then read
shortcut.out using `cat shortcut.out` or `Get-Content shortcut.out`. Earlier
output is not evidence of a successful new run. The browser IDE saves and
exports this native file-I/O pack; its preview does not execute the application
or replace shortcut.in. Protected mocks and live contests start from an empty
file without this practice starter or a reference.
