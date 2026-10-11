# USACO Gold

Source material for the Gold course. These C++20 projects provide separate learner and completed-reference packs with fixtures and assignment guides:

- [Fibonacci dynamic programming](UG1-Dynamic-Programming-with-Fibonacci/README.md): core state definition, base cases, transition and evaluation order.
- [Marathon Gold](UG5-Marathon/README.md): optional point-update and range-query practice using mutable checkpoints and sum/maximum segment trees. This implements the 2014 Gold contract.

Each guide explains the contract, predictions, learner tasks, examples, independent checks, and native build command. Start with the `starter/` pack, retain the learner attempt, and compare the separate `solution/` reference after an attempt. The other course folders retain their existing material.

Repository acceptance: `python3 tests/verify-gold-packs.py --compiler c++ --mode ordinary`. Use `--mode sanitized` for address and undefined-behavior checks. The pinned hosted workflow repeats both modes with GCC and Clang. Checks compile both roles, execute actual file I/O, compare independent models, cover the advertised limits, and require untouched learner tasks to remain unfinished.

## Native Java packs

The following guides provide native Java learner and reference roles with
separate contracts and verification steps:

- [Gold setup checkpoint](UG0-Contest-Contract/README.md): standard input/output and 64-bit totals before algorithm lessons.
- [0-1 Knapsack demonstration](UG2-0-1-Knapsack/README.md): small edited datasets, optimal subsets and single-use traceback.
- [Fruit Feast](UG40-Fruit-Feast/README.md): optional before/after-water reachability with native file input and output.
- [Dijkstra shortest paths](UG9-Dijkstras-Algorithm/README.md): priority-queue distances, path validation and unreachable vertices.
- [Dijkstra II matrix comparison](UG9-Dijkstras-Algorithm-II/README.md): optional dense storage, row-scan costs and the same shortest-path invariant.
- [Minimum spanning tree](UG14-MST/README.md): Prim's algorithm, predecessor edges and a 64-bit tree total.
- [Fenwick tree](UG22-Binary-Indexed-Tree-Fenwick-Tree/README.md): point updates, prefix sums and range sums.
- [MooTube](UG21-Moo-Tube/README.md): optional weighted DSU and descending offline-query practice.
- [CircleCross](UG24-Why-Did-the-Cow-Cross-the-Road-III/README.md): optional interval and Fenwick crossing practice.
- [Snow Boots](UG27-Snow-Boots/README.md): optional descending-depth sweep and surviving-path gap practice.
- [Balanced Photo](UG23-Balanced-Photo/README.md): optional taller-side counts and strict imbalance checks.
- [Sleepy Cow Sorting](UG25-Sleepy-Cow-Sorting/README.md): optional optimal front-move plans and a growing sorted suffix.
- [Out of Sorts, Gold](UG26-Out-of-Sorts/README.md): optional bidirectional sweeps, stable ties and cut counts.

Each role guide is usable independently and includes native build/run
commands, predictions and changed-case checks. Retain the learner attempt
before consulting its separate reference. These programs run natively; the
site IDE saves and exports them and provides build directions.

The source manifest records the current structural inventory, including
remaining placeholder roles. A source file's presence is not proof of
algorithm correctness or an accepted site import. Use each pack's dedicated
acceptance before promoting its import action.

DP role acceptance: `python3 tests/verify-dp-learner-packs.py --javac javac --java java`. This compiles both learner scaffolds, checks their drivers and preserved answers, and repeats independent reference checks. The tiny driver probes do not complete learner algorithms.

## Optional tree-path and bounded-time graph packs

[Milk Visits](UG-Milk-Visits/README.md) practices Euler ancestry and active-path
type state with an iterative full-depth reference. [Time is Mooney](UG-Time-is-Mooney/README.md)
practices bounded-time directed-graph DP and the return-trip penalty. Both
provide unfinished learners, independently checked references, standalone role
guides and native JDK commands. Original bytes remain archived; role presence
alone does not qualify a pack for site imports.

## Optional road sensitivity pack

[Roadblock](UG10-Roadblock/README.md) follows core weighted graphs with candidate-
path reasoning and restored single-road experiments. It supplies a dense
shortest-path helper, a distinct unfinished learner and full native workflow
guidance. The historical reference is unchanged. Site imports and saved-project
identity preservation are a separate acceptance step.

## Optional shortest-route tree and traffic pack

[Shortcut](UG11-Shortcut/README.md) follows weighted shortest paths and tree
rooting with route-tie reasoning, iterative traffic aggregation and shortcut
savings on fixed usual routes. It supplies a shortest-route helper and a
distinct unfinished learner, full standalone role guides and native JDK
commands. The reference retains its route and traffic algorithms with six
typed-adjacency changes; exact original bytes remain archived. Dedicated native
acceptance checks independent route choices, teaching bounds and preserved
learner answers. Site placement and imports require separate acceptance.

## Advertised implementation labs

- [Dynamic programming practice](UG1-Dynamic-Programming-Practice/README.md): rolling state, grid order and recursive item choices with the first-item base case corrected.
- [MST II](UG14-MST-II/README.md): priority-queue Prim with a dense matrix, stale-entry handling and long totals.
- [Disjoint sets and Kruskal](UG19-Disjoint-Sets-and-Kruskals/README.md): union by size, cycle decisions and explicit optional tracing.

Each has a distinct unfinished learner, a standalone reference guide and exact preserved historical source. Accept with `python3 tests/verify-implementation-labs.py --javac javac --java java` before promoting site imports.

## Optional historical applications

- [Cow Routing](UG13-Cow-Routing/README.md): Silver-origin bridge practice with ordered tickets and lexicographic shortest paths.
- [Watering the Fields](UG16-Watering-the-Fields/README.md): Silver-origin bridge practice with an implicit eligible-edge MST.
- [I Would Walk 500 Miles](UG18-I-Would-Walk-500-Miles/README.md): Gold maximum-spacing clustering with an implicit complete graph.
- [Talent Show](UG2-Talent-Show/README.md): Gold ratio feasibility, clamped minimum-weight DP and integer binary search.

Each now has a distinct unfinished Java learner and standalone role guides. Original reference bytes are preserved; only misleading comments are corrected. Run `python3 tests/verify-historical-algorithm-packs.py --javac javac --java java` before promoting site imports. These four applications keep their optional purposes. The accepted catalog now assigns their transfer rows distinct verifier/extension work using five native packs. The ten older generic arithmetic folders are retained as inactive legacy support in `SOURCE_BACKLOG.md`, preserving recovery context without treating them as active assignments.

## Optional Hoof, Paper, Scissors application

The switch-budget DP folder now contains distinct learner/reference roles with complete guides. Use `python3 tests/verify-hps-pack.py --javac javac --java java` to verify independent gesture-sequence answers and learner file boundaries. Original reference statements and official sample bytes remain unchanged; source acceptance does not establish site import readiness.

## Current catalog inventory

The 47 current Gold catalog targets contain 34 structurally distinct starter/reference pairs and 13 remaining counterpart gaps. Ten additional generic arithmetic snapshots remain in place as inactive legacy support, giving 57 retained folders in total. Counts are not a claim of full algorithm or site readiness. See `COURSE_SOURCE_MANIFEST.md` and `SOURCE_BACKLOG.md` for the current boundary.

## Spanning-tree objectives and interval merges

`UG15-Superbull`, `UG17-Moocast` and `UG6-248` now have distinct four-task unfinished Java learners and complete independent role guides. Superbull preserves its maximum-score purpose and original Silver contest attribution; Moocast minimizes a connectivity threshold rather than an edge sum; 248 maximizes any produced tile rather than requiring the full sequence to collapse. The Superbull and 248 reference source files are unchanged. Moocast retains exact original working bytes under `legacy/`; its only executable edit compares the int sentinel actually used, and three changed comments explain the bottleneck objective. Dedicated JDK 17/21 checks use elimination sequences, threshold flood-fill and adjacent merge reachability, plus full-size constructions and preserved learner-output boundaries. Structural presence, native acceptance and consent-based site activation remain separate gates.

## Fenced In memory boundary

The grid-MST pack now has a distinct unfinished learner, complete role guides and a reference that stores primitive edge keys instead of millions of objects. The original disjoint-set logic and graph are preserved. Exact old working bytes remain under `legacy/`. Dedicated JDK 17/21 acceptance tests exhaustive tiny spanning trees, full 2000-by-2000 constructions under a 256 MiB heap, one-orientation cases and learner file boundaries. Site activation is pending its own acceptance.
