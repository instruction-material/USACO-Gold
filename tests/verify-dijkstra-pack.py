"""Compile both actual roles, verify file I/O and independently check paths."""
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
PACK = ROOT / "UG9-Dijkstras-Algorithm"
LEGACY_SHA = "dc8911401580f4eca1ccc3ed5cc47a5a603811679a2902cbd63b459c201dc1e1"
TASK = "required-dijkstra-native-acceptance"


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


def oracle(n, edges):
    distances = [None] * n
    distances[0] = 0
    for _ in range(n - 1):
        changed = False
        for a, b, w in edges:
            for start, end in [(a, b), (b, a)]:
                if distances[start] is None:
                    continue
                candidate = distances[start] + w
                if distances[end] is None or candidate < distances[end]:
                    distances[end] = candidate
                    changed = True
        if not changed:
            break
    return distances


def check_output(n, edges, text):
    expected = oracle(n, edges)
    lines = text.splitlines()
    assert len(lines) == n - 1
    weights = {}
    for a, b, w in edges:
        for pair in [(a, b), (b, a)]:
            weights[pair] = min(weights.get(pair, w), w)
    for destination, line in enumerate(lines, 1):
        if expected[destination] is None:
            assert line == f"Unreachable: {destination}", line
            continue
        path, cost = line.split("Distance: ")
        vertices = [int(token) for token in path.split()]
        assert vertices[0] == 0 and vertices[-1] == destination
        assert len(vertices) == len(set(vertices))
        assert int(cost) == expected[destination]
        assert sum(weights[(a, b)] for a, b in zip(vertices, vertices[1:])) == int(cost)


def verify(javac, java):
    assert hashlib.sha256((PACK / "legacy/Main.java").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == LEGACY_SHA
    assert (PACK / "starter/dijkstra.in").read_bytes() == (PACK / "solution/dijkstra.in").read_bytes()
    valid = [
        (1, []), (3, []), (3, [(1, 2, 1)]),
        (3, [(0, 1, 1), (0, 1, 9), (1, 2, 0), (1, 1, 0)]),
        (4, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1)]),
        (3, [(0, 1, 0), (1, 2, 0), (2, 0, 0)]),
        (4, [(0, 1, 1000000000), (1, 2, 1000000000), (2, 3, 1000000000)]),
        (5, [(0, 1, 10), (0, 2, 3), (2, 1, 4), (1, 3, 2), (2, 3, 9), (3, 4, 0)]),
        (2000, [(i, i + 1, 1000000000) for i in range(1999)]),
        (2, [(0, 1, 7)] + [(0, 1, 1000000000)] * 199999),
    ]
    invalid = ["", "0 0\n", "2001 0\n", "1 -1\n", "1 200001\n",
               "1 0 extra\n", "2 1\n", "2 1\n0 2 1\n", "2 1\n0 1 -1\n",
               "1 1\n0 0 1000000001\n", "two 0\n", "2 0\nextra\n",
               "2 1\n0 1\n", "2 1\n0 1 1\n0 1 2\n"]
    with tempfile.TemporaryDirectory(prefix="required-dijkstra-") as directory:
        working = Path(directory)
        classes = {}
        for role in ["starter", "solution"]:
            destination = working / role
            destination.mkdir()
            classes[role] = destination
            command = [javac, "--release", "17", "-encoding", "UTF-8", "-Xlint:all", "-Werror",
                       "-d", str(destination), str(PACK / role / "Main.java")]
            if role == "solution":
                command.append(str(ROOT / "tests/DijkstraOracleProbe.java"))
            result = run(command, working, 60)
            assert result.returncode == 0, result.stderr
        probe = run([java, "-ea", "-Xmx256m", "-cp", str(classes['solution']), "DijkstraOracleProbe"], working)
        assert probe.returncode == 0 and probe.stdout.strip() == "BELLMAN_FORD_PATH_ORACLE_PASS 4168", (probe.stdout, probe.stderr)
        input_file, output_file = working / "dijkstra.in", working / "dijkstra.out"
        def execute(role):
            return run([java, "-ea", "-Xmx256m", "-cp", str(classes[role]), "Main"], working)
        for n, edges in valid:
            input_file.write_text(encode(n, edges))
            output_file.unlink(missing_ok=True)
            result = execute("solution")
            assert result.returncode == 0, result.stderr
            check_output(n, edges, output_file.read_text())
        for text in invalid:
            input_file.write_text(text)
            output_file.write_text("previous correct output\n")
            result = execute("solution")
            assert result.returncode == 2 and "Cannot solve dijkstra.in:" in result.stderr
            assert output_file.read_text() == "previous correct output\n"
        input_file.unlink()
        output_file.unlink()
        result = execute("solution")
        assert result.returncode == 2 and not output_file.exists()
        input_file.write_bytes((PACK / "starter/dijkstra.in").read_bytes())
        for previous in [None, "earlier learner output\n"]:
            if previous is None:
                output_file.unlink(missing_ok=True)
            else:
                output_file.write_text(previous)
            result = execute("starter")
            assert result.returncode == 2 and "Complete the four Dijkstra tasks" in result.stderr
            assert not output_file.exists() if previous is None else output_file.read_text() == previous
    print(json.dumps({"event": "verified-required-dijkstra-pack", "parentTaskId": TASK,
                      "algorithmOracle": "Bellman-Ford relaxation plus independent predecessor-edge sums",
                      "oracleGraphs": 4168, "nativeValidFileCases": len(valid),
                      "maximumSizeFileCases": 2, "invalidFileCases": len(invalid),
                      "unfinishedLearnerProducesNoAnswer": True, "priorOutputPreservedOnFailure": True,
                      "legacyGitBytesPreserved": True, "javaRelease": 17,
                      "sourceHashes": {role: hashlib.sha256((PACK / role / "Main.java").read_bytes().replace(b"\r\n", b"\n")).hexdigest() for role in ['starter', 'solution']}}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--javac", default="javac")
    parser.add_argument("--java", default="java")
    arguments = parser.parse_args()
    verify(arguments.javac, arguments.java)
