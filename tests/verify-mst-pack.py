"""Verify actual Prim roles with independent tree oracles and native file I/O."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "UG14-MST"
LEGACY_SHA = "e47f6916a578af8fbc6a0eb3beb0b06b89991c9603bdbe1a2980c69638f2bd8d"
TASK = "required-mst-native-acceptance"


def run(command, cwd, timeout=20):
    started = time.time()
    process = subprocess.Popen(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=True)
    print(json.dumps({"event": "start", "parentTaskId": TASK, "cwd": str(cwd),
                      "command": command, "pid": process.pid, "startTime": started,
                      "timeoutSeconds": timeout}), flush=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except BaseException:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.communicate()
        print(json.dumps({"event": "cleanup", "parentTaskId": TASK, "pid": process.pid,
                          "childProcessGroupCleanup": "terminated", "endTime": time.time(),
                          "exitCode": process.returncode}), flush=True)
        raise
    print(json.dumps({"event": "end", "parentTaskId": TASK, "pid": process.pid,
                      "endTime": time.time(), "exitCode": process.returncode,
                      "childProcessGroupCleanup": "exited"}), flush=True)
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def encode(n, edges):
    return f"{n} {len(edges)}\n" + "".join(f"{a} {b} {w}\n" for a, b, w in edges)


def kruskal(n, edges):
    parent = list(range(n))

    def find(v):
        while parent[v] != v:
            v = parent[v]
        return v

    total, count = 0, 0
    for a, b, weight in sorted(edges, key=lambda edge: edge[2]):
        a, b = find(a), find(b)
        if a != b:
            parent[a] = b
            total += weight
            count += 1
    return total if count == n - 1 else None


def check_output(n, edges, text):
    expected = kruskal(n, edges)
    assert expected is not None
    lines = text.splitlines()
    assert len(lines) == n and lines[-1] == f"Total Distance: {expected}"
    weights = {}
    for a, b, weight in edges:
        for pair in [(a, b), (b, a)]:
            weights[pair] = min(weights.get(pair, weight), weight)
    previous = [-1] * n
    total = 0
    for vertex, line in enumerate(lines[:-1], 1):
        child, parent = map(int, line.split())
        assert child == vertex and 0 <= parent < n and child != parent
        assert (child, parent) in weights
        previous[child] = parent
        total += weights[(child, parent)]
    for vertex in range(1, n):
        seen = set()
        while vertex != 0:
            assert 0 <= vertex < n and vertex not in seen
            seen.add(vertex)
            vertex = previous[vertex]
    assert total == expected


def verify(javac, java):
    assert hashlib.sha256((PACK / "legacy/Main.java").read_bytes()).hexdigest() == LEGACY_SHA
    assert (PACK / "starter/prim.in").read_bytes() == (PACK / "solution/prim.in").read_bytes()
    for role in ["starter", "solution"]:
        guide = (PACK / role / "README.md").read_text()
        assert "## Prerequisites and input" in guide and "## Trace and explain" in guide
        assert "## Native workflow" in guide and "../" not in guide
    valid = [
        (1, []), (1, [(0, 0, 0)]),
        (2, [(0, 1, 1), (0, 1, 9)]), (2, [(0, 1, 9), (0, 1, 1)]),
        (4, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1)]),
        (3, [(0, 1, 0), (1, 2, 0), (2, 0, 0), (1, 1, 0)]),
        (4, [(0, 1, 1000000000), (1, 2, 1000000000), (2, 3, 1000000000)]),
        (3, [(0, 1, 10), (0, 2, 6), (1, 2, 5)]),
        (5, [(0, 1, 10), (0, 2, 3), (2, 1, 4), (1, 3, 2),
             (2, 3, 9), (3, 4, 0), (0, 4, 20)]),
        (2000, [(i, i + 1, 1000000000) for i in range(1999)]),
        (2, [(0, 1, 7)] + [(0, 1, 1000000000)] * 199999),
    ]
    invalid = ["", "0 0\n", "2001 0\n", "1 -1\n", "1 200001\n",
               "1 0 extra\n", "2 1\n", "2 1\n0 2 1\n", "2 1\n0 1 -1\n",
               "1 1\n0 0 1000000001\n", "two 0\n", "2 0\nextra\n",
               "2 1\n0 1\n", "2 1\n0 1 1\n0 1 2\n"]
    disconnected = [encode(2, []), encode(3, [(1, 2, 1)]),
                    encode(4, [(0, 1, 0), (2, 3, 0)])]
    with tempfile.TemporaryDirectory(prefix="required-mst-") as directory:
        working = Path(directory)
        classes = {}
        for role in ["starter", "solution", "legacy"]:
            destination = working / role
            destination.mkdir()
            classes[role] = destination
            command = [javac, "--release", "17", "-encoding", "UTF-8", "-Xlint:all", "-Werror",
                       "-d", str(destination), str(PACK / role / "Main.java")]
            if role == "solution":
                command.append(str(ROOT / "tests/MstOracleProbe.java"))
            result = run(command, working, 60)
            assert result.returncode == 0, result.stderr
        probe = run([java, "-ea", "-Xmx256m", "-cp", str(classes["solution"]), "MstOracleProbe"], working)
        assert probe.returncode == 0 and probe.stdout.strip() == "KRUSKAL_AND_TREE_ORACLE_PASS 2784", (probe.stdout, probe.stderr)
        input_file, output_file = working / "prim.in", working / "prim.out"

        def execute(role):
            return run([java, "-ea", "-Xmx256m", "-cp", str(classes[role]), "Main"], working)

        for n, edges in valid:
            input_file.write_text(encode(n, edges))
            output_file.unlink(missing_ok=True)
            result = execute("solution")
            assert result.returncode == 0, result.stderr
            check_output(n, edges, output_file.read_text())
        assert encode(*valid[8]) == (PACK / "solution/prim.in").read_text()
        input_file.write_text(encode(*valid[8]))
        result = execute("solution")
        assert result.returncode == 0
        assert output_file.read_text() == "1 2\n2 0\n3 1\n4 3\nTotal Distance: 9\n"
        for text in invalid + disconnected:
            input_file.write_text(text)
            for earlier in [None, "earlier correct output\n"]:
                output_file.unlink(missing_ok=True)
                if earlier is not None:
                    output_file.write_text(earlier)
                result = execute("solution")
                assert result.returncode == 2 and "Cannot solve prim.in:" in result.stderr
                if earlier is None:
                    assert not output_file.exists()
                else:
                    assert output_file.read_text() == earlier
        for earlier in [None, "earlier correct output\n"]:
            input_file.unlink(missing_ok=True)
            output_file.unlink(missing_ok=True)
            if earlier is not None:
                output_file.write_text(earlier)
            result = execute("solution")
            assert result.returncode == 2
            assert not output_file.exists() if earlier is None else output_file.read_text() == earlier
        input_file.write_bytes((PACK / "starter/prim.in").read_bytes())
        for earlier in [None, "earlier learner output\n"]:
            output_file.unlink(missing_ok=True)
            if earlier is not None:
                output_file.write_text(earlier)
            result = execute("starter")
            assert result.returncode == 2 and "Complete the four Prim tasks" in result.stderr
            assert not output_file.exists() if earlier is None else output_file.read_text() == earlier
        # Reproduce the preserved historical defects without using them as an oracle.
        for n, edges, observed in [(2, valid[2][1], "Total Distance: 9"),
                                  (4, valid[6][1], "Total Distance: -1294967296")]:
            input_file.write_text(encode(n, edges))
            output_file.unlink(missing_ok=True)
            result = execute("legacy")
            assert result.returncode == 0 and output_file.read_text().splitlines()[-1] == observed
        input_file.write_text(encode(2, []))
        output_file.write_text("earlier correct output\n")
        result = execute("legacy")
        assert result.returncode != 0 and "ArrayIndexOutOfBoundsException" in result.stderr
        assert output_file.exists() and output_file.read_text() != "earlier correct output\n"
    print(json.dumps({"event": "verified-required-mst-pack", "parentTaskId": TASK,
                      "algorithmOracle": "independent Kruskal plus exhaustive tiny spanning trees",
                      "oracleGraphs": 2784, "exhaustiveSimpleGraphs": 729,
                      "nativeValidFileCases": len(valid), "maximumSizeFileCases": 2,
                      "invalidFileCases": len(invalid), "disconnectedFileCases": len(disconnected),
                      "unfinishedLearnerProducesNoAnswer": True, "priorOutputPreservedOnRefusal": True,
                      "threeLegacyDefectsReproduced": True, "legacyGitBytesPreserved": True,
                      "javaRelease": 17, "selfContainedRoleGuides": True,
                      "sourceHashes": {role: hashlib.sha256((PACK / role / "Main.java").read_bytes()).hexdigest()
                                       for role in ["starter", "solution"]}}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--javac", default="javac")
    parser.add_argument("--java", default="java")
    arguments = parser.parse_args()
    verify(arguments.javac, arguments.java)
