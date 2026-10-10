"""Verify preserved reference answers and the genuinely unfinished learner export."""
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
PACK = ROOT / "UG21-Moo-Tube"
REFERENCE_SHA = "0e47f318ee65993f390f6e3e27270976c8403365bff069dc5088c7b627ebd613"
TASK = "mootube-native-source-acceptance"


def run(command, cwd, timeout=30):
    child = subprocess.Popen(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True)
    print(json.dumps(dict(event="start", parentTaskId=TASK, cwd=str(cwd), command=command,
                          pid=child.pid, startTime=time.time(), timeoutSeconds=timeout)), flush=True)
    try:
        out, err = child.communicate(timeout=timeout)
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


def case(n, edges, queries):
    adjacency = [[] for _ in range(n)]
    for a, b, relevance in edges:
        adjacency[a].append((b, relevance))
        adjacency[b].append((a, relevance))
    answers = []
    for threshold, start in queries:
        seen = {start}
        stack = [start]
        while stack:
            for vertex, relevance in adjacency[stack.pop()]:
                if relevance >= threshold and vertex not in seen:
                    seen.add(vertex)
                    stack.append(vertex)
        answers.append(len(seen) - 1)
    text = f"{n} {len(queries)}\n" + "".join(f"{a+1} {b+1} {w}\n" for a, b, w in edges)
    text += "".join(f"{k} {v+1}\n" for k, v in queries)
    return text, "".join(f"{a}\n" for a in answers)


def verify(javac, java):
    before = {str(p.relative_to(PACK)): p.read_bytes() for p in PACK.rglob("*") if p.is_file()}
    canonical = (PACK / "solution/Main.java").read_bytes().replace(b"\r\n", b"\n")
    tracked = subprocess.run(["git", "show", "HEAD:UG21-Moo-Tube/solution/Main.java"],
                             cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
    assert canonical == tracked and hashlib.sha256(tracked).hexdigest() == REFERENCE_SHA
    for role in ["starter", "solution"]:
        assert {p.name for p in (PACK / role).iterdir()} == {"Main.java", "README.md", "sample.in"}
        text = (PACK / role / "README.md").read_text()
        for section in ["Prerequisites and input", "Trace and explain", "Native workflow", "Verify and explain"]:
            assert "## " + section in text
    starter = (PACK / "starter/Main.java").read_text()
    assert all("TASK " + str(i) + ":" in starter for i in range(1, 7))
    assert starter != (PACK / "solution/Main.java").read_text()
    assert (PACK / "starter/sample.in").read_bytes() == (PACK / "solution/sample.in").read_bytes()
    sample = (PACK / "solution/sample.in").read_text()
    small = [case(4, [(0, 1, 3), (1, 2, 2), (1, 3, 4)], [(1, 1), (4, 0), (3, 0)]),
             case(1, [], [(1, 0), (1000000000, 0)]),
             case(5, [(0, 1, 7), (1, 2, 7), (2, 3, 7), (3, 4, 7)], [(7, 4), (8, 2), (1, 0), (7, 4)]),
             case(7, [(0, i, i) for i in range(1, 7)], [(i, i % 7) for i in [6, 1, 4, 2, 7, 1]])]
    assert small[0] == (sample, "3\n0\n2\n")
    rng = random.Random(20261010)
    for _ in range(24):
        n = rng.randint(2, 23)
        edges = [(i, rng.randrange(i), rng.choice([1, 2, 5, 7, 1000000000])) for i in range(1, n)]
        queries = [(rng.choice([1, 2, 5, 7, 8, 1000000000]), rng.randrange(n)) for _ in range(25)]
        small.append(case(n, edges, queries))
    n = 100000
    queries = [(1 if i % 3 == 0 else 1000000000 if i % 3 == 1 else 999999999, i) for i in range(n)]
    large_text = f"{n} {n}\n" + "".join(f"{i} {i+1} 999999999\n" for i in range(1, n))
    large_text += "".join(f"{k} {v+1}\n" for k, v in queries)
    large_answer = "".join(f"{0 if k == 1000000000 else n-1}\n" for k, _ in queries)
    valid = small + [(sample.replace("\n", "\r\n"), "3\n0\n2\n"),
                     (sample.replace(" ", "\t") + " \n\n", "3\n0\n2\n"),
                     (large_text, large_answer)]
    invalid = ["", "0 1\n", "100001 1\n", "1 0\n", "1 100001\n", "1 1 extra\n",
               "N Q\n", "2 1\n1 2 0\n1 1\n", "2 1\n1 2 1000000001\n1 1\n",
               "2 1\n1 3 7\n1 1\n", "2 1\n1 1 7\n1 1\n", "2 1\n1 2\n1 1\n",
               "1 1\n", "1 1\n0 1\n", "1 1\n1000000001 1\n", "1 1\n1 0\n",
               "1 1\n1 2\n", "1 1\n1 1 extra\n", "1 1\n1.5 1\n",
               "1 1\n9999999999999999999999 1\n", sample + "late-invalid\n",
               "2 2\n1 2 7\n1 1\n0 2\n"]
    # An independent tiny traversal implementation exercises the completed learner
    # DRIVER only. It is not a Gold performance solution and never changes the export.
    marker = 'throw new UnsupportedOperationException("Complete the six MooTube tasks before producing an answer");'
    assert starter.count(marker) == 1
    probe = starter.replace(marker, "return traversalForTesting(input);")
    probe = probe.replace("    public static void main(String[] args)", '''    static int[] traversalForTesting(Input input) {
        List<List<int[]>> graph = new ArrayList<>();
        for (int i = 0; i < input.n; i++) graph.add(new ArrayList<>());
        for (Edge edge : input.edges) {
            graph.get(edge.p).add(new int[] {edge.q, edge.weight});
            graph.get(edge.q).add(new int[] {edge.p, edge.weight});
        }
        int[] answers = new int[input.queries.length];
        for (Query query : input.queries) {
            boolean[] seen = new boolean[input.n];
            java.util.ArrayDeque<Integer> pending = new java.util.ArrayDeque<>();
            pending.add(query.v); seen[query.v] = true;
            int reached = 0;
            while (!pending.isEmpty()) {
                int vertex = pending.removeFirst(); reached++;
                for (int[] edge : graph.get(vertex)) {
                    if (edge[1] >= query.k && !seen[edge[0]]) {
                        seen[edge[0]] = true; pending.addLast(edge[0]);
                    }
                }
            }
            answers[query.index] = reached - 1;
        }
        return answers;
    }

    public static void main(String[] args)''')
    with tempfile.TemporaryDirectory(prefix="mootube-source-native-") as temporary:
        work = Path(temporary)
        classes = {}
        for role, source in [("starter", starter), ("solution", (PACK / "solution/Main.java").read_text()),
                             ("completed-driver-probe", probe)]:
            directory = work / role
            directory.mkdir()
            source_path = directory / "Main.java"
            source_path.write_text(source)
            result = run([javac, "--release", "17", "-encoding", "UTF-8", "-Xlint:all", "-Werror", "Main.java"], directory)
            assert result.returncode == 0, result.stderr
            classes[role] = directory
        execution = work / "execution"
        execution.mkdir()
        input_path = execution / "mootube.in"
        answer_path = execution / "mootube.out"
        unrelated = execution / "retained-attempt.txt"
        unrelated.write_text("separate retained learner work\n")
        def execute(role):
            return run([java, "-ea", "-Xmx256m", "-cp", str(classes[role]), "Main"], execution)
        for text, expected in valid:
            input_path.write_text(text, newline="")
            answer_path.write_text("old answer\n")
            result = execute("solution")
            assert result.returncode == 0 and result.stdout == "" and result.stderr == "", result
            assert answer_path.read_text() == expected and input_path.read_text() == text.replace("\r\n", "\n")
        for text, expected in small:
            input_path.write_text(text)
            answer_path.write_text("old answer\n")
            result = execute("completed-driver-probe")
            assert result.returncode == 0 and result.stdout == "" and result.stderr == "", result
            assert answer_path.read_text() == expected and input_path.read_text() == text
        unfinished = [sample, small[1][0], small[2][0], large_text]
        for text in unfinished:
            input_path.write_text(text)
            for existing in [False, True]:
                if answer_path.exists(): answer_path.unlink()
                if existing: answer_path.write_text("retained old answer\n")
                result = execute("starter")
                assert result.returncode == 2 and result.stdout == ""
                assert result.stderr == "Cannot solve mootube.in: Complete the six MooTube tasks before producing an answer\n"
                assert answer_path.exists() == existing
                if existing: assert answer_path.read_text() == "retained old answer\n"
                assert input_path.read_text() == text
        for text in invalid:
            input_path.write_text(text)
            answer_path.write_text("retained old answer\n")
            for role in ["starter", "completed-driver-probe"]:
                result = execute(role)
                assert result.returncode == 2 and result.stdout == "" and result.stderr.startswith("Cannot solve mootube.in:")
                assert answer_path.read_text() == "retained old answer\n" and input_path.read_text() == text
        input_path.unlink()
        result = execute("starter")
        assert result.returncode == 2 and result.stdout == "" and result.stderr.startswith("Cannot solve mootube.in:")
        assert answer_path.read_text() == "retained old answer\n"
        assert unrelated.read_text() == "separate retained learner work\n"
    assert {str(p.relative_to(PACK)): p.read_bytes() for p in PACK.rglob("*") if p.is_file()} == before
    print(json.dumps(dict(event="mootube-source-accepted", parentTaskId=TASK,
                          validReferenceCases=len(valid), tinyIndependentDriverCases=len(small),
                          maximumN=100000, maximumQ=100000, refusedLearnerAndDriverInputs=len(invalid),
                          unfinishedLearnerCases=len(unfinished) * 2, missingInputCases=1,
                          referenceGitSha256=REFERENCE_SHA, referencePreserved=True,
                          sourceFilesUnchanged=True, originalInputAndUnrelatedWorkPreserved=True,
                          historicalReferenceInvalidInputClaims=False,
                          completedProbeGoldPerformanceClaim=False,
                          sourceHashes={name:hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest() for name,data in before.items()})), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--javac", default="javac")
    parser.add_argument("--java", default="java")
    arguments = parser.parse_args()
    verify(arguments.javac, arguments.java)
