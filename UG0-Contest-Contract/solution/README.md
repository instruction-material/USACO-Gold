# Gold setup: reference

This separately stored reference completes the authored setup checkpoint's 64-bit sum. The learner role retains an unfinished calculation. Compare this role only after an independent attempt.

Read `N` and exactly `N` integer values from standard input, with `0 <= N <= 200000` and absolute values at most 1000000000. Print their sum and one newline, or `0` for no values. The supplied driver refuses missing, invalid, out-of-range and extra tokens with status 2 and no answer. It validates the whole input before calculating.

`calculateTotal` starts a `long` at zero and adds each value. After `i` iterations it equals the sum of the first `i` values. The absolute sum is at most 200000000000000. The calculation takes O(N) time and O(1) extra space; storing the validated array makes whole-program memory O(N).

The sample's expected output is `2999999990` followed by a newline. Change the input and predict the result before executing. Check empty input counts, negative values, cancellation, 32-bit overflow and malformed records. The native acceptance checks also require refusal without partial answers and preservation of existing input and unrelated files.

Use JDK 17 or newer and run from the directory containing the exported files:

```sh
javac -encoding UTF-8 Main.java
java Main < sample.in
```

The commands use a POSIX shell or Windows Command Prompt. In PowerShell, `Get-Content sample.in | java Main` supports this numeric input. The browser Java preview and site Input panel do not execute this native program. Output-file existence after shell redirection is not proof of success.

This exercise confirms the language and I/O workflow before Gold algorithms. It is authored practice, not an official contest statement and not a substitute for reading each contest's own contract.
