"""Verify the two DP role contracts without completing the learner algorithms."""
import argparse
from collections import deque
import datetime
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TASK = os.environ.get("CLASSES_FAMILY_TASK_ID", "gold-dp-learner-packs")


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def run(command, cwd, expected=0, timeout=45):
    child = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True)
    record = dict(parentTaskId=TASK, cwd=str(cwd), command=command,
                  pid=child.pid, parentPid=os.getpid(), startTime=now(),
                  timeoutSeconds=timeout)
    print(json.dumps(dict(event="start", **record)), flush=True)
    try:
        out, err = child.communicate(timeout=timeout)
        assert child.returncode == expected, (command, child.returncode, err.decode())
        if expected == 0:
            assert not err, err.decode()
        else:
            assert not out and err, (out, err)
        return out.decode().replace("\r\n", "\n"), err.decode()
    except BaseException:
        if child.poll() is None:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.communicate()
        record["childProcessGroupCleanup"] = True
        raise
    finally:
        print(json.dumps(dict(event="end", **record, endTime=now(),
                              exitCode=child.returncode)), flush=True)


def compile_java(javac, directory, *files):
    run([javac, "--release", "17", "-encoding", "UTF-8",
         "-Xlint:all", "-Werror", *files], directory)


def replace_method(source, signature, body):
    start = source.index(signature)
    first = source.index("{", start)
    depth = 1
    end = first + 1
    while depth:
        if source[end] == "{":
            depth += 1
        elif source[end] == "}":
            depth -= 1
        end += 1
    return source[:first + 1] + "\n" + body + "\n    " + source[end - 1:]


def subset_value(weights, values, capacity):
    return max(sum(v for v, take in zip(values, bits) if take)
               for bits in itertools.product([False, True], repeat=len(weights))
               if sum(w for w, take in zip(weights, bits) if take) <= capacity)


def fullness_value(limit, first, second):
    seen = {(0, False)}
    pending = deque(seen)
    while pending:
        fullness, water = pending.popleft()
        states = [(fullness + first, water), (fullness + second, water)]
        if not water:
            states.append((fullness // 2, True))
        for state in states:
            if state[0] <= limit and state not in seen:
                seen.add(state)
                pending.append(state)
    return max(fullness for fullness, _ in seen)


KNAPSACK_PROBE = """
        if (weights.length > 12) throw new UnsupportedOperationException("Tiny driver probe only");
        int best = -1;
        List<Integer> indices = new ArrayList<>();
        for (int mask = 0; mask < (1 << weights.length); mask++) {
            long weight = 0;
            int value = 0;
            List<Integer> chosen = new ArrayList<>();
            for (int i = 0; i < weights.length; i++) {
                if ((mask & (1 << i)) != 0) {
                    weight += weights[i]; value += values[i]; chosen.add(i);
                }
            }
            if (weight <= capacity && value > best) { best = value; indices = chosen; }
        }
        return new Result(best, indices);
"""

FRUIT_PROBE = """
        if (input.limit() > 60) throw new UnsupportedOperationException("Tiny driver probe only");
        boolean[][] seen = new boolean[input.limit() + 1][2];
        java.util.ArrayDeque<int[]> pending = new java.util.ArrayDeque<>();
        pending.add(new int[] {0, 0}); seen[0][0] = true;
        int answer = 0;
        while (!pending.isEmpty()) {
            int[] current = pending.remove();
            int fullness = current[0], water = current[1];
            answer = Math.max(answer, fullness);
            int[][] next = {{fullness + input.firstFruit(), water},
                            {fullness + input.secondFruit(), water},
                            {fullness / 2, 1}};
            for (int i = 0; i < (water == 0 ? 3 : 2); i++) {
                int value = next[i][0], used = next[i][1];
                if (value <= input.limit() && !seen[value][used]) {
                    seen[value][used] = true; pending.add(next[i]);
                }
            }
        }
        return answer;
"""

VALIDATION_PROBE = """
import java.util.Arrays;
import java.util.List;
public class ValidationProbe {
    interface Checked { void run(); }
    static int checks = 0;
    static void accepted(Checked check) { check.run(); checks++; }
    static void refused(Checked check) {
        try { check.run(); } catch (IllegalArgumentException expected) { checks++; return; }
        throw new AssertionError("Invalid parameters or selection were accepted");
    }
    public static void main(String[] args) {
        accepted(() -> Main.validateInput(new int[] {2}, new int[] {3}, 4));
        accepted(() -> Main.validateInput(new int[] {}, new int[] {}, 0));
        accepted(() -> Main.validateInput(new int[] {1}, new int[] {Integer.MAX_VALUE}, 1));
        accepted(() -> Main.validateInput(new int[] {1}, new int[] {0}, 499999));
        refused(() -> Main.validateInput(null, new int[] {}, 0));
        refused(() -> Main.validateInput(new int[] {}, null, 0));
        refused(() -> Main.validateInput(new int[] {1}, new int[] {}, 0));
        refused(() -> Main.validateInput(new int[] {0}, new int[] {1}, 1));
        refused(() -> Main.validateInput(new int[] {-1}, new int[] {1}, 1));
        refused(() -> Main.validateInput(new int[] {1}, new int[] {-1}, 1));
        refused(() -> Main.validateInput(new int[] {1}, new int[] {1}, -1));
        refused(() -> Main.validateInput(new int[] {1}, new int[] {0}, 500000));
        refused(() -> Main.validateInput(new int[] {1}, new int[] {1}, Integer.MAX_VALUE));
        refused(() -> Main.validateInput(new int[] {1, 1}, new int[] {Integer.MAX_VALUE, 1}, 2));
        int[] weights = {2}, values = {3};
        accepted(() -> Main.validateResult(new Main.Result(3, List.of(0)), weights, values, 4));
        accepted(() -> Main.validateResult(new Main.Result(0, List.of()), weights, values, 0));
        refused(() -> Main.validateResult(null, weights, values, 4));
        refused(() -> Main.validateResult(new Main.Result(3, null), weights, values, 4));
        refused(() -> Main.validateResult(new Main.Result(-1, List.of()), weights, values, 4));
        refused(() -> Main.validateResult(new Main.Result(6, List.of(0, 0)), weights, values, 4));
        refused(() -> Main.validateResult(new Main.Result(3, List.of(-1)), weights, values, 4));
        refused(() -> Main.validateResult(new Main.Result(3, List.of(1)), weights, values, 4));
        refused(() -> Main.validateResult(new Main.Result(3, Arrays.asList((Integer) null)), weights, values, 4));
        refused(() -> Main.validateResult(new Main.Result(3, List.of(0)), weights, values, 1));
        refused(() -> Main.validateResult(new Main.Result(2, List.of(0)), weights, values, 4));
        System.out.println("parameter-and-selection-checks: " + checks);
    }
}
"""


def verify_knapsack(javac, java, directory):
    learner = (ROOT / "UG2-0-1-Knapsack/starter/Main.java").read_text()
    (directory / "Main.java").write_text(learner)
    compile_java(javac, directory, "Main.java")
    _, error = run([java, "Main"], directory, expected=2)
    assert "Complete all five knapsack tasks" in error
    (directory / "ValidationProbe.java").write_text(VALIDATION_PROBE)
    compile_java(javac, directory, "Main.java", "ValidationProbe.java")
    assert run([java, "ValidationProbe"], directory)[0] == "parameter-and-selection-checks: 25\n"
    probe = replace_method(learner, "static Result solve(", KNAPSACK_PROBE)
    cases = [([1, 3, 4, 5], [1, 4, 5, 7], 7), ([2], [3], 4),
             ([3], [7], 6), ([2, 3], [3, 4], 6), ([2, 2], [3, 3], 4),
             ([1, 2], [0, 0], 3), ([9, 8], [2, 3], 3), ([1], [9], 0),
             ([], [], 0), ([1, 3, 4, 5], [1, 4, 5, 7], 6)]
    for weights, values, capacity in cases:
        candidate = probe
        for before, after in [
            ("int[] weights = {1, 3, 4, 5};", "int[] weights = {" + ", ".join(map(str, weights)) + "};"),
            ("int[] values = {1, 4, 5, 7};", "int[] values = {" + ", ".join(map(str, values)) + "};"),
            ("int capacity = 7;", "int capacity = " + str(capacity) + ";"),
        ]:
            assert candidate.count(before) == 1
            candidate = candidate.replace(before, after)
        (directory / "Main.java").write_text(candidate)
        compile_java(javac, directory, "Main.java")
        output, _ = run([java, "Main"], directory)
        match = re.fullmatch(r"Max value: (\d+)\nItem indices in knapsack: \[([\d, ]*)\]\n", output)
        assert match, output
        indices = [int(x.strip()) for x in match[2].split(",") if x.strip()]
        assert len(indices) == len(set(indices))
        assert all(0 <= i < len(weights) for i in indices)
        assert sum(weights[i] for i in indices) <= capacity
        assert sum(values[i] for i in indices) == int(match[1]) == subset_value(weights, values, capacity)
    return dict(untouchedLearnerRefused=True, parameterAndSelectionChecks=25,
                tinyDriverCases=len(cases), anyOptimalSubsetAccepted=True,
                hardcodedDemonstration=True, algorithmCompleted=False)


def verify_fruit(javac, java, directory):
    learner = (ROOT / "UG40-Fruit-Feast/starter/Main.java").read_text()
    (directory / "Main.java").write_text(learner)
    compile_java(javac, directory, "Main.java")
    answer = directory / "feast.out"
    sentinel = b"preserved earlier attempt\r\n"
    answer.write_bytes(sentinel)
    for sample in ["8 5 6\n", "1 1 1\n", "5000000 5000000 1\n"]:
        (directory / "feast.in").write_text(sample)
        _, error = run([java, "Main"], directory, expected=2)
        assert "Complete all five Fruit Feast tasks" in error
        assert answer.read_bytes() == sentinel
    (directory / "feast.in").unlink()
    run([java, "Main"], directory, expected=2)
    assert answer.read_bytes() == sentinel
    invalid = ["", "\n", "8 5", "8 5 6 7", "x 5 6", "8 0 6", "8 5 9",
               "-1 1 1", "5000001 1 1", "8 5 6\n1\n", "2147483648 1 1", "8 5 6.0"]
    for sample in invalid:
        (directory / "feast.in").write_text(sample)
        run([java, "Main"], directory, expected=2)
        assert answer.read_bytes() == sentinel
    (directory / "feast.in").write_text("8 5 6\n")
    run([java, "Main", "--trace"], directory, expected=2)
    assert answer.read_bytes() == sentinel
    (directory / "Main.java").write_text(replace_method(learner, "static int solve(", FRUIT_PROBE))
    compile_java(javac, directory, "Main.java")
    cases = [(8, 5, 6), (1, 1, 1), (7, 4, 6), (20, 6, 9), (25, 8, 11),
             (11, 11, 11), (19, 3, 7), (30, 13, 17), (2, 2, 2),
             (9, 6, 6), (23, 5, 8), (17, 4, 9)]
    for case in cases:
        (directory / "feast.in").write_text(" ".join(map(str, case)) + "\n\n")
        assert run([java, "Main"], directory)[0] == ""
        assert answer.read_text() == str(fullness_value(*case)) + "\n"
    answer.write_bytes(sentinel)
    (directory / "feast.in").write_text("61 1 1\n")
    _, error = run([java, "Main"], directory, expected=2)
    assert "Tiny driver probe only" in error and answer.read_bytes() == sentinel
    return dict(untouchedLearnerCases=3, invalidInputCases=len(invalid),
                missingInputCases=1, unexpectedArgumentCases=1,
                existingAnswerPreserved=True, tinyDriverCases=len(cases),
                probeLimitExplicit=60, algorithmCompleted=False)


def verify(javac, java):
    folders = ["UG2-0-1-Knapsack", "UG40-Fruit-Feast"]
    original = {f: f.read_bytes() for folder in folders for f in (ROOT / folder).rglob("*") if f.is_file()}
    for folder in folders:
        before = (ROOT / folder / "starter/Main.java").read_text()
        reference = (ROOT / folder / "solution/Main.java").read_text()
        assert before != reference and re.findall(r"TASK ([1-5]):", before) == ["1", "2", "3", "4", "5"]
    with tempfile.TemporaryDirectory(prefix="gold-dp-learner-contracts-") as temp:
        root = Path(temp)
        knapsack_dir = root / "knapsack"
        fruit_dir = root / "fruit"
        knapsack_dir.mkdir()
        fruit_dir.mkdir()
        knapsack = verify_knapsack(javac, java, knapsack_dir)
        fruit = verify_fruit(javac, java, fruit_dir)
    for script in ["verify-knapsack-demo.py", "verify-fruit-feast-reference.py"]:
        output, _ = run([sys.executable, str(ROOT / "tests" / script),
                         "--javac", javac, "--java", java], ROOT, timeout=180)
        print(output, end="", flush=True)
    assert all(path.read_bytes() == data for path, data in original.items())
    print(json.dumps(dict(event="gold-dp-learner-packs-accepted", parentTaskId=TASK,
                          distinctRolePairs=2, tasksPerLearner=5, knapsack=knapsack,
                          fruitFeast=fruit, allCourseFilesUnchangedDuringVerification=True,
                          roleSourceSha256={str(f.relative_to(ROOT)): hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
                                            for f, data in original.items() if f.name == "Main.java"},
                          learnerAlgorithmsRemainUnfinished=True,
                          formalContestPerformanceClaim=False)), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--javac", default="javac")
    parser.add_argument("--java", default="java")
    args = parser.parse_args()
    try:
        verify(args.javac, args.java)
    finally:
        print(json.dumps(dict(event="cleanup", parentTaskId=TASK,
                              pid=os.getpid(), time=now())), flush=True)
