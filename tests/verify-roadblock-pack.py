"""Native preserved-reference, supplied-helper and restricted file-driver checks."""
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

TASK = 'gold-roadblock-native-acceptance'
REFERENCE_SHA = 'd81fc19d4b07e0b3d8279d490f2252fb9912bc9cdd0ad6ec926a01b41b59051a'
SAMPLE_SHA = 'ffc25b6c65d1c547ec2b06a12cc1311e612ece5d123dcb6da5277349e2a2b14d'
PROBE = r'''
import java.nio.file.Path;
import java.util.Arrays;

class RoadblockDriverProbe {
    static String mode = "normal";
    static long floyd(int[][] lengths) {
        int n = lengths.length;
        long[][] distance = new long[n][n];
        for (int a = 0; a < n; a++) {
            Arrays.fill(distance[a], Main.INF);
            distance[a][a] = 0;
            for (int b = 0; b < n; b++) {
                if (lengths[a][b] > 0) distance[a][b] = Math.min(distance[a][b], lengths[a][b]);
            }
        }
        for (int k = 0; k < n; k++) {
            for (int a = 0; a < n; a++) {
                for (int b = 0; b < n; b++) {
                    distance[a][b] = Math.min(distance[a][b], distance[a][k] + distance[k][b]);
                }
            }
        }
        return distance[0][n - 1];
    }
    static void checkPath(Main.ShortestPath path, int[][] lengths, long expected) {
        assert path.distance == expected;
        int node = lengths.length - 1;
        boolean[] seen = new boolean[lengths.length];
        long sum = 0;
        while (node != 0) {
            assert !seen[node];
            seen[node] = true;
            int parent = path.parent[node];
            assert parent >= 0 && parent < lengths.length && lengths[parent][node] > 0;
            sum += lengths[parent][node];
            node = parent;
        }
        assert path.parent[0] == -1 && sum == expected;
    }
    // Acceptance-only all-road Floyd enumeration, restricted to eight fields.
    static long solve(Main.Problem problem) {
        if (problem.lengths.length > 8) throw new IllegalArgumentException("Tiny driver probe only");
        if (mode.equals("negative")) return -1;
        if (mode.equals("too-large")) return (long) (problem.lengths.length - 1) * Main.MAX_WEIGHT + 1;
        int[][] original = Arrays.stream(problem.lengths).map(int[]::clone).toArray(int[][]::new);
        long baseline = floyd(problem.lengths);
        Main.ShortestPath saved = Main.shortestPath(problem.lengths);
        int[] savedParents = saved.parent.clone();
        checkPath(saved, problem.lengths, baseline);
        long answer = 0;
        for (int[] road : problem.roads) {
            int a = road[0], b = road[1], old = problem.lengths[a][b];
            // Deliberately failed experiment verifies symmetric state restoration.
            try {
                problem.lengths[a][b] = old * 2;
                problem.lengths[b][a] = old * 2;
                throw new IllegalStateException("controlled trial failure");
            } catch (IllegalStateException expected) {
                assert expected.getMessage().equals("controlled trial failure");
            } finally {
                problem.lengths[a][b] = old;
                problem.lengths[b][a] = old;
            }
            assert Arrays.deepEquals(original, problem.lengths);
            try {
                problem.lengths[a][b] = old * 2;
                problem.lengths[b][a] = old * 2;
                long trial = floyd(problem.lengths);
                checkPath(Main.shortestPath(problem.lengths), problem.lengths, trial);
                answer = Math.max(answer, trial - baseline);
            } finally {
                problem.lengths[a][b] = old;
                problem.lengths[b][a] = old;
            }
            assert Arrays.deepEquals(original, problem.lengths);
            assert Arrays.equals(savedParents, saved.parent) && saved.distance == baseline;
        }
        return answer;
    }
    public static void main(String[] args) {
        mode = args[0];
        Main.main(new String[0]);
    }
}

class RoadblockHelperProbe {
    public static void main(String[] args) throws Exception {
        Main.Problem problem = Main.readProblem(Path.of("rblock.in"));
        int[][] original = Arrays.stream(problem.lengths).map(int[]::clone).toArray(int[][]::new);
        RoadblockDriverProbe.checkPath(Main.shortestPath(problem.lengths), problem.lengths, Long.parseLong(args[0]));
        assert Arrays.deepEquals(original, problem.lengths);
    }
}
'''


def run(command, cwd, expected=0, timeout=30):
    child = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    print(json.dumps(dict(event='start', parentTaskId=TASK, cwd=str(cwd), command=command, pid=child.pid,
                          startTime=time.time(), timeoutSeconds=timeout)), flush=True)
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
        print(json.dumps(dict(event='cleanup', parentTaskId=TASK, pid=child.pid, exitCode=child.returncode,
                              endTime=time.time(), childProcessGroupCleanup='terminated')), flush=True)
        raise
    print(json.dumps(dict(event='end', parentTaskId=TASK, pid=child.pid, exitCode=child.returncode,
                          endTime=time.time(), childProcessGroupCleanup='exited')), flush=True)
    assert child.returncode == expected, (command, child.returncode, out, err)
    return out, err


def encode(n, roads):
    return f'{n} {len(roads)}\n' + ''.join(f'{a+1} {b+1} {weight}\n' for a, b, weight in roads)


def shortest(n, roads):
    # Independent repeated edge relaxation; no matrix selection or queue.
    distance = [10**20] * n
    distance[0] = 0
    for _ in range(n - 1):
        changed = False
        for a, b, weight in roads:
            if distance[a] + weight < distance[b]:
                distance[b] = distance[a] + weight
                changed = True
            if distance[b] + weight < distance[a]:
                distance[a] = distance[b] + weight
                changed = True
        if not changed:
            break
    assert distance[-1] < 10**20
    return distance[-1]


def oracle(n, roads):
    baseline = shortest(n, roads)
    answer = 0
    for index in range(len(roads)):
        changed = [(a, b, weight * (2 if at == index else 1)) for at, (a, b, weight) in enumerate(roads)]
        answer = max(answer, shortest(n, changed) - baseline)
    return baseline, answer


def verify(pack, javac, java):
    before = {str(f.relative_to(pack)): hashlib.sha256(f.read_bytes()).hexdigest() for f in pack.rglob('*') if f.is_file()}
    reference = (pack/'solution/Main.java').read_bytes()
    sample_raw = (pack/'solution/rblock.in').read_bytes()
    assert hashlib.sha256(reference.replace(b'\r\n', b'\n')).hexdigest() == REFERENCE_SHA
    assert hashlib.sha256(sample_raw.replace(b'\r\n', b'\n')).hexdigest() == SAMPLE_SHA
    assert (pack/'starter/rblock.in').read_bytes() == sample_raw
    assert (pack/'solution/rblock.out').read_text() == '2\n'
    learner = (pack/'starter/Main.java').read_bytes()
    assert learner != reference
    sample = sample_raw.decode().replace('\r\n', '\n')
    words = list(map(int, sample.split()))
    sample_roads = [(words[k]-1, words[k+1]-1, words[k+2]) for k in range(2, len(words), 3)]
    cases = []

    def tiny(name, n, roads, data=None):
        baseline, answer = oracle(n, roads)
        cases.append((name, encode(n, roads) if data is None else data, baseline, answer))

    tiny('official-sample', 5, sample_roads, sample)
    assert cases[-1][2:] == (6, 2)
    tiny('single-road', 2, [(0, 1, 5)])
    tiny('tied-best-routes', 4, [(0, 1, 1), (1, 3, 1), (0, 2, 1), (2, 3, 1)])
    tiny('bridge', 3, [(0, 1, 5), (1, 2, 7)])
    tiny('replacement-route', 3, [(0, 2, 5), (0, 1, 4), (1, 2, 4)])
    tiny('coincident-endpoints-positive-loop', 1, [(0, 0, 3)])
    tiny('positive-loop-and-reversed-roads', 3, [(0, 0, 1), (1, 0, 2), (2, 1, 3)])
    rng = random.Random(39811)
    for index in range(45):
        n = rng.randint(2, 15)
        roads = [(i-1, i, rng.randint(1, 40)) for i in range(1, n)]
        roads += [(a, b, rng.randint(1, 40)) for a in range(n) for b in range(a+2, n) if rng.random() < 0.25]
        roads = [(b, a, weight) if rng.random() < 0.5 else (a, b, weight) for a, b, weight in roads]
        tiny(f'independent-all-road-{index}', n, roads)
    independent_count = len(cases)
    n = 250
    cases.append(('maximum-length-chain', encode(n, [(i, i+1, 1_000_000) for i in range(n-1)]), 249_000_000, 1_000_000))
    pairs = [(i, i+1) for i in range(n-1)] + [(0, n-1)]
    seen = set(pairs)
    for a in range(n):
        for b in range(a+1, n):
            if len(pairs) == 25_000:
                break
            if (a, b) not in seen:
                pairs.append((a, b))
                seen.add((a, b))
        if len(pairs) == 25_000:
            break
    assert len(pairs) == 25_000
    for name, lengths, baseline, answer in [
        ('maximum-density-chain', [1000 if b == a+1 else 1_000_000 for a, b in pairs], 249_000, 1000),
        ('maximum-density-tied-unit-routes', [1] * len(pairs), 1, 1),
        ('maximum-density-maximum-weights', [1_000_000] * len(pairs), 1_000_000, 1_000_000),
    ]:
        cases.append((name, encode(n, [(a, b, w) for (a, b), w in zip(pairs, lengths)]), baseline, answer))

    invalid = [
        '0 1\n', '251 1\n', '2 0\n', '2 25001\n', '2\n', '2 1 7\n', 'two 1\n',
        '2 1\n1 2\n', '2 1\n1 2 5 6\n', '2 1\n1 2 zero\n',
        '2 1\n0 2 5\n', '2 1\n1 3 5\n', '2 1\n-2147483648 2 5\n',
        '2 1\n2147483647 2 5\n', '2 1\n1 2 0\n', '2 1\n1 2 -1\n', '2 1\n1 2 1000001\n',
        '2 2\n1 2 5\n1 2 7\n', '2 2\n1 2 5\n2 1 7\n',
        '3 1\n1 2 5\n', '2 1\n', '2 1\n\n', '2 1\n1 2 5\nextra\n',
    ]
    sentinel = b'earlier answer\n'
    with tempfile.TemporaryDirectory(prefix='roadblock-pack-acceptance-') as temp:
        roles = {}
        for role in ['starter', 'solution', 'probe']:
            cwd = Path(temp)/role
            cwd.mkdir()
            source = learner if role in ['starter', 'probe'] else reference
            files = ['Main.java']
            if role == 'probe':
                marker = b'throw new UnsupportedOperationException("Complete the four Roadblock sensitivity tasks");'
                assert source.count(marker) == 1
                source = source.replace(marker, b'return RoadblockDriverProbe.solve(problem);')
                (cwd/'RoadblockDriverProbe.java').write_text(PROBE)
                files.append('RoadblockDriverProbe.java')
            (cwd/'Main.java').write_bytes(source)
            run([javac, '--release', '17', '-encoding', 'UTF-8', '-Xlint:all', '-Werror', *files], cwd, timeout=45)
            roles[role] = cwd
        for name, data, baseline, answer in cases:
            cwd = roles['solution']
            (cwd/'rblock.in').write_text(data)
            (cwd/'rblock.out').write_bytes(sentinel)
            assert run([java, '-ea', '-Xmx256m', 'Main'], cwd) == (b'', b'')
            assert (cwd/'rblock.out').read_text() == f'{answer}\n', name
            assert (cwd/'rblock.in').read_text() == data
            cwd = roles['probe']
            (cwd/'rblock.in').write_text(data)
            assert run([java, '-ea', '-Xmx256m', 'RoadblockHelperProbe', str(baseline)], cwd) == (b'', b'')
            assert (cwd/'rblock.in').read_text() == data and not (cwd/'rblock.out').exists()
        unfinished = 0
        # Include full teaching bounds and the statement's minimally restricted cases.
        untouched = [cases[index][1] for index in [0, 1, 2, 5, 6, -4, -3, -1]] + [sample + '\n\n']
        for data in untouched:
            cwd = roles['starter']
            (cwd/'rblock.in').write_text(data)
            for previous in [False, True]:
                output = cwd/'rblock.out'
                if previous:
                    output.write_bytes(sentinel)
                else:
                    output.unlink(missing_ok=True)
                out, err = run([java, '-ea', '-Xmx256m', 'Main'], cwd, expected=2)
                assert not out and b'Complete the four Roadblock sensitivity tasks' in err
                assert output.read_bytes() == sentinel if previous else not output.exists()
                assert (cwd/'rblock.in').read_text() == data
                unfinished += 1
        refused = 0
        for data, args in [(item, []) for item in invalid] + [(None, []), (sample, ['extra'])]:
            cwd = roles['starter']
            inputfile = cwd/'rblock.in'
            if data is None:
                inputfile.unlink(missing_ok=True)
            else:
                inputfile.write_text(data)
            for previous in [False, True]:
                output = cwd/'rblock.out'
                if previous:
                    output.write_bytes(sentinel)
                else:
                    output.unlink(missing_ok=True)
                out, err = run([java, '-ea', '-Xmx256m', 'Main', *args], cwd, expected=2)
                assert not out and b'Cannot solve Roadblock:' in err and b'Complete the four' not in err
                assert output.read_bytes() == sentinel if previous else not output.exists()
                refused += 1
        cwd = roles['probe']
        for name, data, _, answer in cases[:7]:
            (cwd/'rblock.in').write_text(data)
            (cwd/'rblock.out').write_bytes(sentinel)
            assert run([java, '-ea', '-Xmx256m', 'RoadblockDriverProbe', 'normal'], cwd) == (b'', b'')
            assert (cwd/'rblock.out').read_text() == f'{answer}\n', name
        guards = 0
        for mode in ['negative', 'too-large']:
            (cwd/'rblock.in').write_text(sample)
            for previous in [False, True]:
                output = cwd/'rblock.out'
                if previous:
                    output.write_bytes(sentinel)
                else:
                    output.unlink(missing_ok=True)
                out, err = run([java, '-ea', '-Xmx256m', 'RoadblockDriverProbe', mode], cwd, expected=2)
                assert not out and b'Return an increase in 0..' in err
                assert output.read_bytes() == sentinel if previous else not output.exists()
                guards += 1
    after = {str(f.relative_to(pack)): hashlib.sha256(f.read_bytes()).hexdigest() for f in pack.rglob('*') if f.is_file()}
    assert before == after
    print(json.dumps(dict(event='gold-roadblock-pack-accepted', referenceFileCases=len(cases),
                          independentAllEdgeGraphs=independent_count, maximumDensityCases=3,
                          maximumFields=250, maximumRoads=25000, maximumWeight=1000000,
                          suppliedHelperFileCases=len(cases), tinyIndependentDriverCases=7,
                          suppliedHelperIndependentPaths=True, baselineParentSnapshotPreserved=True,
                          successiveAndFailedTrialRestoration=True, unfinishedLearnerCases=unfinished,
                          refusedInputCases=refused, invalidResultGuards=guards, previousAnswerPreserved=True,
                          learnerAlgorithmUnfinished=True, historicalReferenceInvalidInputClaims=False,
                          historicalJudgeRuntimeClaim=False, originalNormalizedReferenceSha256=REFERENCE_SHA,
                          originalSampleNormalizedSha256=SAMPLE_SHA, sourceFilesUnchanged=True,
                          roleSourceSha256={r: hashlib.sha256((pack/r/'Main.java').read_bytes().replace(b'\r\n', b'\n')).hexdigest() for r in ['starter', 'solution']})), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--javac', default='javac')
    parser.add_argument('--java', default='java')
    args = parser.parse_args()
    verify(Path(__file__).resolve().parents[1]/'UG10-Roadblock', args.javac, args.java)
