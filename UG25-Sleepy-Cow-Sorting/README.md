# Sleepy Cow Sorting

Optional Gold practice after sorting and Fenwick ordering/range prerequisites. Keep learner and reference attempts separate. The guides support independent study and the same pauses in a shared walkthrough.

- [Learner guide and five marked tasks](starter/README.md)
- [Preserved Java reference and explanations](solution/README.md)

Each role includes `Main.java`, `sample.in` and a complete native workflow. The Java reference is unchanged from `3c944ee24b4a55671b4e43d3cc0aa2e2101ce853`. The preserved historical Java reference stores zero-based values and queries an inclusive prefix at the current value before marking it. Because the permutation is unique and that value is still absent, this counts strictly smaller inserted values. The reference need not end its final move line with a newline. On K=0 it writes only the count line; token-based validation accepts no move tokens. The learner writes an explicit blank move line when completed with K=0.

Native gate: `python3 tests/verify-fenwick-practice-packs.py --javac javac --java java`. A structural pair count is not native algorithm acceptance. Site import promotion requires the exact accepted source revision.
