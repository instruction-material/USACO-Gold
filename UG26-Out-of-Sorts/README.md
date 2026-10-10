# Out of Sorts, Gold bidirectional sweeps

Optional Gold practice after sorting and Fenwick ordering/range prerequisites. Keep learner and reference attempts separate. The guides support independent study and the same pauses in a shared walkthrough.

- [Learner guide and five marked tasks](starter/README.md)
- [Preserved Java reference and explanations](solution/README.md)

Each role includes `Main.java`, `sample.in` and a complete native workflow. The Java reference is unchanged from `3c944ee24b4a55671b4e43d3cc0aa2e2101ce853`. The unchanged Java reference uses a stable object sort comparing values, marks original positions, and queries each inclusive prefix. Its subtraction comparator is safe within the published nonnegative range, whose difference fits int. Preserve tie order when translating the reference; do not substitute the Silver maximum-displacement formula.

Native gate: `python3 tests/verify-fenwick-practice-packs.py --javac javac --java java`. A structural pair count is not native algorithm acceptance. Site import promotion requires the exact accepted source revision.
