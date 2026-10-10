"""Exercise exported Gold setup roles, numeric boundaries and failure behavior."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "UG0-Contest-Contract"
TASK = "gold-setup-native-acceptance"


def run(command, cwd, text=None, timeout=30):
    child = subprocess.Popen(command, cwd=cwd, text=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             start_new_session=True)
    print(json.dumps(dict(event="start", parentTaskId=TASK, cwd=str(cwd),
                          command=command, pid=child.pid, startTime=time.time(),
                          timeoutSeconds=timeout)), flush=True)
    try:
        out, err = child.communicate(input=text, timeout=timeout)
    except BaseException:
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        child.communicate()
        print(json.dumps(dict(event="cleanup", parentTaskId=TASK, pid=child.pid,
                              endTime=time.time(), exitCode=child.returncode,
                              childProcessGroupCleanup="terminated")), flush=True)
        raise
    print(json.dumps(dict(event="end", parentTaskId=TASK, pid=child.pid,
                          endTime=time.time(), exitCode=child.returncode,
                          childProcessGroupCleanup="exited")), flush=True)
    return subprocess.CompletedProcess(command, child.returncode, out, err)


def verify(javac, java):
    assert "TASK" in (PACK / "starter/Main.java").read_text()
    assert (PACK / "starter/Main.java").read_text() != (PACK / "solution/Main.java").read_text()
    assert (PACK / "starter/sample.in").read_bytes() == (PACK / "solution/sample.in").read_bytes()
    source_hashes = {}
    for role in ["starter", "solution"]:
        assert {p.name for p in (PACK / role).iterdir()} == {"Main.java", "README.md", "sample.in"}
        for name in ["Main.java", "README.md", "sample.in"]:
            source_hashes[role + "/" + name] = hashlib.sha256((PACK / role / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    with tempfile.TemporaryDirectory(prefix="gold-setup-native-") as temporary:
        work = Path(temporary)
        classes = {}
        for role in ["starter", "solution"]:
            directory = work / role
            directory.mkdir()
            compiled = run([javac, "-encoding", "UTF-8", "-d", str(directory), str(PACK / role / "Main.java")], ROOT)
            assert compiled.returncode == 0, compiled.stderr
            classes[role] = directory
        current = work / "execution"
        current.mkdir()
        sample = (PACK / "solution/sample.in").read_text()
        (current / "sample.in").write_text(sample)
        (current / "old-answer.out").write_text("saved answer\n")
        original = {p.name: p.read_bytes() for p in current.iterdir()}
        values_cases = [[], [0], [-1000000000], [1000000000] * 3,
                        [1000000000, -1000000000, 7, -7],
                        [1000000000] * 200000, [-1000000000] * 200000]
        randomizer = random.Random(20261010)
        values_cases += [[randomizer.randint(-1000000000, 1000000000) for _ in range(n)] for n in [1, 2, 7, 101, 5000]]
        valid_count = 0
        for values in values_cases:
            text = str(len(values)) + "\n" + " ".join(map(str, values)) + "\n"
            result = run([java, "-cp", str(classes["solution"]), "Main"], current, text)
            assert result.returncode == 0 and result.stderr == "" and result.stdout == f"{sum(values)}\n", result
            valid_count += 1
        for text in [sample, sample.replace("\n", "\r\n"), "\n 3 \n 1\t -2\n3 \n\n"]:
            result = run([java, "-cp", str(classes["solution"]), "Main"], current, text)
            expected = "2\n" if text.startswith("\n") else "2999999990\n"
            assert result.returncode == 0 and result.stderr == "" and result.stdout == expected, result
            valid_count += 1
        invalid = ["", "x\n", "-1\n", "200001\n", "0 extra\n", "1\n", "1 1000000001\n",
                   "1 -1000000001\n", "1 3.5\n", "1 9999999999999999999999\n",
                   "2 1 junk\n", "2 1 2 3\n", "2 1\n", "1 7 late-invalid\n"]
        for text in invalid:
            result = run([java, "-cp", str(classes["solution"]), "Main"], current, text)
            assert result.returncode == 2 and result.stdout == "" and result.stderr.startswith("Cannot solve setup input:"), result
        for text in [sample, "0\n", "1 -7\n"]:
            result = run([java, "-cp", str(classes["starter"]), "Main"], current, text)
            assert result.returncode == 2 and result.stdout == "" and result.stderr == "Cannot solve setup input: Complete the setup total task before producing an answer\n", result
        assert {p.name: p.read_bytes() for p in current.iterdir()} == original
    print(json.dumps(dict(event="gold-setup-accepted", parentTaskId=TASK, validCases=valid_count,
                          invalidCases=len(invalid), unfinishedLearnerCases=3,
                          allInputAndUnrelatedFilesPreserved=True, sourceHashes=source_hashes)), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--javac", default="javac")
    parser.add_argument("--java", default="java")
    args = parser.parse_args()
    verify(args.javac, args.java)
