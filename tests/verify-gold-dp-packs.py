"""Check Gold references against exhaustive partitions and full-limit fixtures."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKS = {"UG3-Teamwork": "teamwork", "UG8-Bookshelf": "bookshelf"}


def partitions(values):
    """Enumerate every placement of boundaries, without a DP recurrence."""
    for mask in range(1 << (len(values) - 1)):
        groups = []
        begin = 0
        for end in range(1, len(values)):
            if mask & (1 << (end - 1)):
                groups.append(values[begin:end])
                begin = end
        groups.append(values[begin:])
        yield groups


def teamwork_case(skills, maximum_team):
    expected = max(
        sum(len(group) * max(group) for group in groups)
        for groups in partitions(skills)
        if all(len(group) <= maximum_team for group in groups)
    )
    return f"{len(skills)} {maximum_team}\n" + "\n".join(map(str, skills)) + "\n", expected


def bookshelf_case(books, limit):
    expected = min(
        sum(max(height for height, _ in group) for group in groups)
        for groups in partitions(books)
        if all(sum(width for _, width in group) <= limit for group in groups)
    )
    return f"{len(books)} {limit}\n" + "".join(f"{h} {w}\n" for h, w in books), expected


def fixtures(basename):
    rng = random.Random(863 if basename == "teamwork" else 138)
    if basename == "teamwork":
        sample = teamwork_case([1, 15, 7, 9, 2, 5, 10], 3)
        assert sample[1] == 84
        yield sample
        for skills, maximum_team in [
            ([1], 1), ([100000], 1000), ([1, 100000, 1], 1),
            ([4, 4, 4, 4], 3), ([1, 2, 3, 4, 5], 2),
            ([5, 4, 3, 2, 1], 3), ([1, 100, 1, 1, 100, 1], 3),
            ([1, 100000, 1, 1], 1000),
        ]:
            yield teamwork_case(skills, maximum_team)
        for _ in range(120):
            n = rng.randint(1, 12)
            yield teamwork_case([rng.randint(1, 100000) for _ in range(n)], rng.randint(1, 15))
        # Uniform skills are unchanged by grouping, even at the maximum N/K.
        yield "10000 1000\n" + "100000\n" * 10000, 1000000000
        # Only the one team containing the high skill can increase others.
        skills = [1] * 10000
        skills[4999] = 100000
        yield "10000 1000\n" + "\n".join(map(str, skills)) + "\n", 1000 * 100000 + 9000
        yield "10000 1\n" + "\n".join(map(str, range(1, 10001))) + "\n", 10000 * 10001 // 2
        return
    sample = bookshelf_case([(5, 7), (9, 2), (8, 5), (13, 2), (3, 8)], 10)
    assert sample[1] == 21
    yield sample
    for books, limit in [
        ([(1, 1)], 1), ([(1000000, 1000000000)], 1000000000),
        ([(7, 2)] * 6, 6), ([(h, 2) for h in range(1, 9)], 5),
        ([(h, 2) for h in range(8, 0, -1)], 5),
        ([(8, 5), (1, 5), (8, 5)], 10),
        ([(2, 10), (9, 10), (3, 10)], 10),
        ([(1000000, 500000000)] * 8, 1000000000),
    ]:
        yield bookshelf_case(books, limit)
    for _ in range(120):
        n, limit = rng.randint(1, 12), rng.randint(1, 30)
        yield bookshelf_case([(rng.randint(1, 1000000), rng.randint(1, limit)) for _ in range(n)], limit)
    # Every book fills a shelf: total width is 10^14 and height is 10^11.
    yield "100000 1000000000\n" + "1000000 1000000000\n" * 100000, 100000000000
    # All books fit one shelf; increasing/decreasing stack patterns at full N.
    yield "100000 1000000000\n" + "1000000 1\n" * 100000, 1000000
    yield "100000 1000000000\n" + "".join(f"{h} 1\n" for h in range(1, 100001)), 100000
    yield "100000 1000000000\n" + "".join(f"{h} 1\n" for h in range(100000, 0, -1)), 100000
    # Equal heights reduce the optimum to the minimum number of legal shelves.
    yield "100000 37\n" + "1000000 1\n" * 100000, ((100000 + 36) // 37) * 1000000


def normalized_hash(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify(compiler, mode):
    flags = ["-std=c++20", "-Wall", "-Wextra", "-Wpedantic", "-Werror", "-O1"]
    if mode == "sanitized":
        flags += ["-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
        if os.uname().sysname == "Linux":
            flags += ["-fno-pie", "-no-pie"]
    leaks = "1" if os.uname().sysname == "Linux" else "0"
    environment = {**os.environ, "ASAN_OPTIONS": f"detect_leaks={leaks}:halt_on_error=1", "UBSAN_OPTIONS": "halt_on_error=1:print_stacktrace=1"}
    legacy = [ROOT / "UG3-Teamwork/solution/teamwork.in", ROOT / "UG8-Bookshelf/solution/bookshelf.out"]
    legacy_before = [path.read_bytes() for path in legacy]
    results = []
    with tempfile.TemporaryDirectory(prefix="gold-dp-native-") as directory:
        working = Path(directory)
        for folder, basename in PACKS.items():
            reference_source = ROOT / folder / "solution/main.cpp"
            starter_source = ROOT / folder / "starter/main.cpp"
            reference, learner = working / (basename + "-reference"), working / (basename + "-learner")
            for source, binary in [(reference_source, reference), (starter_source, learner)]:
                subprocess.run([compiler, *flags, str(source), "-o", str(binary)], check=True, timeout=90)
            input_file, output_file = working / (basename + ".in"), working / (basename + ".out")
            count = 0
            for text, expected in fixtures(basename):
                input_file.write_text(text)
                output_file.unlink(missing_ok=True)
                process = subprocess.run([str(reference)], cwd=working, env=environment, capture_output=True, text=True, timeout=20)
                assert process.returncode == 0, (folder, count, process.stderr)
                assert output_file.read_text().split() == [str(expected)], (folder, count, expected, output_file.read_text())
                count += 1
            invalid = ["0 1\n", "1 0\n1\n", "1 1\n0\n"] if basename == "teamwork" else ["0 1\n", "1 1\n1 0\n", "1 1\n1 2\n"]
            for text in invalid:
                input_file.write_text(text)
                output_file.unlink(missing_ok=True)
                process = subprocess.run([str(reference)], cwd=working, env=environment, capture_output=True, text=True, timeout=20)
                assert process.returncode == 2 and "Invalid " in process.stderr, (folder, process.returncode, process.stderr)
                assert not output_file.exists()
            input_file.write_bytes((ROOT / folder / "starter" / (basename + ".in")).read_bytes())
            output_file.unlink(missing_ok=True)
            process = subprocess.run([str(learner)], cwd=working, env=environment, capture_output=True, text=True, timeout=20)
            assert process.returncode == 2 and "Complete " in process.stderr, (folder, process.returncode, process.stderr)
            assert not output_file.exists(), "Untouched starter must not create an answer"
            results.append({"folder": folder, "fileIOCases": count, "outputRecords": count, "independentOracle": True, "maximumSizeCase": True, "starterUnfinished": True, "invalidInputCases": len(invalid), "referenceSha256": normalized_hash(reference_source), "starterSha256": normalized_hash(starter_source)})
    assert [path.read_bytes() for path in legacy] == legacy_before
    print(json.dumps({"compiler": compiler, "mode": mode, "packs": results, "legacyFixtures": {str(path.relative_to(ROOT)): normalized_hash(path) for path in legacy}}, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--compiler", default="c++")
    parser.add_argument("--mode", choices=["ordinary", "sanitized"], default="ordinary")
    args = parser.parse_args()
    verify(args.compiler, args.mode)
