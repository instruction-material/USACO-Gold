# Balanced Photo

Optional Gold practice after sorting and Fenwick ordering/range prerequisites. Keep learner and reference attempts separate. The guides support independent study and the same pauses in a shared walkthrough.

- [Learner guide and five marked tasks](starter/README.md)
- [Preserved Java reference and explanations](solution/README.md)

Each role includes `Main.java`, `sample.in` and a complete native workflow. The Java reference is unchanged from `3c944ee24b4a55671b4e43d3cc0aa2e2101ce853`. The unchanged historical Java reference sorts negated heights and maps each distinct height to its original index. Its inclusive prefix includes the current index, but that position is still unmarked, so it equals the strict-left count. The tracked sample input remains unchanged. The historical answer file contained a nonnumeric control byte; its original byte is retained in the audit evidence and the current sample answer is corrected to 3. An included answer file is an example, not evidence of a successful new run.

Native gate: `python3 tests/verify-fenwick-practice-packs.py --javac javac --java java`. A structural pair count is not native algorithm acceptance. Site import promotion requires the exact accepted source revision.
