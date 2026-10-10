# Gold MooTube practice

Use this optional practice after the Gold disjoint-set and sorting lessons.
The required native setup checkpoint is a separate project.

- `starter/` contains an unfinished, compilable learner source, a sample and
  a standalone guide with six explicit tasks.
- `solution/` retains the completed historical Java source unchanged, plus
  the same sample and a reference comparison guide.

Begin with the learner role. Predict the sample, trace the active components,
complete the tasks, retain the attempt, then compare the reference. A student
can use each role guide independently; an instructor can pause at each trace,
invariant and changed-case check. Both roles use native `mootube.in` and
`mootube.out`, with JDK 17 or newer. The learner refuses to fabricate answers
while unfinished. Its input checks do not alter the historical reference.

Acceptance: `python3 tests/verify-mootube-pack.py` from the repository root.
The dedicated hosted workflow checks JDK 17 and 21, independent tiny-tree
traversal answers, the maximum chain/query bounds, original-order output,
untouched learner behavior, refusal behavior and preserved reference bytes.
Successful source acceptance is required before enabling the site's import
action; folder presence alone does not establish that workflow.
