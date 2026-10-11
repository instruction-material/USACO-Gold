# Reference: Cow Poetry: Ordered Lines and Rhyme Groups

This exported reference role contains the complete algorithm. Predict the results and preserve the learner attempt before running it.

This required counting project connects syllable-state dynamic programming with choices across repeated rhyme groups. Work from a written prediction to an unfinished learner, then compare the separate reference. The contract, reasoning and checks support independent study or an instructor walkthrough.

## Contract

Read `poetry.in`: `N M K`, then N pairs of syllable lengths and rhyme-class numbers, then M uppercase scheme letters. Bounds are N and K from 1 to 5000, M from 1 to 100000, word lengths from 1 to K, and class numbers from 1 to N. A word may be reused. Word identities and their order distinguish lines. Each line totals exactly K syllables. Equal scheme letters require equal final rhyme classes; different letters may use the same class. Write the poem count modulo 1000000007 to `poetry.out`.

The [official Cow Poetry contract](https://usaco.org/index.php?page=viewproblem2&cpid=897) defines the contest bounds. The maintained fixtures use the official sample. The previously supplied larger input and answer remain byte-for-byte under `legacy/solution/`.

## Prediction

```text
3 3 10
3 1
4 1
3 2
A
B
A
```

Expected output:

```text
960
```

Treat the two length-three words as different word choices. There are eight complete lines ending in class 1 and four ending in class 2. The two A lines have 8*8 + 4*4 = 80 choices; the B line has 8 + 4 = 12. Their product is 960. Requiring B to use a different class would incorrectly discard poems.

## State and reasoning

Let a prefix state count ordered word sequences at a syllable total. The empty sequence provides one way to reach total zero. Appending a word increases that total by its positive length, so smaller totals can be processed first. Iterate over word identities, even when lengths or classes coincide.

Separate the last word from its prefix to group complete-line counts by the last word's rhyme class. For each scheme letter, choose a class once and choose the required number of lines independently within that class. Sum these choices over classes, then multiply the results for different letters. Skip unused letters. A class with no complete lines contributes zero for a used letter.

Normalize additions, multiplications and powers modulo 1000000007. Java long safely holds the product of two normalized residues. Repeated squaring avoids a loop for every exponent value. With N words, K syllables and at most 26 scheme letters, a direct plan uses O(N*K + M + 26*N*log M) time and O(N+K) extra state. The provided parser retains letter frequencies rather than all M letters.

## Tasks and walkthrough

`Main.readInput(String)` provides bounds checks, arrays and zero-based rhyme-class indices. File reading and guarded writing are provided. `countPoems(Input input)` remains unfinished.

1. Define the prefix-count state, its empty base case and ordered append transitions.
2. Count complete lines by their final word's rhyme class.
3. Combine each used scheme letter's choices and return a normalized result.

For a walkthrough, explain the empty sequence, trace totals three and four, derive the sample's ending counts and compare schemes AB and AA. Record predictions before opening the reference. The supplied learner contains no counting implementation. An untouched run exits with status 2 and writes no new answer; any existing answer is preserved.

## Independent checks

- With one length-one word, K=1 and scheme AAA, there is one poem.
- With two length-one words in different classes and K=1, AB gives 4 poems while AA gives 2.
- With those words in the same class, AA gives 4 because both line choices remain independent.
- With two length-two words and K=3, no complete line exists, so the answer is zero.
- For tiny K, recursively enumerate actual sequences of word identities and tally their last classes. Enumerate poem line choices or calculate rhyme-group products from those independent tallies.
- At N=K=5000 with every word of length 5000 and class 1, a scheme of 100000 A letters has answer 5000^100000 modulo the modulus. Splitting words equally between two classes changes it to twice 2500^100000 modulo the modulus. These constructions also exercise the actual advertised input limits.

Alter syllable lengths, a final class and a repeated scheme letter separately. Explain each result before running. Save the learner attempt before comparison; a matching sample alone does not establish correctness.

## Build and run

Use a native JDK 17 or newer. Keep this role's `Main.java` and `poetry.in` together, then enter that folder. Compile only this role. On macOS or Linux:

```sh
javac --release 17 -Xlint:all -Werror Main.java && java -ea -Xmx256m Main && cat poetry.out
```

In PowerShell:

```powershell
javac --release 17 -Xlint:all -Werror Main.java
if ($LASTEXITCODE -eq 0) { java -ea -Xmx256m Main }
if ($LASTEXITCODE -eq 0) { Get-Content -LiteralPath poetry.out }
```

The display command runs only after success. An old answer file is not evidence that an unfinished or failed run succeeded. The provided learner diagnoses missing or malformed input before writing. The reference expects contract-valid input and writes 960 for the sample. Preserve expected results separately, edit the input intentionally and save source changes before rerunning.

The site workspace saves and exports native Java source when the verified resource import is enabled. Its Java preview is not a complete JDK. Native source acceptance and actual site import/export acceptance are separate gates.

## Reference and provenance

The supplied reference algorithm is unchanged. The active input and expected answer now match the sample taught above; original fixture bytes remain archived. Exact earlier committed placeholder guides are preserved under the pack's `legacy/` directory. Consult the completed reference after deriving the states and recording changed-case predictions. Neither source-file presence nor the unfinished learner grades a completed student algorithm.
