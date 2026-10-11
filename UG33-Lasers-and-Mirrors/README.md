# Lasers and Mirrors: Line States and Fewest Turns

This required graph-modeling project treats a beam direction as a line state. The task is to find the fewest right-angle reflections, rather than a shortest physical distance. The complete contract, sample, provided input helpers and independent checks support either a standalone attempt or an instructor walkthrough.

## Contract

There are 1 to 100,000 distinct posts. Every coordinate is an integer from 0 through 1,000,000,000. Posts are distinct from the laser and barn. A mirror at a post changes a horizontal beam to a vertical beam, or the reverse. Leaving a post without a mirror allows straight travel through it. The initial beam may point along either axis.

Read `lasers.in`: the first line contains `N xLaser yLaser xBarn yBarn`, followed by `N` post coordinate pairs. Write one integer to `lasers.out`: the minimum mirror count, or `-1` if the barn cannot be reached. A direct horizontal or vertical beam needs zero mirrors.

The official statement is [USACO Lasers and Mirrors](https://usaco.org/index.php?page=viewproblem2&cpid=671). The sample input is included in each role. The reference expected-output fixture is corrected to 1; its original blank answer is archived.

## Prediction

```text
4 0 0 7 2
3 2
0 2
1 6
3 0
```

Expected output:

```text
1
```

A mirror at `(0,2)` turns the beam from the laser's vertical line onto the barn's horizontal line. A post such as `(3,2)` can be passed without adding another mirror. The two endpoints share neither coordinate, so zero mirrors cannot solve this sample.

Before implementation, draw the laser lines, the barn lines and the line pair at each post. Count reflections rather than crossed posts or coordinate distance.

## State and reasoning

Use separate identities for vertical and horizontal lines, even when their numeric coordinates are equal. The provided `xLine(x)` helper returns `-x-1`; `yLine(y)` returns `y`. Thus `xLine(0)` is `-1` and `yLine(0)` is `0`. The largest coordinate also fits this encoding in a Java `int`.

Each post joins its vertical line to its horizontal line. Crossing that graph edge represents one reflection. Seed both lines through the laser at distance zero. Reaching either line through the barn completes a straight final segment without another reflection.

Breadth-first search processes nondecreasing edge counts. Mark a line when first discovered so cycles and repeated coordinates do not repeat work. Each post contributes two adjacency entries; expected hashing time and storage are linear in the number of posts. A physical grid containing every possible coordinate would be much larger and is unnecessary.

## Tasks and walkthrough

The supplied parser validates counts, coordinate bounds, distinct posts and trailing input. File reading, line encoding and writing are provided. `minimumMirrors(Input input)` remains unfinished.

1. Build the two-way line adjacency lists from the posts.
2. Add both initial line states with distance zero to a queue and distance map.
3. Repeatedly remove a line, test the barn-line condition and discover its unvisited neighboring lines at one greater distance.
4. Return `-1` when the queue is exhausted. Keep this result distinct from a reachable zero-mirror path.

The initial method throws an unfinished-task exception. It exits with status 2 and writes no new answer. A previously existing `lasers.out` is preserved. The starter contains no mirror-search implementation.

## Independent checks

- For `1 0 0 1 1` with the only post `(2,2)`, neither initial line reaches any usable post. The answer is `-1`.
- Move that post to `(0,1)`. The answer becomes `1`.
- For endpoints `(0,0)` and `(0,5)` with an unrelated post `(9,9)`, the answer is `0`.
- Repeated x coordinates and repeated y coordinates are valid when whole post locations remain distinct.
- Include coordinates zero and one billion to check the line namespaces.
- For a tiny input, construct a separate graph of actual points. Connect two points when they share a coordinate. The minimum number of straight segments minus one is the mirror count; an unreachable barn has answer `-1`. This model checks the line-state implementation using a different representation.

A full-size construction can alternate posts `(1,0), (1,1), (2,1), (2,2), ...` and place the barn just beyond the final turn. Check the exact turn count and completion with 100,000 posts, using a native heap bound instead of a browser Java preview.

Walkthrough checkpoints are the state identities, the two initial states, the first two queue layers, the exhausted-queue result and a changed-case prediction. Compare the complete reference only after recording the model and expected results.

## Build and run

Use a native JDK 17 or newer. Enter the chosen `starter` or `solution` folder, with `Main.java` and `lasers.in` together. Compile only that role's `Main.java`.

On macOS or Linux:

```sh
javac --release 17 -Xlint:all -Werror Main.java && java -ea -Xmx256m Main && cat lasers.out
```

In PowerShell:

```powershell
javac --release 17 -Xlint:all -Werror Main.java
if ($LASTEXITCODE -eq 0) { java -ea -Xmx256m Main }
if ($LASTEXITCODE -eq 0) { Get-Content -LiteralPath lasers.out }
```

An unfinished learner exits 2, so the final display command is skipped. A completed sample run writes `1`. Save source edits separately from expected results, change the input deliberately, and recompute the expected answer before another run. The site workspace can import and export this native source once its verified resource entry is enabled; it does not execute a complete native JDK.

## Reference and provenance

The reference `Main.java` retains the supplied breadth-first search with the unreachable default corrected to `-1`. Its line-encoding comment now describes the actual nonnegative coordinate contract. The `legacy` directory preserves the exact committed bytes of every modified supplied file from source revision 47262a7e6819ee20081a19716dd69fac1fe8e702. The reference expects contract-valid input; the learner's provided parser also diagnoses malformed input before an answer is written.

Source presence and this guide do not establish completed learner grading or site import acceptance. Those require the native source and actual import/export gates for this pack.
