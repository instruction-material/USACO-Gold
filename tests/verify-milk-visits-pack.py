"""Portable native reference checks and unfinished learner-driver checks."""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import tempfile
import time

TASK = 'gold-milk-visits-native-acceptance'
LEGACY_SHA = '084487fc622204d9cef2d53367857fe65f9cbdd124f76d68ab03879ecf7df5e9'

DRIVER_PROBE = r'''
// Acceptance-only BFS path probe, restricted to eight farms and 32 queries.
import java.util.Arrays;
class MilkDriverProbe {
    static String mode = "valid";
    static boolean[] solve(Main.Problem problem) {
        int n = problem.types.length;
        if (n > 8 || problem.queries.length > 32) {
            throw new IllegalArgumentException("Tiny probe supports at most eight farms and 32 queries");
        }
        if (mode.equals("null")) return null;
        if (mode.equals("wrong")) return new boolean[problem.queries.length + 1];
        boolean[] answer = new boolean[problem.queries.length];
        for (int i = 0; i < answer.length; i++) {
            int[] query = problem.queries[i];
            int[] parent = new int[n];
            Arrays.fill(parent, -2);
            parent[query[0]] = -1;
            int[] queue = new int[n];
            int head = 0, tail = 1;
            queue[0] = query[0];
            while (head < tail && parent[query[1]] == -2) {
                int node = queue[head++];
                for (int next : problem.graph.get(node)) {
                    if (parent[next] == -2) {
                        parent[next] = node;
                        queue[tail++] = next;
                    }
                }
            }
            for (int node = query[1]; node != -1; node = parent[node]) {
                answer[i] |= problem.types[node] == query[2];
            }
        }
        return answer;
    }
    public static void main(String[] args) {
        mode = args[0];
        Main.main(new String[0]);
    }
}
'''


def run(command, cwd, expected=0, timeout=30):
    started = time.time()
    child = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    print(json.dumps(dict(event='start', parentTaskId=TASK, cwd=str(cwd), command=command, pid=child.pid, startTime=started, timeoutSeconds=timeout)), flush=True)
    try:
        out, err = child.communicate(timeout=timeout)
    except BaseException:
        try:
            os.killpg(child.pid, signal.SIGTERM)
            child.communicate(timeout=3)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGKILL)
                child.communicate()
        print(json.dumps(dict(event='cleanup', parentTaskId=TASK, pid=child.pid, exitCode=child.returncode, endTime=time.time(), childProcessGroupCleanup='terminated')), flush=True)
        raise
    print(json.dumps(dict(event='end', parentTaskId=TASK, pid=child.pid, exitCode=child.returncode, endTime=time.time(), childProcessGroupCleanup='exited')), flush=True)
    assert child.returncode == expected, (command, child.returncode, out, err)
    return out, err


def encode(types, edges, queries):
    data = f'{len(types)} {len(queries)}\n' + ' '.join(map(str, types)) + '\n'
    data += ''.join(f'{a+1} {b+1}\n' for a, b in edges)
    return data + ''.join(f'{a+1} {b+1} {c}\n' for a, b, c in queries)


def oracle(types, edges, queries):
    graph = [[] for _ in types]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    answer = []
    for a, b, c in queries:
        parent = [-2] * len(types)
        parent[a] = -1
        queue = collections.deque([a])
        while queue and parent[b] == -2:
            node = queue.popleft()
            for neighbor in graph[node]:
                if parent[neighbor] == -2:
                    parent[neighbor] = node
                    queue.append(neighbor)
        found = False
        while b != -1:
            found |= types[b] == c
            b = parent[b]
        answer.append('1' if found else '0')
    return ''.join(answer) + '\n'


def verify(pack, javac, java):
    paths = sorted(p for p in pack.rglob('*') if p.is_file())
    before = {str(p.relative_to(pack)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert before['legacy/Main.java'] == LEGACY_SHA
    assert before['starter/Main.java'] != before['solution/Main.java']
    sample = (pack/'starter/milkvisits.in').read_text()
    assert sample == (pack/'solution/milkvisits.in').read_text()
    assert (pack/'solution/milkvisits.out').read_text() == '10110\n'
    second = '6 4\n1 2 3 3 3 3\n1 2\n2 3\n3 4\n2 5\n5 6\n4 6 1\n4 6 2\n4 6 3\n4 6 4\n'
    small = '1 1\n1\n1 1 1\n'
    valid = [('sample-1', sample, '10110\n'), ('sample-2', second, '0110\n'), ('one-farm', small, '1\n')]
    rng = random.Random(970)
    for index in range(45):
        n = rng.randint(2, 55)
        types = [rng.randint(1, n) for _ in range(n)]
        edges = [(rng.randrange(v), v) for v in range(1, n)]
        rng.shuffle(edges)
        queries = [(rng.randrange(n), rng.randrange(n), rng.randint(1, n)) for _ in range(90)]
        valid.append((f'independent-path-{index}', encode(types, edges, queries), oracle(types, edges, queries)))
    n = 100000
    edges = [(i, i+1) for i in range(n-1)]
    queries = [((i*179)%n, (i*65537)%n, (i*997)%n+1) for i in range(n)]
    full = encode(list(range(1, n+1)), edges, queries)
    expected = ''.join('1' if min(a, b)+1 <= c <= max(a, b)+1 else '0' for a, b, c in queries) + '\n'
    valid.append(('full-depth-and-queries', full, expected))
    invalid = [
        '0 1\n', '1 0\n', '100001 1\n', '1 100001\n', '1 1 1\n', 'one 1\n',
        '1 1\n2\n1 1 1\n', '1 1\n1\n1 2 1\n', '1 1\n1\n1 1 0\n',
        '2 1\n1 2\n1 1\n1 2 1\n', '3 1\n1 2 3\n1 2\n1 2\n1 3 1\n',
        '2 1\n1 2\n1 3\n1 2 1\n', '1 1\n1\n', '1 1\n1\n1 1\n', small+'1\n'
    ]
    sentinel = b'earlier answer\n'
    with tempfile.TemporaryDirectory(prefix='milk-visits-acceptance-') as temp:
        root = Path(temp)
        roles = {}
        for role in ['starter', 'solution', 'probe']:
            cwd = root/role
            cwd.mkdir()
            source = (pack/('starter' if role == 'probe' else role)/'Main.java').read_bytes()
            files = ['Main.java']
            if role == 'probe':
                marker = b'throw new UnsupportedOperationException("Complete the four Milk Visits tree-path tasks");'
                assert source.count(marker) == 1
                source = source.replace(marker, b'return MilkDriverProbe.solve(problem);')
                (cwd/'MilkDriverProbe.java').write_text(DRIVER_PROBE)
                files.append('MilkDriverProbe.java')
            (cwd/'Main.java').write_bytes(source)
            run([javac, '--release', '17', '-encoding', 'UTF-8', '-Xlint:all', '-Werror', *files], cwd, timeout=45)
            roles[role] = cwd
        cwd = roles['solution']
        for name, data, answer in valid:
            (cwd/'milkvisits.in').write_text(data)
            (cwd/'milkvisits.out').write_bytes(sentinel)
            assert run([java, '-ea', '-Xmx256m', 'Main'], cwd) == (b'', b'')
            assert (cwd/'milkvisits.out').read_text() == answer, name
            assert (cwd/'milkvisits.in').read_text() == data
        cwd = roles['starter']
        for data in [sample, second, small, full]:
            (cwd/'milkvisits.in').write_text(data)
            for previous in [False, True]:
                output = cwd/'milkvisits.out'
                if previous:
                    output.write_bytes(sentinel)
                else:
                    output.unlink(missing_ok=True)
                out, err = run([java, '-ea', '-Xmx256m', 'Main'], cwd, expected=2)
                assert not out and b'Complete the four Milk Visits' in err
                assert output.read_bytes() == sentinel if previous else not output.exists()
        for data in invalid:
            (cwd/'milkvisits.in').write_text(data)
            (cwd/'milkvisits.out').write_bytes(sentinel)
            out, err = run([java, '-ea', '-Xmx256m', 'Main'], cwd, expected=2)
            assert not out and b'Cannot solve' in err and (cwd/'milkvisits.out').read_bytes() == sentinel
        (cwd/'milkvisits.in').unlink()
        run([java, '-ea', '-Xmx256m', 'Main'], cwd, expected=2)
        assert (cwd/'milkvisits.out').read_bytes() == sentinel
        (cwd/'milkvisits.in').write_text(small)
        run([java, '-ea', '-Xmx256m', 'Main', '--trace'], cwd, expected=2)
        assert (cwd/'milkvisits.out').read_bytes() == sentinel
        cwd = roles['probe']
        types = [1, 2, 1, 3, 4, 2, 1, 8]
        edges = [(0, 1), (1, 2), (1, 3), (0, 4), (4, 5), (5, 6), (4, 7)]
        queries = [(2, 6, 2), (3, 7, 8), (5, 6, 3), (7, 7, 8)]
        tiny = valid[:3] + [('eight-farm-branches', encode(types, edges, queries), oracle(types, edges, queries))]
        for name, data, answer in tiny:
            (cwd/'milkvisits.in').write_text(data)
            (cwd/'milkvisits.out').write_bytes(sentinel)
            assert run([java, '-ea', '-Xmx256m', 'Main'], cwd) == (b'', b'')
            assert (cwd/'milkvisits.out').read_text() == answer, name
        for mode in ['null', 'wrong']:
            (cwd/'milkvisits.in').write_text(small)
            (cwd/'milkvisits.out').write_bytes(sentinel)
            out, err = run([java, '-ea', '-Xmx256m', 'MilkDriverProbe', mode], cwd, expected=2)
            assert not out and b'Return one answer per query' in err
            assert (cwd/'milkvisits.out').read_bytes() == sentinel
        for oversized in [encode(list(range(1, 10)), [(i, i+1) for i in range(8)], [(0, 8, 1)]),
                          encode([1], [], [(0, 0, 1)] * 33)]:
            (cwd/'milkvisits.in').write_text(oversized)
            (cwd/'milkvisits.out').write_bytes(sentinel)
            out, err = run([java, '-ea', '-Xmx256m', 'Main'], cwd, expected=2)
            assert not out and b'Tiny probe supports' in err
            assert (cwd/'milkvisits.out').read_bytes() == sentinel
    assert before == {str(p.relative_to(pack)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    print(json.dumps(dict(event='gold-milk-visits-pack-accepted', parentTaskId=TASK, referenceFileCases=len(valid), independentBfsQueries=4050, maximumVertices=100000, maximumQueries=100000, unfinishedLearnerCases=8, invalidInputCases=len(invalid), missingInputCases=1, unexpectedArgumentCases=1, tinyIndependentDriverCases=len(tiny), driverResultGuardCases=2, tinyProbeMaximumN=8, tinyProbeMaximumQueries=32, originalBytesPreserved=True, roleSourceDistinct=True, sourceFilesUnchanged=True, previousAnswerPreserved=True, learnerAlgorithmUnfinished=True, jvmStackOverride=False, historicalReferenceInvalidInputClaims=False, roleSourceSha256={role: before[f'{role}/Main.java'] for role in ['starter', 'solution']})), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pack', type=Path, default=Path(__file__).resolve().parents[1]/'UG-Milk-Visits')
    parser.add_argument('--javac', default='javac')
    parser.add_argument('--java', default='java')
    args = parser.parse_args()
    verify(args.pack.resolve(), args.javac, args.java)
