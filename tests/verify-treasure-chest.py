"""Verify actual role file I/O against independent exhaustive models."""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]

PACK, BASENAME = "UG7-Treasure-Chest", "treasure"
LEGACY = PACK + "/solution/treasure.out"
ORACLE = "enumerate complete alternating game trees with absolute player totals"
LARGE_CASES = 3


def full_game(coins):
    def play(left, right, totals, turn):
        if left > right:
            return totals
        possibilities = []
        for side, value in [(0, coins[left]), (1, coins[right])]:
            earned = list(totals)
            earned[turn] += value
            possibilities.append(play(left + (side == 0), right - (side == 1), tuple(earned), 1 - turn))
        return max(possibilities, key=lambda totals: totals[turn])
    return play(0, len(coins) - 1, (0, 0), 0)[0]


def encode(coins):
    return str(len(coins)) + "\n" + "\n".join(map(str, coins)) + "\n"


def fixtures():
    sample = [30, 25, 10, 35]
    assert full_game(sample) == 60
    yield encode(sample), 60
    # Enumerate every small 1/2-valued line, with both players choosing their own totals.
    for length in range(1, 7):
        for coins in itertools.product([1, 2], repeat=length):
            yield encode(coins), full_game(coins)
    for coins in [[5000], [8, 15, 3, 7], [7, 3, 15, 8], [1, 5000, 1], [9] * 9, [1, 2, 3, 4, 5]]:
        yield encode(coins), full_game(coins)
    rng = random.Random(201012)
    for _ in range(180):
        coins = [rng.randint(1, 5000) for _ in range(rng.randint(1, 11))]
        yield encode(coins), full_game(coins)
    # Closed bounds: every first-player turn can take a maximum-valued coin.
    yield encode([5000] * 5000), 12500000
    yield encode([5000] * 4999), 12500000
    yield encode([5000, 1] * 2500), 12500000


def invalid_inputs():
    return ["0\n", "5001\n", "1\n0\n", "1\n5001\n", "2\n1\n", "1\nword\n", "1\n1\nextra\n", "-1\n"]

def verify(compiler, mode):
    flags = ["-std=c++20", "-Wall", "-Wextra", "-Wpedantic", "-Werror", "-O1"]
    if mode == "sanitized":
        flags += ["-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
        if os.uname().sysname == "Linux":
            flags += ["-fno-pie", "-no-pie"]
    environment = {
        **os.environ,
        "ASAN_OPTIONS": "detect_leaks=" + ("1" if os.uname().sysname == "Linux" else "0") + ":halt_on_error=1",
        "UBSAN_OPTIONS": "halt_on_error=1:print_stacktrace=1",
    }
    legacy = ROOT / LEGACY
    original = legacy.read_bytes()
    cases = list(fixtures())
    processes = 0
    with tempfile.TemporaryDirectory(prefix=BASENAME + "-native-") as directory:
        working = Path(directory)
        reference, learner = working / "reference", working / "learner"
        for role, binary in [("solution", reference), ("starter", learner)]:
            subprocess.run([compiler, *flags, str(ROOT / PACK / role / "main.cpp"), "-o", str(binary)], check=True, timeout=90)
        input_file, output_file = working / (BASENAME + ".in"), working / (BASENAME + ".out")
        def run(binary):
            nonlocal processes
            processes += 1
            return subprocess.run([str(binary)], cwd=working, env=environment, capture_output=True, text=True, timeout=20)
        for number, (data, expected) in enumerate(cases):
            input_file.write_text(data)
            output_file.unlink(missing_ok=True)
            process = run(reference)
            assert process.returncode == 0, (number, process.stderr)
            assert output_file.read_text().split() == [str(expected)], (number, expected, output_file.read_text())
        for data in invalid_inputs():
            input_file.write_text(data)
            output_file.write_text("previous successful attempt\n")
            process = run(reference)
            assert process.returncode == 2 and "Invalid " in process.stderr, process.stderr
            assert output_file.read_text() == "previous successful attempt\n"
        input_file.unlink()
        output_file.unlink()
        process = run(reference)
        assert process.returncode == 2 and "Invalid " in process.stderr and not output_file.exists()
        input_file.write_bytes((ROOT / PACK / "starter" / (BASENAME + ".in")).read_bytes())
        for prior_output in [None, "saved earlier output\n"]:
            if prior_output is None:
                output_file.unlink(missing_ok=True)
            else:
                output_file.write_text(prior_output)
            process = run(learner)
            assert process.returncode == 2 and "Complete " in process.stderr, process.stderr
            assert not output_file.exists() if prior_output is None else output_file.read_text() == prior_output
    assert legacy.read_bytes() == original
    print(json.dumps({
        "pack": PACK, "compiler": compiler, "mode": mode,
        "fileIOCases": len(cases), "nativeProcesses": processes,
        "independentOracle": ORACLE, "maximumSizeCases": LARGE_CASES,
        "unfinishedLearnerWritesNoAnswer": True, "failedRunPreservesPreviousOutput": True,
        "legacyByteSha256": hashlib.sha256(original).hexdigest(),
        "legacyBytesPreserved": True,
        "sourceHashes": {role: hashlib.sha256((ROOT / PACK / role / "main.cpp").read_bytes().replace(b"\r\n", b"\n")).hexdigest() for role in ["starter", "solution"]},
    }, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--compiler", default="c++")
    parser.add_argument("--mode", choices=["ordinary", "sanitized"], default="ordinary")
    args = parser.parse_args()
    verify(args.compiler, args.mode)
