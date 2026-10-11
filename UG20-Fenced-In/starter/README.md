# Fenced In learner

Four algorithm tasks remain unfinished.

## Contract

USACO February 2016 Gold, problem 3: [Fenced In](https://usaco.org/index.php?page=viewproblem2&cpid=623). Read `fencedin.in`: `A B n m`, then n vertical positions and m horizontal positions. A and B are 1..1000000000; n and m are 0..2000. Positions within each orientation are distinct and strictly inside the corresponding outer boundary. Input positions need not be sorted. Write the minimum total removed length to `fencedin.out`, using a 64-bit total. The outer fence is not a candidate for removal. This is native Java with JDK 17 or 21 and a 256 MiB teaching heap.

## Prediction

The supplied official sample has A=B=15, vertical positions 2,5,10,6,4 and horizontal positions 11,3. Predict 44, then trace the cheapest connections. Before coding, predict: no interior fences gives 0; only m horizontal fences gives m*A; only n vertical fences gives n*B. A larger answer can exceed a 32-bit integer.

## Tasks and walkthrough

1. Draw the regions, sort coordinates with outer boundaries 0/A and 0/B, and compute gaps.
2. Map each region to `column + row*(n+1)`. A horizontal dividing segment has the column width; a vertical dividing segment has the row height. Explain why crossing direction and removed-segment length differ.
3. Remove increasing-cost segments only when they join different components. Stop after `(n+1)*(m+1)-1` successful joins. Describe why a cycle can be omitted without losing connectivity.
4. Keep a long total, verify zero dimensions and tied gaps, and evaluate the memory cost before running the full boundary.

Learner work can be read independently or walked through with an instructor: predict, explain a state, implement, compare independent checks and describe a failure. Preserve the first attempt before using the reference. A later changed-case retry should close the reference and change ordering, dimensions or gap lengths.

## State and reasoning

Vertices are enclosed regions; each candidate edge is a fence segment between neighboring regions. A minimum spanning tree minimizes the total removed length, not the largest individual opening. The reference retains Kruskal and weighted disjoint sets. It packs a positive weight in the high 32 bits of a long and the original construction index in the low 32 bits. The index recovers the same endpoints after sorting. There are `(n+1)*m + (m+1)*n` edges. At n=m=2000 the primitive edge array and two disjoint-set arrays contain about 92 MiB of payload, before VM/sorting overhead; native acceptance uses `-Xmx256m`. Never divide by a zero dimension: the corresponding orientation has no edges. The algorithm uses O(E log E) time and O(E+V) memory.

## Build and run

Export the chosen role to its own folder. Keep `Main.java`, this guide and `fencedin.in` together. Open a terminal in that folder. The browser IDE can edit/export these files; its ordinary Input panel is not native file input. It cannot validate this heap-bound reference in a browser Java runner.

On macOS/Linux with JDK 17 or 21:

```sh
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
java -ea -Xmx256m Main
status=$?
if [ "$status" -eq 0 ]; then cat fencedin.out; else printf 'Run failed with exit status %s\n' "$status"; fi
```

On PowerShell:

```powershell
javac --release 17 -encoding UTF-8 -Xlint:all -Werror Main.java
if ($LASTEXITCODE -eq 0) {
    java -ea -Xmx256m Main
    if ($LASTEXITCODE -eq 0) { Get-Content fencedin.out }
    else { Write-Host "Run failed with exit status $LASTEXITCODE" }
}
```

Check the exit status before reading the answer; an older output file is not evidence that the current run succeeded. The unfinished learner exits 2 and preserves an earlier output. Learner input guards reject missing, extra, out-of-range or repeated positions before the algorithm tasks. The historical reference expects valid contest input; no malformed-input guarantee is made for it. Keep learner/reference work in separate export folders and saved attempts.

## Independent checks

Compare tiny grids against enumeration of all candidate spanning trees with independent flood-fill connectivity. Check unsorted positions, equal gaps, one region, either zero dimension and swapped axes. Full-size constructions include 2000-by-2000 fences with unit gaps (4004000), unequal constant gaps with a total above 32 bits, and varied column gaps to exercise sorting. Check both single-orientation boundaries with a 2000000000000 total. The source acceptance runs actual role ZIP exports on JDK 17/21 with a 256 MiB heap, preserving unfinished learner outputs and source files. Native source acceptance and confirmed site imports remain separate gates.
