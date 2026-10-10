# Gold setup: contest input/output checkpoint

This is an authored setup exercise, not an official contest problem. It checks that the chosen native Java workflow reads a complete input, uses a 64-bit result and prints only the required answer. It requires arrays and loops from Silver; it does not require DSU, MSTs or another Gold algorithm.

## Contract

Read `N` followed by exactly `N` signed integer values from standard input. Whitespace may separate tokens across lines. The maintained practice bounds are `0 <= N <= 200000` and `-1000000000 <= value <= 1000000000`.

Print the sum followed by one newline. Print `0` for no values. Do not print prompts, labels or debugging text. Missing tokens, invalid integers, out-of-range values and extra tokens are refused with status 2 and no answer. The supplied parser validates the whole input before the learner calculation runs.

The result may reach positive or negative 200000000000000. Store the running total in a Java `long`; an `int` total can overflow even when each individual input fits in an `int`.

## Complete and explain

Complete the marked `calculateTotal` task. Keep the provided input checks and output driver. The untouched starter reports unfinished work with status 2 and prints no answer, including on an empty list.

Before coding, write the input count, required output and numeric bound. Trace a tiny example with positive, negative and zero values. Explain the invariant: after consuming the first `i` values, the total is their sum. The calculation takes O(N) time and O(1) extra space; the whole supplied program uses O(N) memory for the validated input array.

The sample contains three billion-weight values and two `-5` values. Its expected output is:

```text
2999999990
```

## Run natively

Use JDK 17 or newer. Save or export `Main.java`, `README.md` and `sample.in` together, then open a terminal in that folder:

```sh
javac -encoding UTF-8 Main.java
java Main < sample.in
```

These commands use a POSIX shell or Windows Command Prompt. In PowerShell, use `Get-Content sample.in | java Main` for this numeric input. The browser Java teaching preview does not execute this native input-driven project. The site Input panel is not the input source for the native process.

Compare standard output with the prediction. Change the sample and run again. Test zero values, one negative value, cancellation and a sum greater than 2147483647. Then test missing, extra and invalid tokens. Refused input must produce no answer. Shell redirection may create or truncate an output file before Java starts; a file's existence does not establish that the program succeeded.

Work alone by writing the expected result before each run and explaining any mismatch. With an instructor, pause at the same contract, trace and boundary checks. Compare the separate reference only after an attempt; keep the learner project and any later retry separately.
