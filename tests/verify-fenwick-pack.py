"""Verify exported Fenwick roles against plain-array oracles and actual native I/O."""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "UG22-Binary-Indexed-Tree-Fenwick-Tree"
LEGACY_SHA = "8f9eeb3a1df29088cee66843e1889036a0b7cde5529e560a95d532071dcf0a66"
TASK = "required-fenwick-native-acceptance"


def run(command, cwd, input_text=None, timeout=30):
    started = time.time()
    process = subprocess.Popen(command, cwd=cwd, text=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True)
    print(json.dumps({"event": "start", "parentTaskId": TASK, "cwd": str(cwd),
                      "command": command, "pid": process.pid, "startTime": started,
                      "timeoutSeconds": timeout}), flush=True)
    try:
        stdout, stderr = process.communicate(input=input_text, timeout=timeout)
    except BaseException:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.communicate()
        print(json.dumps({"event": "cleanup", "parentTaskId": TASK, "pid": process.pid,
                          "endTime": time.time(), "exitCode": process.returncode,
                          "childProcessGroupCleanup": "terminated"}), flush=True)
        raise
    print(json.dumps({"event": "end", "parentTaskId": TASK, "pid": process.pid,
                      "endTime": time.time(), "exitCode": process.returncode,
                      "childProcessGroupCleanup": "exited"}), flush=True)
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def encode(values, commands):
    return f"{len(values)} {len(commands)}\n" + " ".join(map(str, values)) + "\n" + "".join(
        " ".join(map(str, command)) + "\n" for command in commands)


def plain_array(values, commands):
    values = list(values)
    answers = []
    for command in commands:
        if command[0] == "ADD":
            values[command[1]] += command[2]
        elif command[0] == "PREFIX":
            answers.append(sum(values[:command[1] + 1]))
        else:
            answers.append(sum(values[command[1]:command[2] + 1]))
    return "".join(f"{value}\n" for value in answers)


def all_queries(n):
    return [("PREFIX", index) for index in range(-1, n)] + [
        ("RANGE", left, right) for left in range(n) for right in range(left, n)]


def verify(javac, java):
    working_legacy = (PACK / "legacy/Main.java").read_bytes()
    tracked = subprocess.run(["git", "show", "HEAD:UG22-Binary-Indexed-Tree-Fenwick-Tree/legacy/Main.java"],
                             cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    canonical_legacy = tracked.stdout if tracked.returncode == 0 else working_legacy
    assert hashlib.sha256(canonical_legacy).hexdigest() == LEGACY_SHA
    # Git may convert text newlines at checkout; the canonical blob remains exact.
    assert working_legacy.replace(b"\r\n", b"\n") == canonical_legacy
    reference = (PACK / "solution/Main.java").read_text()
    starter = (PACK / "starter/Main.java").read_text()
    assert reference.rsplit("\n/**", 1)[0] == starter.rsplit("\n/**", 1)[0]
    assert (PACK / "starter/sample.in").read_bytes() == (PACK / "solution/sample.in").read_bytes()
    for role in ["starter", "solution"]:
        assert sorted(p.name for p in (PACK / role).iterdir()) == ["Main.java", "README.md", "sample.in"]
        guide = (PACK / role / "README.md").read_text()
        for heading in ["Prerequisites and input", "Trace and explain", "Native workflow", "Verify and explain"]:
            assert f"## {heading}" in guide
        assert "not historical contest limits" in guide and "O(N+Q) memory" in guide
        assert "../" not in guide
    invalid = [
        "", "0 0\n0\n", "200001 0\n0\n", "1 -1\n0\n", "1 200001\n0\n",
        "1 0 extra\n0\n", "one 0\n0\n", "1 0\n", "2 0\n1\n", "1 0\n0 1\n",
        "1 0\n1000000001\n", "1 0\n-1000000001\n", "1 0\n1.5\n",
        "1 1\n0\n", "1 1\n0\n\n", "1 1\n0\nADD -1 1\n",
        "1 1\n0\nADD 1 1\n", "1 1\n0\nADD 0 1000000001\n",
        "1 1\n0\nADD 0 -1000000001\n", "1 1\n0\nADD 0\n",
        "1 1\n0\nPREFIX -2\n", "1 1\n0\nPREFIX 1\n",
        "1 1\n0\nPREFIX 0 extra\n", "1 1\n0\nRANGE -1 0\n",
        "1 1\n0\nRANGE 0 1\n", "2 1\n0 0\nRANGE 1 0\n",
        "1 1\n0\nUNKNOWN 0\n", "1 0\n0\nextra\n",
        "1 2\n7\nPREFIX 0\nADD 1 1\n"
    ]
    with tempfile.TemporaryDirectory(prefix="required-fenwick-") as directory:
        work = Path(directory)
        classes = {}
        for role in ["starter", "solution", "legacy"]:
            target = work / role
            target.mkdir()
            result = run([javac, "--release", "17", "-encoding", "UTF-8", "-d", str(target),
                          str(PACK / role / "Main.java")], work)
            assert result.returncode == 0, result.stderr
            classes[role] = target
        current = work / "native-run"
        current.mkdir()
        sentinel = current / "earlier-answer.txt"
        sentinel.write_text("Earlier separately saved answer\n")
        old_files = {p.name: p.read_bytes() for p in current.iterdir()}
        result = run([java, "-cp", str(classes["legacy"]), "Main"], current)
        assert result.returncode == 0 and result.stdout == "19\n" and result.stderr == ""
        cases = 0
        answers = 0

        def native(values, commands, expected=None):
            nonlocal cases, answers
            expected = plain_array(values, commands) if expected is None else expected
            result = run([java, "-Xmx128m", "-cp", str(classes["solution"]), "Main"],
                         current, encode(values, commands))
            assert result.returncode == 0 and result.stderr == "", result.stderr
            assert result.stdout == expected, (values[:20], commands[:20], result.stdout[:400], expected[:400])
            cases += 1
            answers += expected.count("\n")

        sample = (PACK / "solution/sample.in").read_text()
        result = run([java, "-cp", str(classes["solution"]), "Main"], current, sample)
        assert result.returncode == 0 and result.stderr == ""
        assert result.stdout == "19\n14\n24\n3\n0\n9\n33\n"
        native([0], [])
        native([1000000000, 1000000000], [("RANGE", 0, 1), ("ADD", 0, -1000000000),
                                       ("ADD", 0, -1000000000), ("PREFIX", 0), ("RANGE", 0, 1)])
        tiny = 0
        for n in range(1, 5):
            for values in itertools.product([-1, 0, 1], repeat=n):
                commands = all_queries(n)
                for index, delta in [(0, 1), (n - 1, -2), (0, -1)]:
                    commands.append(("ADD", index, delta))
                    commands.extend(all_queries(n))
                native(values, commands)
                tiny += 1
        randomizer = random.Random(20261010)
        values = [randomizer.randint(-1000000000, 1000000000) for _ in range(37)]
        commands = []
        for i in range(2500):
            if i % 3 == 0:
                commands.append(("ADD", randomizer.randrange(37), randomizer.randint(-1000000000, 1000000000)))
            elif i % 3 == 1:
                commands.append(("PREFIX", randomizer.randrange(-1, 37)))
            else:
                left = randomizer.randrange(37)
                commands.append(("RANGE", left, randomizer.randrange(left, 37)))
        native(values, commands)
        for sign in [-1, 1]:
            values = [sign * 1000000000] * 200000
            commands = []
            expected = []
            total = sign * 200000000000000
            for _ in range(100000):
                commands.extend([("ADD", 199999, -sign * 1000000000), ("PREFIX", 199999)])
                total -= sign * 1000000000
                expected.append(f"{total}\n")
            native(values, commands, "".join(expected))
        for text in invalid:
            result = run([java, "-cp", str(classes["solution"]), "Main"], current, text)
            assert result.returncode == 2 and result.stdout == "", (text, result)
            assert result.stderr.startswith("Cannot solve Fenwick input:")
        for text in [sample, "1 0\n0\n", "1 1\n7\nPREFIX 0\n"]:
            result = run([java, "-cp", str(classes["starter"]), "Main"], current, text)
            assert result.returncode == 2 and result.stdout == ""
            assert result.stderr == "Cannot solve Fenwick input: Complete the four Fenwick tasks before producing an answer\n"
        result = run([java, "-cp", str(classes["solution"]), "Main"], current, " 1 1 \n 7 \n PREFIX 0 \n\n")
        assert result.returncode == 0 and result.stdout == "7\n" and result.stderr == ""
        result = run([java, "-cp", str(classes["solution"]), "Main"], current, sample.replace("\n", "\r\n"))
        assert result.returncode == 0 and result.stdout == "19\n14\n24\n3\n0\n9\n33\n" and result.stderr == ""
        # Probe the actual exported class API independently of the input driver.
        probe = work / "FenwickBoundaryProbe.java"
        probe.write_text("""
class FenwickBoundaryProbe {
    static void refused(Runnable action) {
        try { action.run(); throw new AssertionError("Expected invalid index refusal"); }
        catch (IllegalArgumentException expected) { }
    }
    public static void main(String[] args) throws Exception {
        BinaryIndexedTree bit = new BinaryIndexedTree(11);
        long[] values = {3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3};
        for (int round = 0; round < 3; round++) {
            bit.load(values);
            for (int step = 0; step < 5; step++) {
                for (int left = 0; left < values.length; left++) {
                    long total = 0;
                    for (int right = left; right < values.length; right++) {
                        total += values[right];
                        if (bit.rangeSum(left, right) != total) throw new AssertionError("range");
                    }
                }
                var field = BinaryIndexedTree.class.getDeclaredField("A");
                field.setAccessible(true);
                long[] cells = (long[]) field.get(bit);
                if (cells[0] != 0) throw new AssertionError("unused slot");
                for (int i = 1; i < cells.length; i++) {
                    int width = 1;
                    while (i % (width * 2) == 0) width *= 2;
                    long sum = 0;
                    for (int j = i - width; j < i; j++) sum += values[j];
                    if (cells[i] != sum) throw new AssertionError("block invariant");
                }
                int index = step % 2 == 0 ? 0 : 10;
                long delta = step % 2 == 0 ? 1000000000L : -1000000000L;
                values[index] += delta;
                bit.add(delta, index);
            }
        }
        for (int i : new int[]{-2, -1, 11, 12}) { final int index = i; refused(() -> bit.add(1, index)); }
        for (int i : new int[]{-2, 11, 12}) { final int index = i; refused(() -> bit.sum(index)); }
        refused(() -> bit.rangeSum(2, 1));
        refused(() -> bit.rangeSum(-1, 0));
        refused(() -> bit.rangeSum(0, 11));
        refused(() -> bit.load(new long[1]));
        if (bit.sum(-1) != 0) throw new AssertionError("empty prefix");
        System.out.println("Verified reset/load, cells, closed ranges and API bounds");
    }
}
""")
        result = run([javac, "--release", "17", "-encoding", "UTF-8", "-cp", str(classes["solution"]),
                      "-d", str(classes["solution"]), str(probe)], work)
        assert result.returncode == 0, result.stderr
        result = run([java, "-cp", str(classes["solution"]), "FenwickBoundaryProbe"], current)
        assert result.returncode == 0 and result.stderr == "", result.stderr
        assert result.stdout == "Verified reset/load, cells, closed ranges and API bounds\n"
        assert {p.name: p.read_bytes() for p in current.iterdir()} == old_files
        report = {"event": "verified-fenwick-native", "parentTaskId": TASK,
                  "sourceHead": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                  "workingTreeDirty": bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT)),
                  "validCases": cases + 3, "exhaustiveTinyArrays": tiny, "seededOperations": 2500,
                  "verifiedQueryAnswers": answers + 15, "maximumInputs": 2, "invalidInputs": len(invalid),
                  "unfinishedStarterCases": 3, "originalDemoPreserved": True,
                  "internalBlockInvariantAndApiBounds": True, "noAnswerFilesCreatedOrChanged": True,
                  "sourceHashes": {str(p.relative_to(PACK)): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for role in ["starter", "solution"] for p in sorted((PACK / role).iterdir())}}
        print(json.dumps(report), flush=True)
        return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--javac", default="javac")
    parser.add_argument("--java", default="java")
    parser.add_argument("--report")
    arguments = parser.parse_args()
    report = verify(arguments.javac, arguments.java)
    if arguments.report:
        Path(arguments.report).write_text(json.dumps(report, indent=2) + "\n")
