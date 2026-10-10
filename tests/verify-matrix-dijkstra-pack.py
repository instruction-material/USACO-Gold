"""Native matrix/reference checks and bounded independent learner-driver probes."""
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
PACK = ROOT / 'UG9-Dijkstras-Algorithm-II'
TASK = 'gold-matrix-dijkstra-native-acceptance'
LEGACY_SHA = 'ca5e56778c33f9990d8c92e749d0a3698895943f4353c37908f766f0bf76aaaf'


def run(command, cwd, expected=0, timeout=25):
    started = time.time()
    process = subprocess.Popen(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=True)
    print(json.dumps(dict(event='start', parentTaskId=TASK, cwd=str(cwd), command=command,
                          pid=process.pid, startTime=started, timeoutSeconds=timeout)), flush=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except BaseException:
        try:
            os.killpg(process.pid, signal.SIGTERM)
            process.communicate(timeout=3)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
        print(json.dumps(dict(event='cleanup', parentTaskId=TASK, pid=process.pid,
                              endTime=time.time(), exitCode=process.returncode,
                              childProcessGroupCleanup='terminated')), flush=True)
        raise
    print(json.dumps(dict(event='end', parentTaskId=TASK, pid=process.pid,
                          endTime=time.time(), exitCode=process.returncode,
                          childProcessGroupCleanup='exited')), flush=True)
    assert process.returncode == expected, (command, process.returncode, stdout, stderr)
    return stdout, stderr


def encode(n, edges):
    return f'{n} {len(edges)}\n' + ''.join(f'{a} {b} {w}\n' for a, b, w in edges)


def oracle(n, edges):
    distance = [None] * n
    distance[0] = 0
    for _ in range(n - 1):
        changed = False
        for a, b, w in edges:
            for start, end in [(a, b), (b, a)]:
                if distance[start] is None:
                    continue
                candidate = distance[start] + w
                if distance[end] is None or candidate < distance[end]:
                    distance[end] = candidate
                    changed = True
        if not changed:
            break
    return distance


def check_output(n, edges, text):
    expected = oracle(n, edges)
    weights = {}
    for a, b, w in edges:
        for pair in [(a, b), (b, a)]:
            weights[pair] = min(weights.get(pair, w), w)
    lines = text.splitlines()
    assert len(lines) == n - 1
    for target, line in enumerate(lines, 1):
        if expected[target] is None:
            assert line == f'Unreachable: {target}', line
            continue
        path, total = line.split('Distance: ')
        vertices = [int(x) for x in path.split()]
        assert vertices[0] == 0 and vertices[-1] == target
        assert len(vertices) == len(set(vertices)) and all(0 <= x < n for x in vertices)
        assert int(total) == expected[target]
        assert sum(weights[(a, b)] for a, b in zip(vertices, vertices[1:])) == int(total)


DRIVER_PROBE = r'''
// Acceptance-only Bellman-Ford probe; deliberately restricted to at most eight vertices.
import java.util.Arrays;
class MatrixDriverProbe {
    static Main.Result solve(Main.Graph graph) {
        if (graph.n > 8) throw new IllegalArgumentException("Tiny probe supports at most eight vertices");
        long[] distance = new long[graph.n];
        int[] previous = new int[graph.n];
        Arrays.fill(distance, Main.INF);
        Arrays.fill(previous, -1);
        distance[0] = 0;
        for (int pass = 1; pass < graph.n; pass++) {
            boolean changed = false;
            for (int a = 0; a < graph.n; a++) {
                for (int b = 0; b < graph.n; b++) {
                    int w = graph.weight[a][b];
                    if (w == -1 || distance[a] == Main.INF) continue;
                    long candidate = distance[a] + w;
                    if (candidate < distance[b]) {
                        distance[b] = candidate;
                        previous[b] = a;
                        changed = true;
                    }
                }
            }
            if (!changed) break;
        }
        return new Main.Result(distance, previous);
    }
    static int checks;
    static void refused(Runnable action) {
        try { action.run(); } catch (IllegalArgumentException expected) { checks++; return; }
        throw new AssertionError("Invalid result accepted");
    }
    public static void main(String[] args) {
        Main.Graph g = new Main.Graph(3, new int[][] {{-1, 7, -1}, {7, -1, 0}, {-1, 0, -1}});
        refused(() -> Main.outputLines(g, null));
        refused(() -> Main.outputLines(g, new Main.Result(null, new int[3])));
        refused(() -> Main.outputLines(g, new Main.Result(new long[3], null)));
        refused(() -> Main.outputLines(g, new Main.Result(new long[2], new int[3])));
        refused(() -> Main.outputLines(g, new Main.Result(new long[3], new int[2])));
        refused(() -> Main.outputLines(g, new Main.Result(new long[] {1, 7, 7}, new int[] {-1, 0, 1})));
        refused(() -> Main.outputLines(g, new Main.Result(new long[] {0, 7, 7}, new int[] {0, 0, 1})));
        refused(() -> Main.outputLines(g, new Main.Result(new long[] {0, -7, 7}, new int[] {-1, 0, 1})));
        refused(() -> Main.outputLines(g, new Main.Result(new long[] {0, Long.MAX_VALUE - 1, 7}, new int[] {-1, 0, 1})));
        refused(() -> Main.outputLines(g, new Main.Result(new long[] {0, 7, 7}, new int[] {-1, 0, 3})));
        refused(() -> Main.outputLines(g, new Main.Result(new long[] {0, 7, 7}, new int[] {-1, 2, 1})));
        refused(() -> Main.outputLines(g, new Main.Result(new long[] {0, 7, 7}, new int[] {-1, 0, -1})));
        refused(() -> Main.outputLines(g, new Main.Result(new long[] {0, 7, 7}, new int[] {-1, 0, 0})));
        refused(() -> Main.outputLines(g, new Main.Result(new long[] {0, 8, 7}, new int[] {-1, 0, 1})));
        refused(() -> Main.outputLines(g, new Main.Result(new long[] {0, Main.INF, Main.INF}, new int[] {-1, 0, -1})));
        if (!Main.outputLines(g, solve(g)).equals(java.util.List.of("0 1 Distance: 7", "0 1 2 Distance: 7"))) {
            throw new AssertionError("Valid paths refused");
        }
        if (new Main.State(Long.MAX_VALUE, 0).compareTo(new Main.State(0, 1)) <= 0) {
            throw new AssertionError("Queue key overflow");
        }
        System.out.println("MATRIX_DRIVER_GUARDS_PASS " + checks);
    }
}
'''


def verify(javac, java):
    paths = [p for p in PACK.rglob('*') if p.is_file()]
    before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert before[str((PACK / 'legacy/Main.java').relative_to(ROOT))] == LEGACY_SHA
    assert (PACK / 'starter/dijkstra.in').read_bytes() == (PACK / 'solution/dijkstra.in').read_bytes()
    learner = (PACK / 'starter/Main.java').read_text()
    assert learner.count('// TODO ') == 4
    stop = 'throw new UnsupportedOperationException("Complete the four matrix Dijkstra tasks");'
    assert learner.count(stop) == 1
    sample = (PACK / 'solution/dijkstra.in').read_text().splitlines()
    sample_n = int(sample[0].split()[0])
    sample_edges = [tuple(map(int, row.split())) for row in sample[1:]]
    tiny = [(sample_n, sample_edges), (1, []), (3, []), (3, [(1, 2, 1)]),
            (2, [(0, 1, 1), (0, 1, 9)]), (2, [(0, 1, 9), (0, 1, 1)]),
            (3, [(0, 1, 1500000000), (1, 2, 1500000000)]),
            (3, [(0, 1, 2147483647), (1, 2, 2147483647)]),
            (3, [(0, 1, 0), (1, 2, 0), (2, 0, 0), (1, 1, 0)]),
            (4, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1)]),
            (4, [(0, 1, 10), (0, 2, 1), (2, 1, 1), (1, 3, 2)])]
    rng = random.Random(20261010)
    for n in range(1, 9):
        tiny.append((n, [(rng.randrange(n), rng.randrange(n), rng.choice([0, 1, 7, 2147483647]))
                         for _ in range(n * 2)]))
    large = [(2000, [(0, i, 2147483647) for i in range(1, 2000)]),
             (2, [(0, 1, 7)] + [(0, 1, 2147483647)] * 199999)]
    invalid = ['', '\n', '0 0\n', '2001 0\n', '1 -1\n', '1 200001\n',
               '1 0 extra\n', '2 1\n', '2 1\n0 2 1\n', '2 1\n-1 1 1\n',
               '2 1\n0 1 -1\n', '2 1\n0 1 2147483648\n', 'two 0\n',
               '2 0\nextra\n', '2 1\n0 1\n', '2 1\n0 1 1 2\n',
               '2 1\n0 1 1\n0 1 2\n', '2 1\n\n', '2 1\n0 1 1.5\n']
    with tempfile.TemporaryDirectory(prefix='gold-matrix-dijkstra-') as temp:
        directory = Path(temp)
        classes = {}
        for role in ['starter', 'solution', 'probe']:
            working = directory / role
            working.mkdir()
            classes[role] = working
            if role == 'probe':
                (working / 'Main.java').write_text(learner.replace(stop, 'return MatrixDriverProbe.solve(graph);'))
                (working / 'MatrixDriverProbe.java').write_text(DRIVER_PROBE)
                files = [str(working / 'Main.java'), str(working / 'MatrixDriverProbe.java')]
            else:
                files = [str(PACK / role / 'Main.java')]
                if role == 'solution':
                    files.append(str(ROOT / 'tests/MatrixDijkstraOracleProbe.java'))
            run([javac, '--release', '17', '-encoding', 'UTF-8', '-Xlint:all', '-Werror',
                 '-d', str(working), *files], directory, timeout=60)
        assert run([java, '-ea', '-Xmx256m', '-cp', str(classes['solution']), 'MatrixDijkstraOracleProbe'], directory)[0] == 'MATRIX_BELLMAN_FORD_PATH_ORACLE_PASS 321\n'
        assert run([java, '-ea', '-Xmx256m', '-cp', str(classes['probe']), 'MatrixDriverProbe'], directory)[0] == 'MATRIX_DRIVER_GUARDS_PASS 15\n'
        input_file, answer = directory / 'dijkstra.in', directory / 'dijkstra.out'
        sentinel = b'earlier correct answer\r\n'
        unrelated = directory / 'learner-notes.txt'
        unrelated.write_bytes(b'preserved notes\n')
        def execute(role, expected=0, args=None):
            return run([java, '-ea', '-Xmx256m', '-cp', str(classes[role]), 'Main', *(args or [])], directory, expected)
        for n, edges in tiny + large:
            input_file.write_text(encode(n, edges))
            input_before = input_file.read_bytes()
            answer.unlink(missing_ok=True)
            assert execute('solution') == ('', '')
            check_output(n, edges, answer.read_text())
            assert input_file.read_bytes() == input_before
        for n, edges in tiny:
            input_file.write_text(encode(n, edges))
            assert execute('probe') == ('', '')
            check_output(n, edges, answer.read_text())
        unfinished_cases = [encode(1, []), encode(6, sample_edges), encode(2000, [])]
        for text in unfinished_cases:
            input_file.write_text(text)
            for previous in [False, True]:
                if previous:
                    answer.write_bytes(sentinel)
                else:
                    answer.unlink(missing_ok=True)
                _, error = execute('starter', 2)
                assert 'Complete the four matrix Dijkstra tasks' in error
                assert answer.read_bytes() == sentinel if previous else not answer.exists()
        for role in ['starter', 'probe']:
            for text in invalid:
                input_file.write_text(text)
                answer.write_bytes(sentinel)
                execute(role, 2)
                assert answer.read_bytes() == sentinel and input_file.read_text() == text
            input_file.unlink()
            execute(role, 2)
            assert answer.read_bytes() == sentinel
            input_file.write_text(encode(2, [(0, 1, 1)]))
            execute(role, 2, ['--trace'])
            assert answer.read_bytes() == sentinel
        input_file.write_text(encode(9, []))
        _, error = execute('probe', 2)
        assert 'Tiny probe supports at most eight vertices' in error and answer.read_bytes() == sentinel
        assert unrelated.read_bytes() == b'preserved notes\n'
    assert before == {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    proof = dict(event='gold-matrix-dijkstra-pack-accepted', parentTaskId=TASK,
                 independentOracleGraphs=321, validReferenceFileCases=len(tiny) + len(large),
                 tinyIndependentDriverCases=len(tiny), maximumN=2000, maximumM=200000,
                 maximumWeight=2147483647, maximumSimplePathTotal=4292819810353,
                 refusedInputsPerLearnerAndProbe=len(invalid), resultGuardChecks=15,
                 unfinishedLearnerCases=len(unfinished_cases) * 2, missingInputCases=2,
                 unexpectedArgumentCases=2, originalWorkingBytesPreserved=True,
                 originalLegacySha256=LEGACY_SHA, sourceFilesUnchanged=True,
                 priorAnswerAndUnrelatedWorkPreserved=True, anyMinimumPathAccepted=True,
                 originalSampleSha256={name:hashlib.sha256((PACK/'solution'/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for name in ['dijkstra.in','dijkstra.out']},
                 roleSourceSha256={role:hashlib.sha256((PACK/role/'Main.java').read_bytes().replace(b'\r\n',b'\n')).hexdigest() for role in ['starter','solution']},
                 learnerAlgorithmRemainsUnfinished=True, tinyProbeMaximumN=8,
                 historicalReferenceInvalidInputClaims=False, formalContestPerformanceClaim=False)
    print(json.dumps(proof), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--javac', default='javac')
    parser.add_argument('--java', default='java')
    args = parser.parse_args()
    verify(args.javac, args.java)
